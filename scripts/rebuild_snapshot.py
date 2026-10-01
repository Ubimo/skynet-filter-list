"""Rebuild the committed snapshot offline after sources were removed from sources.json
or protected.json changed.

Uses only the already validated generated/*.ipv4 files: no downloads, checked_at
unchanged. Removing a source or adding a protected network this way keeps the PR
check (exact committed snapshot) green. New or changed sources still require a
normal update run; a new or changed GitHub meta configuration is recorded as
`missing` (static protection only) until the next update run fetches it.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from feed_policy import ROOT, atomic_write, digest, load_feeds, parse
from feed_analysis import address_count, combine, intervals, subtract
from update_ipv4_feeds import combined_body, load_state, protection_record, render_report
from feed_protection import load_protected, protected_networks, read_github_snapshot


def rebuild(root: Path = ROOT) -> list[str]:
    feeds = load_feeds(root)
    names = {feed['name'] for feed in feeds}
    state = load_state(root)
    if 'checked_at' not in state:
        raise ValueError('No committed snapshot to rebuild')
    missing = sorted(names - set(state['sources']))
    if missing:
        raise ValueError(f'New sources require a normal update run: {missing}')
    removed = sorted(set(state['sources']) - names)
    for name in removed:
        del state['sources'][name]
        state.get('redundancy', {}).pop(name, None)
    for record in state['sources'].values():
        for obsolete in ('pending_shift', 'level_shift_accepted'):  # from the removed size limits
            record.pop(obsolete, None)
    for feed in feeds:
        if state['sources'][feed['name']].get('url') != feed['url']:
            raise ValueError(f"Changed source URL requires a normal update run: {feed['name']}")

    networks = {}
    for feed in feeds:
        record = state['sources'][feed['name']]
        if record['status'] not in ('ok', 'stale'):
            continue
        body = (root / f"generated/{feed['name']}.ipv4").read_text(encoding='utf-8')
        if digest(body) != record['sha256']:
            raise ValueError(f"Snapshot hash mismatch: {feed['name']}")
        networks[feed['name']] = parse(body, feed, published=True).networks

    # Same evidence rule as select_sources, without advancing observation days:
    # this is not a new observation, only the old one minus removed sources.
    core = intervals(n for f in feeds if not f.get('redundancy_candidate')
                     and state['sources'][f['name']]['status'] == 'ok'
                     for n in networks.get(f['name'], set()))
    for feed in feeds:
        record = state['sources'][feed['name']]
        record['included'] = record['status'] in ('ok', 'stale')
        evidence = state.get('redundancy', {}).get(feed['name'])
        if not feed.get('redundancy_candidate') or evidence is None:
            continue
        evidence['unique_addresses'] = address_count(subtract(intervals(networks.get(feed['name'], set())), core))
        if evidence['unique_addresses']:
            evidence.update(since=None, days=0, suppressed=False)
        record['included'] = record['included'] and not evidence['suppressed']

    exceptions = state['allowlist_active']
    shield = load_protected(root)
    meta = shield['github_meta']
    github = state.get('protection', {}).get('github_meta')
    if meta is None:
        github = None
    elif not github or github.get('url') != meta['url'] or github.get('keys') != meta['keys']:
        github = {'url': meta['url'], 'keys': meta['keys'], 'status': 'missing', 'last_success': None,
                  'checked_at': state['checked_at'], 'error': 'Not fetched yet; static protection only until the next update run'}
    protected = protected_networks(shield, read_github_snapshot(root, github))
    combined = combine([ns for name, ns in networks.items() if state['sources'][name]['included']], exceptions, protected)
    if combined != combine(networks.values(), exceptions, protected):
        raise ValueError('Redundancy suppression would lose coverage')
    body = combined_body(combined, state['sources'])
    state['combined'] = {'entries': len(combined), 'sha256': digest(body),
                         'public_addresses': sum(n.num_addresses for n in combined)}
    state.pop('combined_anomaly', None)  # from the removed size limits
    state['protection'] = protection_record(shield, github, networks, exceptions, protected, state['sources'])
    atomic_write(root / 'generated/combined.ipv4', body)
    atomic_write(root / 'generated/status.json', json.dumps(state, indent=2) + '\n')
    atomic_write(root / 'AUDIT.md', render_report(feeds, state))
    for name in removed:
        (root / f'generated/{name}.ipv4').unlink(missing_ok=True)
    return removed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    removed = rebuild(args.root)
    print(f"Removed: {', '.join(removed) or 'nothing'}; now run: python scripts/audit_sources.py")


if __name__ == '__main__':
    main()
