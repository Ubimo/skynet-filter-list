"""Permanent protection for infrastructure the router itself depends on.

Protected networks are subtracted from the published union, like exceptions,
but they never expire. Two parts:

- `networks` in protected.json: reviewed static entries (GitHub's own ranges,
  public DNS resolvers). Always applied, even if every download fails.
- `github_meta`: GitHub's published IPv4 ranges (https://api.github.com/meta),
  refreshed on every update and stored as generated/protected-github.ipv4 so the
  audit can verify it offline. On failure the last good snapshot stays in force
  (and the run fails so it gets noticed); it never expires, because older
  protection is still protection.

Strict bounds keep a broken or manipulated meta response from punching large
holes into the blocklist.
"""
from __future__ import annotations

from datetime import datetime
import ipaddress
import json
from pathlib import Path

from feed_policy import SPECIAL_BOUNDS, digest, serialize

GITHUB_SNAPSHOT = 'generated/protected-github.ipv4'
MIN_PREFIXLEN = 16
GITHUB_MAX_ADDRESSES = 131072
GITHUB_MIN_ENTRIES = 4


def overlaps_special(network) -> bool:
    start, end = int(network.network_address), int(network.broadcast_address)
    return any(start <= hi and end >= lo for lo, hi in SPECIAL_BOUNDS)


def load_protected(root: Path, read=None) -> dict:
    """Validated protection config; a missing file means no protection configured."""
    if read is None:
        path = root / 'protected.json'
        body = path.read_text(encoding='utf-8') if path.exists() else '{}'
    else:
        try:
            body = read('protected.json')
        except FileNotFoundError:
            body = '{}'
    config = json.loads(body)
    if not isinstance(config, dict) or set(config) - {'networks', 'github_meta'}:
        raise ValueError('protected.json must be an object with "networks" and optional "github_meta"')
    networks, seen = [], set()
    for item in config.get('networks', []):
        network = ipaddress.ip_network(item['cidr'], strict=True)
        if network.version != 4 or network.prefixlen < MIN_PREFIXLEN or overlaps_special(network):
            raise ValueError(f'Protected entries must be public IPv4 networks of /{MIN_PREFIXLEN} or narrower: {network}')
        if not str(item.get('reason', '')).strip() or str(network) in seen:
            raise ValueError(f'Protected entries require a reason and a unique CIDR: {network}')
        seen.add(str(network))
        networks.append(network)
    meta = config.get('github_meta')
    if meta is not None:
        keys = meta.get('keys')
        if (not str(meta.get('url', '')).startswith('https://') or not isinstance(keys, list) or not keys
                or not all(isinstance(k, str) and k for k in keys) or len(keys) != len(set(keys))):
            raise ValueError('github_meta requires an https:// url and a non-empty list of unique keys')
    return {'networks': networks, 'github_meta': meta}


def parse_github_meta(body: str, keys: list[str]) -> set[ipaddress.IPv4Network]:
    """IPv4 ranges of the selected meta keys. Any surprise rejects the response."""
    data = json.loads(body)
    if not isinstance(data, dict):
        raise ValueError('GitHub meta is not a JSON object')
    networks = set()
    for key in keys:
        values = data.get(key)
        if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
            raise ValueError(f'GitHub meta key missing or not a list of strings: {key}')
        for value in values:
            network = ipaddress.ip_network(value, strict=False)
            if network.version == 6:
                continue
            if network.prefixlen < MIN_PREFIXLEN or overlaps_special(network):
                raise ValueError(f'GitHub meta range too broad or special-use: {network}')
            networks.add(network)
    collapsed = set(ipaddress.collapse_addresses(networks))
    addresses = sum(n.num_addresses for n in collapsed)
    if len(collapsed) < GITHUB_MIN_ENTRIES:
        raise ValueError(f'GitHub meta has only {len(collapsed)} IPv4 ranges; minimum {GITHUB_MIN_ENTRIES}')
    if addresses > GITHUB_MAX_ADDRESSES:
        raise ValueError(f'GitHub meta covers {addresses} IPv4 addresses; maximum {GITHUB_MAX_ADDRESSES}')
    return collapsed


def read_github_snapshot(root: Path, record: dict | None, read=None):
    """Networks of the recorded snapshot, verified by hash; None if there is none."""
    if not record or record.get('status') not in ('ok', 'stale'):
        return None
    body = read(GITHUB_SNAPSHOT) if read else (root / GITHUB_SNAPSHOT).read_text(encoding='utf-8')
    if digest(body) != record['sha256']:
        raise ValueError('GitHub protection snapshot hash mismatch')
    networks = {ipaddress.ip_network(line) for line in body.splitlines() if line}
    if serialize(networks) != body or len(networks) != record['entries']:
        raise ValueError('GitHub protection snapshot is not canonical')
    return networks


def refresh_github(root: Path, meta: dict | None, previous: dict | None, now: datetime, fetch):
    """Returns (record, body to write or None). Never raises for upstream problems."""
    if meta is None:
        return None, None
    stamp = now.isoformat(timespec='seconds')
    try:
        networks = parse_github_meta(fetch(meta['url']), meta['keys'])
        body = serialize(networks)
        return {'url': meta['url'], 'keys': meta['keys'], 'status': 'ok', 'last_success': stamp,
                'checked_at': stamp, 'error': None, 'entries': len(networks),
                'addresses': sum(n.num_addresses for n in networks), 'sha256': digest(body)}, body
    except Exception as error:
        message = f'{type(error).__name__}: {error}'
        same = previous and previous.get('url') == meta['url'] and previous.get('keys') == meta['keys']
        try:
            usable = same and read_github_snapshot(root, previous) is not None
        except (OSError, ValueError, KeyError):
            usable = False
        if usable:
            record = dict(previous, status='stale', checked_at=stamp, error=message)
        else:
            record = {'url': meta['url'], 'keys': meta['keys'], 'status': 'missing', 'last_success': None,
                      'checked_at': stamp, 'error': message}
        return record, None


def protected_networks(config: dict, github) -> list:
    return [*config['networks'], *(github or ())]
