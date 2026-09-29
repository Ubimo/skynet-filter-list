"""Refresh independent validated snapshots, retaining good data for at most 72h."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

from feed_policy import (
    ROOT, RAW_PREFIX, MAX_STALE_HOURS, COMBINED_MIN_RATIO, COMBINED_MAX_RATIO,
    LEVEL_SHIFT_CONFIRM_HOURS, LevelShiftError, atomic_write, check_change, digest,
    download, load_feeds, metrics, parse, serialize, shift_consistent, snapshot_body,
    unchanged_limit,
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


def unchanged_since(previous: dict, sha256: str, now: datetime) -> datetime:
    """When the accepted content last changed. Unknown history starts the clock
    now, so introducing this check can never produce a false alarm."""
    if previous.get('sha256') == sha256 and previous.get('content_changed_at'):
        try:
            changed = datetime.fromisoformat(previous['content_changed_at'])
            if changed.tzinfo is not None and changed <= now:
                return changed
        except ValueError:
            pass
    return now


def pending_since(pending: dict | None, now: datetime):
    try:
        since = datetime.fromisoformat(pending['first_seen'])
        return since if since.tzinfo is not None and since <= now else None
    except (KeyError, TypeError, ValueError):
        return None


def refresh_one(root: Path, feed: dict, previous: dict, now: datetime, fetch):
    old = previous_snapshot(root, feed, previous, now)
    name = feed["name"]
    shift = None
    try:
        upstream = fetch(feed["url"])
        meta = metadata(upstream, feed, now)
        parsed = parse(upstream, feed)
        current = metrics(parsed.networks, feed)
        if previous.get("last_success") and old is None:
            raise ValueError("Recorded baseline is missing, corrupt or incompatible with policy")
        if old:
            try:
                check_change(current, previous["metrics"])
            except LevelShiftError:
                pending = previous.get('pending_shift')
                since = pending_since(pending, now)
                if not (since and shift_consistent(pending, current)
                        and now - since >= timedelta(hours=LEVEL_SHIFT_CONFIRM_HOURS)):
                    raise
                # Same new level seen again after the confirmation window: a real
                # upstream change, not a glitch. All other checks still apply below.
                shift = {'from': previous['metrics'], 'to': current, 'first_seen': pending['first_seen'],
                         'accepted_at': timestamp(now)}
        churn = turnover(parsed.networks, parse(old[0], feed, published=True).networks, feed) if old else None
        if churn and max(churn['added_ratio'], churn['removed_ratio']) > feed.get('max_churn_ratio', 0.8):
            raise ValueError(f"Anomalous address turnover: {churn}")
        body = snapshot_body(parsed.networks, meta)
        sha256 = digest(body)
        changed = unchanged_since(previous, sha256, now)
        limit = unchanged_limit(feed)
        if limit and now - changed > timedelta(hours=limit):
            raise StaleSourceError(
                f"Content unchanged since {changed.isoformat(timespec='seconds')} (limit {limit}h)", changed)
        record = {
            "url": feed["url"], "status": "ok", "last_success": timestamp(now),
            "checked_at": timestamp(now), "metrics": current,
            "excluded_ipv6": parsed.ipv6, "excluded_special": parsed.excluded_special,
            "excluded_invalid": parsed.invalid,
            "error": None, "turnover": churn, **meta,
            "content_changed_at": timestamp(changed), "sha256": sha256,
            **({"level_shift_accepted": shift} if shift else {}),
        }
        return name, record, body, True
    except Exception as error:
        active = (old is not None and now - old[1] <= timedelta(hours=MAX_STALE_HOURS)
                  and fallback_fresh(previous, feed, now))
        record = dict(previous) if previous else {"last_success": None}
        record.pop("level_shift_accepted", None)
        record["url"] = feed["url"]
        if isinstance(error, LevelShiftError):
            pending = previous.get('pending_shift')
            if not (pending_since(pending, now) and shift_consistent(pending, error.metrics)):
                pending = {'first_seen': timestamp(now)}
            # Latest observation, anchored to when this level was first seen.
            record['pending_shift'] = {'first_seen': pending['first_seen'], 'metrics': error.metrics}
        elif not isinstance(error, (OSError, TimeoutError)):
            # A different content problem breaks the confirmation chain.
            record.pop('pending_shift', None)
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
        message = f"{type(error).__name__}: {error}"
        if record.get('pending_shift') and isinstance(error, LevelShiftError):
            message += (f" (pending since {record['pending_shift']['first_seen']}; accepted automatically "
                        f"if seen again after {LEVEL_SHIFT_CONFIRM_HOURS}h)")
        record.update(status=status, checked_at=timestamp(now), error=message)
        return name, record, None, active


def render_report(feeds: list[dict], state: dict) -> str:
    lines = [
        "# Current feed audit", "", "Automatically generated; historical notes are in `AUDIT-HISTORY.md`.", "",
        f"- Checked at: {state['checked_at']}",
        f"- Configured sources: {len(feeds)}",
        f"- Contributing sources: {sum(r.get('included', False) for r in state['sources'].values())}",
        f"- Combined IPv4/CIDR entries: {state['combined']['entries']}",
        *([f"- Combined coverage anomaly: {state['combined_anomaly']}"] if state.get('combined_anomaly') else []),
        f"- Active / expired exceptions: {len(state['allowlist_active'])} / {len(state['allowlist_expired'])}",
        f"- Maximum fallback age: {MAX_STALE_HOURS} hours",
        *[f"- Pending level shift: {f['name']} {state['sources'][f['name']]['metrics']['entries']} -> "
          f"{state['sources'][f['name']]['pending_shift']['metrics']['entries']} entries, first seen "
          f"{state['sources'][f['name']]['pending_shift']['first_seen']}"
          for f in feeds if state['sources'][f['name']].get('pending_shift')
          and state['sources'][f['name']]['status'] == 'stale'],
        *[f"- Accepted level shift: {f['name']} {r['level_shift_accepted']['from']['entries']} -> "
          f"{r['level_shift_accepted']['to']['entries']} entries, first seen {r['level_shift_accepted']['first_seen']}"
          for f in feeds for r in [state['sources'][f['name']]] if r.get('level_shift_accepted')],
        "",
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


def combined_anomaly(previous_public, public):
    if not previous_public or COMBINED_MIN_RATIO * previous_public <= public <= COMBINED_MAX_RATIO * previous_public:
        return None
    return (f"Combined public coverage changed {previous_public} -> {public} "
            f"(allowed {COMBINED_MIN_RATIO}x to {COMBINED_MAX_RATIO}x)")


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
        # A growth shift awaiting confirmation (still on its good fallback) is an
        # expected, self-resolving state; it fails the run only once it expires.
        confirming = record["status"] == 'stale' and 'pending_shift' in record and 'LevelShiftError' in (record["error"] or '')
        degraded |= record["status"] in ('stale', 'disabled') and not confirming
        print(f"{name}: {record['status']}" + (f" ({record['error']})" if record["error"] else ""))
    state['redundancy'] = select_sources(feeds, state['sources'], networks, previous.get('redundancy', {}), now)
    selected = [ns for name, ns in networks.items() if state['sources'][name]['included']]
    combined = combine(selected, exceptions)
    # A suppressed candidate must never change the actual union, even if state is damaged.
    if combined != combine(networks.values(), exceptions):
        raise ValueError('Redundancy suppression would lose coverage')
    body = combined_body(combined, state['sources'])
    public = sum(n.num_addresses for n in combined)
    state['combined'] = {'entries': len(combined), 'sha256': digest(body), 'public_addresses': public}
    state['combined_anomaly'] = combined_anomaly(previous.get('combined', {}).get('public_addresses'), public)
    if state['combined_anomaly']:
        # Published anyway (every source passed its own checks); main() exits 2 so a
        # large unreviewed swing of the whole list fails the run and gets noticed.
        # Not part of the per-source `degraded` result: an expected quarantine
        # stays an expected state for the sources themselves.
        print(f"combined: {state['combined_anomaly']}")
    state['allowlist_active'], state['allowlist_expired'] = exceptions, expired
    atomic_write(root / 'generated/combined.ipv4', body)
    atomic_write(root / "filter.list", RAW_PREFIX + 'generated/combined.ipv4\n' if combined else '')
    atomic_write(root / "generated/status.json", json.dumps(state, indent=2) + "\n")
    atomic_write(root / "AUDIT.md", render_report(feeds, state))
    atomic_write(root / ".update-result.json", json.dumps({"degraded": degraded,
                                                           "combined_anomaly": state['combined_anomaly']}) + "\n")
    return degraded


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    degraded = update(args.root)
    anomaly = json.loads((args.root / ".update-result.json").read_text(encoding="utf-8"))["combined_anomaly"]
    raise SystemExit(2 if degraded or anomaly else 0)


if __name__ == "__main__":
    main()
