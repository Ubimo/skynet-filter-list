"""Shared, deterministic validation for upstream and published IPv4 feeds."""
from __future__ import annotations

import csv
from dataclasses import dataclass
import hashlib
import io
import ipaddress
import json
from pathlib import Path
import re
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
RAW_PREFIX = "https://raw.githubusercontent.com/Ubimo/skynet-filter-list/main/"
MAX_SOURCE_BYTES = 64 * 1024 * 1024
MAX_STALE_HOURS = 72
# Conservative special-use policy; exceptions must be exact, reviewed prefixes.
SPECIAL = tuple(ipaddress.IPv4Network(n) for n in (
    "0.0.0.0/8", "10.0.0.0/8", "100.64.0.0/10", "127.0.0.0/8",
    "169.254.0.0/16", "172.16.0.0/12", "192.0.0.0/24", "192.0.2.0/24",
    "192.168.0.0/16", "198.18.0.0/15", "198.51.100.0/24",
    "203.0.113.0/24", "224.0.0.0/3",
))
SPECIAL_BOUNDS = tuple((int(n.network_address), int(n.broadcast_address)) for n in SPECIAL)


@dataclass
class Parsed:
    networks: set[ipaddress.IPv4Network]
    ipv6: int = 0
    invalid: int = 0
    excluded_special: int = 0


def load_feeds(root: Path = ROOT) -> list[dict]:
    feeds = json.loads((root / "sources.json").read_text(encoding="utf-8"))
    if not isinstance(feeds, list) or not feeds:
        raise ValueError("sources.json must contain at least one source")
    names, urls = set(), set()
    for feed in feeds:
        name, url = feed["name"], feed["url"]
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name) or name == 'combined':
            raise ValueError(f"Invalid source name: {name}")
        if name in names or url in urls or not url.startswith("https://"):
            raise ValueError(f"Duplicate name/URL or non-HTTPS source: {name}")
        if feed.get("parser", "first_field") not in ("first_field", "csv", "spamhaus_json"):
            raise ValueError(f"Unknown parser: {name}")
        if not isinstance(feed["minimum_entries"], int) or feed["minimum_entries"] < 1:
            raise ValueError(f"Invalid minimum_entries: {name}")
        allowed = set(feed.get("allowed_special", []))
        if not allowed.issubset({str(n) for n in SPECIAL}):
            raise ValueError(f"Exception is not an exact special-use prefix: {name}")
        if not 0 < feed.get('max_churn_ratio', 0.8) <= 1:
            raise ValueError(f"Invalid churn limit: {name}")
        if feed.get('freshness'):
            policy = feed['freshness']
            if policy['type'] not in ('iso_comment', 'firehol', 'spamhaus_json') or policy['max_age_hours'] <= 0:
                raise ValueError(f"Invalid freshness policy: {name}")
        names.add(name)
        urls.add(url)
    return feeds


def download(url: str, timeout: float = 30, retries: int = 1) -> str:
    for attempt in range(retries + 1):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "skynet-filter-list/3.0"})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                if not response.url.startswith("https://"):
                    raise ValueError("Refusing HTTPS downgrade")
                content = response.read(MAX_SOURCE_BYTES + 1)
            if len(content) > MAX_SOURCE_BYTES:
                raise ValueError("Source exceeds 64 MiB")
            return content.decode("utf-8-sig", errors="strict")
        except Exception:
            if attempt == retries:
                raise
            time.sleep(1)
    raise AssertionError("unreachable")


def parse(body: str, feed: dict, *, published: bool = False) -> Parsed:
    result = Parsed(set())
    if not published and feed.get('parser') == 'spamhaus_json':
        rows = [json.loads(line) for line in body.splitlines() if line.strip()]
        if any('cidr' not in row and row.get('type') != 'metadata' for row in rows):
            raise ValueError('Invalid Spamhaus row')
        body = '\n'.join(row['cidr'] for row in rows if 'cidr' in row)
    is_csv = not published and feed.get("parser") == "csv"
    rows = csv.reader(io.StringIO(body)) if is_csv else ([s] for s in body.splitlines())
    allowed = set(feed.get("allowed_special", []))
    for index, row in enumerate(rows):
        if not row or not row[0].strip() or row[0].lstrip().startswith(("#", ";", "!")):
            continue
        token = row[0].strip() if is_csv else row[0].split()[0]
        if is_csv and index == 0 and token.lower() in ("ip", "ip_address", "ip address"):
            continue
        try:
            network = ipaddress.ip_network(token, strict=False)
        except ValueError:
            result.invalid += 1
            continue
        if network.version == 6:
            result.ipv6 += 1
            continue
        # Check before filtering special ranges; never silently discard a /0.
        if str(network) not in allowed and network.prefixlen < 12:
            raise ValueError(f"Dangerously broad network: {network}")
        start, end = int(network.network_address), int(network.broadcast_address)
        if str(network) not in allowed and any(start <= hi and end >= lo for lo, hi in SPECIAL_BOUNDS):
            result.excluded_special += 1
            continue
        result.networks.add(network)
    if result.invalid:
        raise ValueError(f"{result.invalid} invalid non-comment rows")
    if published and (result.ipv6 or result.excluded_special):
        raise ValueError("Published file contains IPv6 or unapproved special-use entries")
    if not published and result.ipv6 and not feed.get("allow_ipv6", False):
        raise ValueError(f"Unexpected IPv6 entries: {result.ipv6}")
    if result.excluded_special > max(1, len(result.networks) * 0.01):
        raise ValueError(f"Too many special-use entries: {result.excluded_special}")
    if len(result.networks) < feed["minimum_entries"]:
        raise ValueError(f"Only {len(result.networks)} IPv4 entries; minimum {feed['minimum_entries']}")
    return result


def metrics(networks: set[ipaddress.IPv4Network], feed: dict) -> dict:
    # Intentional bogons must not hide an increase in public coverage.
    allowed = set(feed.get("allowed_special", []))
    public = (n for n in networks if str(n) not in allowed)
    return {
        "entries": len(networks),
        "public_addresses": sum(n.num_addresses for n in ipaddress.collapse_addresses(public)),
    }


def check_change(current: dict, previous: dict) -> None:
    for key in ("entries", "public_addresses"):
        old, new = previous[key], current[key]
        if old and (new < old * 0.5 or new > old * 2):
            raise ValueError(f"Anomalous {key}: {old} -> {new} (allowed 0.5x to 2x)")


def serialize(networks: set[ipaddress.IPv4Network]) -> str:
    ordered = sorted(networks, key=lambda n: (int(n.network_address), n.prefixlen))
    return "".join(f"{n.network_address if n.prefixlen == 32 else n}\n" for n in ordered)


def snapshot_body(networks, record):
    return ''.join('# ' + line + '\n' for line in record.get('attribution', [])) + serialize(networks)


def digest(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def atomic_write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    try:
        temp.write_text(body, encoding="utf-8", newline="\n")
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)
