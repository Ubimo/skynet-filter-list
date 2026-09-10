"""Exact IPv4 interval algebra, bounded exceptions and redundancy observation."""
from __future__ import annotations
from datetime import datetime, timedelta
import ipaddress
import json
from pathlib import Path


def intervals(networks):
    result = []
    for start, end in sorted((int(n.network_address), int(n.broadcast_address)) for n in networks):
        if result and start <= result[-1][1] + 1:
            result[-1] = (result[-1][0], max(end, result[-1][1]))
        else:
            result.append((start, end))
    return result


def subtract(base, exclusions):
    result = []
    j = 0
    for start, end in base:
        while j < len(exclusions) and exclusions[j][1] < start:
            j += 1
        k = j
        while k < len(exclusions) and exclusions[k][0] <= end:
            lo, hi = exclusions[k]
            if lo > start:
                result.append((start, lo - 1))
            start = max(start, hi + 1)
            if start > end:
                break
            k += 1
        if start <= end:
            result.append((start, end))
    return result


def address_count(ranges):
    return sum(end - start + 1 for start, end in ranges)


def to_networks(ranges):
    return {n for start, end in ranges for n in ipaddress.summarize_address_range(
        ipaddress.IPv4Address(start), ipaddress.IPv4Address(end))}


def turnover(current, previous, feed):
    allowed = set(feed.get('allowed_special', []))
    old = intervals(n for n in previous if str(n) not in allowed)
    new = intervals(n for n in current if str(n) not in allowed)
    added, removed = address_count(subtract(new, old)), address_count(subtract(old, new))
    return {'added_addresses': added, 'removed_addresses': removed,
            'added_ratio': added / max(1, address_count(new)),
            'removed_ratio': removed / max(1, address_count(old))}


def load_allowlist(root: Path, now: datetime, read=None):
    if read is None:
        path = root / 'allowlist.json'
        body = path.read_text(encoding='utf-8') if path.exists() else '[]'
    else:
        body = read('allowlist.json')
    records = json.loads(body)
    if not isinstance(records, list):
        raise ValueError('allowlist.json must be a list')
    active, expired, seen = [], [], set()
    for item in records:
        network = ipaddress.ip_network(item['cidr'], strict=True)
        expires = datetime.fromisoformat(item['expires_at'])
        if network.version != 4 or network.prefixlen < 24:
            raise ValueError('Exceptions must be targeted IPv4 networks (/24 or narrower)')
        if not item.get('reason', '').strip() or expires.tzinfo is None or str(network) in seen:
            raise ValueError('Exceptions require a reason, timezone-aware expiry and unique CIDR')
        seen.add(str(network))
        (active if expires > now else expired).append(item)
    return active, expired


def combine(network_sets, exceptions):
    union = intervals(n for networks in network_sets for n in networks)
    excluded = intervals(ipaddress.ip_network(item['cidr']) for item in exceptions)
    return to_networks(subtract(union, excluded))


def select_sources(feeds, records, networks, previous, now):
    """Candidates cannot use one another as coverage evidence (no circular removal)."""
    healthy_core = intervals(n for f in feeds if not f.get('redundancy_candidate')
                             and records[f['name']]['status'] == 'ok'
                             for n in networks.get(f['name'], set()))
    evidence = {}
    for feed in feeds:
        name = feed['name']
        record = records[name]
        record['included'] = record['status'] in ('ok', 'stale')
        if not feed.get('redundancy_candidate'):
            continue
        old = previous.get(name, {})
        unique = address_count(subtract(intervals(networks.get(name, set())), healthy_core))
        same_policy = old.get('policy') == feed
        valid = record['status'] == 'ok' and unique == 0
        since, days = now, 0
        if valid:
            days = 1
            if same_policy and old.get('since'):
                last = datetime.fromisoformat(old['last_observed'])
                if timedelta(0) <= now - last <= timedelta(hours=48):
                    since = datetime.fromisoformat(old['since'])
                    days = old['days'] + int(now.date() != last.date())
            suppressed = days >= 14 and now - since >= timedelta(days=14)
        else:
            suppressed = False
        evidence[name] = {'policy': feed, 'since': since.isoformat(timespec='seconds') if valid else None,
                          'last_observed': now.isoformat(timespec='seconds'), 'days': days,
                          'unique_addresses': unique, 'suppressed': suppressed}
        record['included'] = record['included'] and not suppressed
    return evidence
