"""Refresh independent validated snapshots, retaining good data for at most 72h."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

from feed_policy import (
    ROOT, RAW_PREFIX, MAX_STALE_HOURS, atomic_write, check_change, digest,
    download, load_feeds, metrics, parse, serialize,
    snapshot_body,
)
from feed_analysis import combine, load_allowlist, select_sources, turnover
from feed_freshness import StaleSourceError, fallback_fresh, metadata


def timestamp(now: datetime) -> str:
    return now.isoformat(timespec="seconds")


def load_state(root: Path) -> dict:
    path = root / "generated/status.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"sources": {}}


def previous_snapshot(root: Path, feed: dict, previous: dict, now: datetime):
    """Only recorded, intact, policy-valid data can be used as a fallback."""
    if previous.get("baseline_url", previous.get("url")) != feed["url"] or not previous.get("last_success"):
        return None
    try:
        date = datetime.fromisoformat(previous["last_success"])
        if date.tzinfo is None or date > now:
            return None
        body = (root / f"generated/{feed['name']}.ipv4").read_text(encoding="utf-8")
        if digest(body) != previous["sha256"]:
            return None
        parsed = parse(body, feed, published=True)
        if snapshot_body(parsed.networks, previous) != body or metrics(parsed.networks, feed) != previous["metrics"]:
            return None
        return body, date
    except (ValueError, KeyError, OSError):
        return None


def refresh_one(root: Path, feed: dict, previous: dict, now: datetime, fetch):
    old = previous_snapshot(root, feed, previous, now)
    name = feed["name"]
    try:
        upstream = fetch(feed["url"])
        meta = metadata(upstream, feed, now)
        parsed = parse(upstream, feed)
        current = metrics(parsed.networks, feed)
        if previous.get("last_success") and old is None:
            raise ValueError("Recorded baseline is missing, corrupt or incompatible with policy")
        if old:
            check_change(current, previous["metrics"])
        churn = turnover(parsed.networks, parse(old[0], feed, published=True).networks, feed) if old else None
        if churn and max(churn['added_ratio'], churn['removed_ratio']) > feed.get('max_churn_ratio', 0.8):
            raise ValueError(f"Anomalous address turnover: {churn}")
        record = {
            "url": feed["url"], "status": "ok", "last_success": timestamp(now),
            "checked_at": timestamp(now), "metrics": current,
            "excluded_ipv6": parsed.ipv6, "excluded_special": parsed.excluded_special,
            "error": None, "turnover": churn, **meta,
        }
        body = snapshot_body(parsed.networks, record)
        record['sha256'] = digest(body)
        return name, record, body, True
    except Exception as error:
        active = (old is not None and now - old[1] <= timedelta(hours=MAX_STALE_HOURS)
                  and fallback_fresh(previous, feed, now))
        record = dict(previous) if previous else {"last_success": None}
        record["url"] = feed["url"]
        if previous.get("last_success") and old is None:
            record["baseline_invalid"] = True
            record["baseline_url"] = previous.get("baseline_url", previous["url"])
        status = 'stale' if active else 'disabled'
        if not active and isinstance(error, StaleSourceError) and feed.get('quarantine_on_stale'):
            status = 'quarantined'
            # Do not treat the pre-freshness, known-old Feodo snapshot as a
            # trustworthy count baseline when fresh observations first return.
            if not previous.get('upstream_updated_at'):
                record = {'url': feed['url'], 'last_success': None}
        if isinstance(error, StaleSourceError):
            record['rejected_upstream_updated_at'] = error.updated.isoformat(timespec='seconds')
        record.update(status=status, checked_at=timestamp(now),
                      error=f"{type(error).__name__}: {error}")
        return name, record, None, active


def render_report(feeds: list[dict], state: dict) -> str:
    lines = [
        "# Current feed audit", "", "Automatically generated; historical notes are in `AUDIT-HISTORY.md`.", "",
        f"- Checked at: {state['checked_at']}",
        f"- Configured sources: {len(feeds)}",
        f"- Contributing sources: {sum(r.get('included', False) for r in state['sources'].values())}",
        f"- Combined IPv4/CIDR entries: {state['combined']['entries']}",
        f"- Active / expired exceptions: {len(state['allowlist_active'])} / {len(state['allowlist_expired'])}",
        f"- Maximum fallback age: {MAX_STALE_HOURS} hours", "",
        "Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.",
        "Last success means successful retrieval and validation, not an upstream observation date.", "",
        "| Source | State | Included | Entries | Provider timestamp | Last success |",
        "|---|---|---|---:|---|---|",
    ]
    for feed in feeds:
        r = state["sources"][feed["name"]]
        provider_date = r.get('upstream_updated_at')
        if r['status'] not in ('ok', 'stale'):
            provider_date = r.get('rejected_upstream_updated_at') or provider_date
        lines.append(f"| [{feed['name']}]({feed['url']}) | {r['status']} | {r.get('included', False)} | "
                     f"{r.get('metrics', {}).get('entries', 0)} | {provider_date or 'unknown'} | "
                     f"{r.get('last_success') or 'never'} |")
    lines += ['', '## Automatic redundancy observation', '',
              '| Candidate | Zero-contribution days | Additional addresses | Suppressed |',
              '|---|---:|---:|---|']
    for name, r in state.get('redundancy', {}).items():
        lines.append(f"| {name} | {r['days']} | {r['unique_addresses']} | {r['suppressed']} |")
    lines += ["", "Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.",
              "A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.",
              "Provider timestamps describe the supplied file, not necessarily each underlying threat observation.",
              "Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.", ""]
    return "\n".join(lines)


def combined_body(networks, records):
    attribution = sorted({line for r in records.values() if r['status'] in ('ok', 'stale')
                          for line in r.get('attribution', [])})
    return snapshot_body(networks, {'attribution': attribution})


def update(root: Path = ROOT, *, now: datetime | None = None, fetch=download, workers: int = 8) -> bool:
    now = now or datetime.now(timezone.utc)
    feeds = load_feeds(root)
    previous = load_state(root)
    exceptions, expired = load_allowlist(root, now)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(
            lambda feed: refresh_one(root, feed, previous["sources"].get(feed["name"], {}), now, fetch), feeds,
        ))
    state = {"checked_at": timestamp(now), "sources": {}}
    networks = {}
    degraded = False
    for name, record, body, active in results:
        state["sources"][name] = record
        if body is not None:
            atomic_write(root / f"generated/{name}.ipv4", body)
        if active:
            feed = next(f for f in feeds if f['name'] == name)
            networks[name] = parse((root / f'generated/{name}.ipv4').read_text(encoding='utf-8'), feed, published=True).networks
        degraded |= record["status"] in ('stale', 'disabled')
        print(f"{name}: {record['status']}" + (f" ({record['error']})" if record["error"] else ""))
    state['redundancy'] = select_sources(feeds, state['sources'], networks, previous.get('redundancy', {}), now)
    selected = [ns for name, ns in networks.items() if state['sources'][name]['included']]
    combined = combine(selected, exceptions)
    # A suppressed candidate must never change the actual union, even if state is damaged.
    if combined != combine(networks.values(), exceptions):
        raise ValueError('Redundancy suppression would lose coverage')
    body = combined_body(combined, state['sources'])
    state['combined'] = {'entries': len(combined), 'sha256': digest(body)}
    state['allowlist_active'], state['allowlist_expired'] = exceptions, expired
    atomic_write(root / 'generated/combined.ipv4', body)
    atomic_write(root / "filter.list", RAW_PREFIX + 'generated/combined.ipv4\n' if combined else '')
    atomic_write(root / "generated/status.json", json.dumps(state, indent=2) + "\n")
    atomic_write(root / "AUDIT.md", render_report(feeds, state))
    atomic_write(root / ".update-result.json", json.dumps({"degraded": degraded}) + "\n")
    return degraded


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    raise SystemExit(2 if update(args.root) else 0)


if __name__ == "__main__":
    main()
