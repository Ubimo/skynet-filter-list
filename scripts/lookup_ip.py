"""Explain a published IPv4 block and the source networks responsible for it."""
from __future__ import annotations
import argparse
from datetime import datetime
import ipaddress
import json
from pathlib import Path
from feed_policy import ROOT, load_feeds
from feed_analysis import load_allowlist
from feed_protection import load_protected, read_github_snapshot


def lookup(address: str, root: Path = ROOT) -> dict:
    ip = ipaddress.IPv4Address(address)
    state = json.loads((root / 'generated/status.json').read_text(encoding='utf-8'))
    def matching(path):
        matches = []
        for line in path.read_text(encoding='utf-8').splitlines():
            if line and not line.startswith('#'):
                network = ipaddress.ip_network(line)
                if ip in network:
                    matches.append(str(network))
        return matches
    sources = []
    for feed in load_feeds(root):
        record = state['sources'][feed['name']]
        if record['status'] not in ('ok', 'stale'):
            continue
        matches = matching(root / f"generated/{feed['name']}.ipv4")
        if matches:
            sources.append({'source': feed['name'], 'url': feed['url'], 'networks': matches,
                            'contributing': record['included'], 'status': record['status']})
    exceptions, _ = load_allowlist(root, datetime.fromisoformat(state['checked_at']))
    shield = load_protected(root)
    github = read_github_snapshot(root, state.get('protection', {}).get('github_meta')) or set()
    protected = [{'cidr': str(n), 'origin': 'protected.json'} for n in shield['networks'] if ip in n]
    protected += [{'cidr': str(n), 'origin': 'GitHub meta'} for n in sorted(github) if ip in n]
    return {'address': str(ip), 'snapshot_at': state['checked_at'],
            'blocked_in_published_snapshot': bool(matching(root / 'generated/combined.ipv4')),
            'sources': sources,
            'exceptions_at_publication': [item for item in exceptions if ip in ipaddress.ip_network(item['cidr'])],
            'protected': protected}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('address', help='IPv4 address to explain')
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    print(json.dumps(lookup(args.address, args.root), indent=2))


if __name__ == '__main__':
    main()
