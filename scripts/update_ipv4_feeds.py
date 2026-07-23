from __future__ import annotations

import csv
from dataclasses import dataclass
import io
import ipaddress
from pathlib import Path
from typing import Callable, Iterable
import urllib.request


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "skynet-filter-list-updater/2.0"
MAX_SOURCE_BYTES = 64 * 1024 * 1024


@dataclass(frozen=True)
class Feed:
    source_url: str
    output_file: Path
    parser: Callable[
        [str],
        tuple[set[ipaddress.IPv4Network], int],
    ]
    minimum_ipv4_entries: int


def parse_first_field(
    body: str,
) -> tuple[set[ipaddress.IPv4Network], int]:
    networks: set[ipaddress.IPv4Network] = set()
    ignored_ipv6 = 0
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", ";", "!")):
            continue
        first_field = stripped.split(maxsplit=1)[0]
        try:
            network = ipaddress.ip_network(first_field, strict=False)
        except ValueError:
            continue
        if isinstance(network, ipaddress.IPv4Network):
            networks.add(network)
        else:
            ignored_ipv6 += 1
    return networks, ignored_ipv6


def parse_csv_first_column(
    body: str,
) -> tuple[set[ipaddress.IPv4Network], int]:
    networks: set[ipaddress.IPv4Network] = set()
    ignored_ipv6 = 0
    for row in csv.reader(io.StringIO(body)):
        if not row:
            continue
        try:
            network = ipaddress.ip_network(row[0].strip(), strict=False)
        except ValueError:
            continue
        if isinstance(network, ipaddress.IPv4Network):
            networks.add(network)
        else:
            ignored_ipv6 += 1
    return networks, ignored_ipv6


FEEDS = (
    Feed(
        source_url=(
            "https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/"
            "master/feeds/IPC2s-30day.csv"
        ),
        output_file=(
            REPOSITORY_ROOT
            / "generated"
            / "drb-ra-IPC2s-30day.ipv4"
        ),
        parser=parse_csv_first_column,
        minimum_ipv4_entries=10,
    ),
    Feed(
        source_url=(
            "https://myip.ms/files/blacklist/general/"
            "latest_blacklist.txt"
        ),
        output_file=(
            REPOSITORY_ROOT
            / "generated"
            / "myip-ms-latest-blacklist.ipv4"
        ),
        parser=parse_first_field,
        minimum_ipv4_entries=100,
    ),
    Feed(
        source_url=(
            "https://www.blocklist.de/downloads/export-ips_all.txt"
        ),
        output_file=(
            REPOSITORY_ROOT
            / "generated"
            / "blocklist-de-export-ips-all.ipv4"
        ),
        parser=parse_first_field,
        minimum_ipv4_entries=1_000,
    ),
)


def download(source_url: str, retries: int = 1) -> str:
    for attempt in range(retries + 1):
        try:
            request = urllib.request.Request(
                source_url,
                headers={"User-Agent": USER_AGENT},
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                content = response.read(MAX_SOURCE_BYTES + 1)
            if len(content) > MAX_SOURCE_BYTES:
                raise ValueError(
                    f"Source exceeds {MAX_SOURCE_BYTES} bytes: {source_url}"
                )
            return content.decode("utf-8-sig", errors="replace")
        except Exception:
            if attempt == retries:
                raise
    raise AssertionError("unreachable")


def sort_networks(
    networks: Iterable[ipaddress.IPv4Network],
) -> list[ipaddress.IPv4Network]:
    return sorted(
        networks,
        key=lambda network: (
            int(network.network_address),
            network.prefixlen,
        ),
    )


def format_network(network: ipaddress.IPv4Network) -> str:
    if network.prefixlen == network.max_prefixlen:
        return str(network.network_address)
    return str(network)


def main() -> None:
    parsed_feeds = []
    for feed in FEEDS:
        body = download(feed.source_url)
        networks, ignored_ipv6 = feed.parser(body)
        if len(networks) < feed.minimum_ipv4_entries:
            raise RuntimeError(
                f"Refusing to replace {feed.output_file.name}: only "
                f"{len(networks)} valid IPv4 entries"
            )
        parsed_feeds.append((feed, networks, ignored_ipv6))

    for feed, networks, ignored_ipv6 in parsed_feeds:
        feed.output_file.parent.mkdir(parents=True, exist_ok=True)
        feed.output_file.write_text(
            "".join(
                f"{format_network(network)}\n"
                for network in sort_networks(networks)
            ),
            encoding="utf-8",
            newline="\n",
        )
        print(
            f"Wrote {len(networks)} IPv4 entries to "
            f"{feed.output_file}; excluded {ignored_ipv6} IPv6 entries"
        )


if __name__ == "__main__":
    main()
