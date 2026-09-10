"""Validate the exact local or immutable remote snapshot, without regenerating it."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re

from feed_policy import ROOT, RAW_PREFIX, MAX_STALE_HOURS, digest, download, load_feeds, metrics, parse, snapshot_body
from update_ipv4_feeds import combined_body, render_report
from feed_analysis import combine, load_allowlist
from feed_freshness import fallback_fresh


def validate(root: Path = ROOT, *, now: datetime | None = None, read=None) -> None:
    # In historical/PR validation use the recorded audit time; --current enforces
    # wall-clock age for publication and monitoring.
    read = read or (lambda path: (root / path).read_text(encoding="utf-8"))
    feeds = load_feeds(root)
    state = json.loads(read("generated/status.json"))
    checked = datetime.fromisoformat(state["checked_at"])
    now = now or checked
    if checked.tzinfo is None or checked > now:
        raise ValueError("Invalid audit timestamp")
    names = {feed["name"] for feed in feeds}
    if set(state["sources"]) != names:
        raise ValueError("Source status does not match configured sources")
    manifest = read("filter.list").splitlines()
    if not manifest or len(manifest) != len(set(manifest)):
        raise ValueError("Empty manifest or duplicate source URLs")
    active = []
    for feed in feeds:
        record = state["sources"][feed["name"]]
        if record["url"] != feed["url"] or record["status"] not in ("ok", "stale", "disabled", "quarantined"):
            raise ValueError(f"Invalid status: {feed['name']}")
        if record["checked_at"] != state["checked_at"]:
            raise ValueError("Source was not checked in this snapshot")
        if record["status"] in ('disabled', 'quarantined'):
            if not record.get("error") or record.get('included'):
                raise ValueError("Disabled source must explain its failure")
            continue
        last = datetime.fromisoformat(record["last_success"])
        if last.tzinfo is None or last > checked or now - last > timedelta(hours=MAX_STALE_HOURS):
            raise ValueError(f"Expired or invalid fallback: {feed['name']}")
        if record["status"] == "ok" and (last != checked or record.get("error")):
            raise ValueError("Healthy source has inconsistent status")
        if record["status"] == "stale" and not record.get("error"):
            raise ValueError("Stale source must explain its failure")
        if not fallback_fresh(record, feed, now):
            raise ValueError(f"Expired or missing provider timestamp: {feed['name']}")
        if not record.get('included') and not (feed.get('redundancy_candidate') and
                state.get('redundancy', {}).get(feed['name'], {}).get('suppressed')):
            raise ValueError('Source omitted without redundancy evidence')
        path = f"generated/{feed['name']}.ipv4"
        active.append((feed, record, path))
    if manifest != [RAW_PREFIX + 'generated/combined.ipv4']:
        raise ValueError("Manifest differs from validated active sources")

    def verify(item):
        feed, record, path = item
        body = read(path)
        parsed = parse(body, feed, published=True)
        if body != snapshot_body(parsed.networks, record):
            raise ValueError(f"Noncanonical or duplicate entries: {path}")
        if digest(body) != record["sha256"] or metrics(parsed.networks, feed) != record["metrics"]:
            raise ValueError(f"Content/hash/metrics mismatch: {path}")
        return feed['name'], parsed.networks

    with ThreadPoolExecutor(max_workers=8) as executor:
        networks = dict(executor.map(verify, active))
    exceptions, expired = load_allowlist(root, checked, read=read)
    if exceptions != state['allowlist_active'] or expired != state['allowlist_expired']:
        raise ValueError('Exception state differs from allowlist.json')
    if load_allowlist(root, now, read=read)[0] != exceptions:
        raise ValueError('Exception expired between generation and publication; regenerate')
    combined = combine(networks.values(), exceptions)
    selected = combine([ns for name, ns in networks.items() if state['sources'][name]['included']], exceptions)
    if combined != selected:
        raise ValueError('Suppression loses coverage')
    body = read('generated/combined.ipv4')
    if not combined or body != combined_body(combined, state['sources']):
        raise ValueError('Combined file does not exactly equal validated sources minus exceptions')
    if state['combined'] != {'entries': len(combined), 'sha256': digest(body)}:
        raise ValueError('Combined hash/count mismatch')
    if read("AUDIT.md") != render_report(feeds, state):
        raise ValueError("AUDIT.md is not synchronized with status.json")
    print(f"Validated {len(active)} usable sources, {len(combined)} combined entries; exact coverage, exceptions, hashes and report match")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--current", action="store_true")
    parser.add_argument("--remote-ref", help="Verify raw GitHub content at this immutable commit SHA")
    args = parser.parse_args()
    read = None
    if args.remote_ref:
        if not re.fullmatch(r"[0-9a-f]{40}", args.remote_ref):
            parser.error("--remote-ref requires a full commit SHA")
        prefix = RAW_PREFIX.replace("/main/", f"/{args.remote_ref}/")
        # Check config too, so local policy cannot accidentally verify another tree.
        if download(prefix + "sources.json") != (args.root / "sources.json").read_text(encoding="utf-8"):
            raise ValueError("Remote source configuration differs from checkout")
        read = lambda path: download(prefix + path)
    validate(args.root, now=datetime.now(timezone.utc) if args.current else None, read=read)


if __name__ == "__main__":
    main()
