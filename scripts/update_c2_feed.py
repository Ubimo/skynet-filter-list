from __future__ import annotations

import csv
import io
import ipaddress
from pathlib import Path
import urllib.request


SOURCE_URL = (
    "https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/"
    "master/feeds/IPC2s-30day.csv"
)
OUTPUT_FILE = (
    Path(__file__).resolve().parents[1]
    / "generated"
    / "drb-ra-IPC2s-30day.ipv4"
)


def main() -> None:
    request = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "skynet-filter-list-updater/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8-sig")

    addresses: set[ipaddress.IPv4Address] = set()
    for row in csv.reader(io.StringIO(body)):
        if not row:
            continue
        try:
            address = ipaddress.ip_address(row[0].strip())
        except ValueError:
            continue
        if isinstance(address, ipaddress.IPv4Address):
            addresses.add(address)

    if len(addresses) < 10:
        raise RuntimeError(
            f"Refusing to replace feed: only {len(addresses)} valid IPv4 addresses"
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        "".join(f"{address}\n" for address in sorted(addresses)),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {len(addresses)} IPv4 addresses to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
