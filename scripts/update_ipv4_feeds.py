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
)


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
        if serialize(parsed.networks) != body or metrics(parsed.networks, feed) != previous["metrics"]:
            return None
        return body, date
    except (ValueError, KeyError, OSError):
        return None


def refresh_one(root: Path, feed: dict, previous: dict, now: datetime, fetch):
    old = previous_snapshot(root, feed, previous, now)
    name = feed["name"]
    try:
        parsed = parse(fetch(feed["url"]), feed)
        current = metrics(parsed.networks, feed)
        if previous.get("last_success") and old is None:
            raise ValueError("Recorded baseline is missing, corrupt or incompatible with policy")
        if old:
            check_change(current, previous["metrics"])
        body = serialize(parsed.networks)
        record = {
            "url": feed["url"], "status": "ok", "last_success": timestamp(now),
            "checked_at": timestamp(now), "sha256": digest(body), "metrics": current,
            "excluded_ipv6": parsed.ipv6, "excluded_special": parsed.excluded_special,
            "error": None,
        }
        return name, record, body, True
    except Exception as error:
        active = old is not None and now - old[1] <= timedelta(hours=MAX_STALE_HOURS)
        record = dict(previous) if previous else {"last_success": None}
        record["url"] = feed["url"]
        if previous.get("last_success") and old is None:
            record["baseline_invalid"] = True
            record["baseline_url"] = previous.get("baseline_url", previous["url"])
        record.update(status="stale" if active else "disabled", checked_at=timestamp(now),
                      error=f"{type(error).__name__}: {error}")
        return name, record, None, active


def render_report(feeds: list[dict], state: dict) -> str:
    lines = [
        "# Current feed audit", "", "Automatically generated; historical notes are in `AUDIT-HISTORY.md`.", "",
        f"- Checked at: {state['checked_at']}",
        f"- Configured sources: {len(feeds)}",
        f"- Active sources: {sum(r['status'] != 'disabled' for r in state['sources'].values())}",
        f"- Maximum fallback age: {MAX_STALE_HOURS} hours", "",
        "Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.",
        "Last success means successful retrieval and validation, not an upstream observation date.", "",
        "| Source | State | Entries | IPv6 excluded | Special-use excluded | Last success |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for feed in feeds:
        r = state["sources"][feed["name"]]
        lines.append(f"| [{feed['name']}]({feed['url']}) | {r['status']} | "
                     f"{r.get('metrics', {}).get('entries', 0)} | {r.get('excluded_ipv6', 0)} | "
                     f"{r.get('excluded_special', 0)} | {r.get('last_success') or 'never'} |")
    lines += ["", "Failure details and content SHA-256 hashes are in `generated/status.json`.", ""]
    return "\n".join(lines)


def update(root: Path = ROOT, *, now: datetime | None = None, fetch=download, workers: int = 8) -> bool:
    now = now or datetime.now(timezone.utc)
    feeds = load_feeds(root)
    previous = load_state(root)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(
            lambda feed: refresh_one(root, feed, previous["sources"].get(feed["name"], {}), now, fetch), feeds,
        ))
    state = {"checked_at": timestamp(now), "sources": {}}
    manifest = []
    degraded = False
    for name, record, body, active in results:
        state["sources"][name] = record
        if body is not None:
            atomic_write(root / f"generated/{name}.ipv4", body)
        if active:
            manifest.append(f"{RAW_PREFIX}generated/{name}.ipv4")
        degraded |= record["status"] != "ok"
        print(f"{name}: {record['status']}" + (f" ({record['error']})" if record["error"] else ""))
    atomic_write(root / "filter.list", "\n".join(manifest) + ("\n" if manifest else ""))
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
