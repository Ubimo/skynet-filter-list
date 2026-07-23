from __future__ import annotations

import argparse
from concurrent.futures import as_completed, ThreadPoolExecutor
from dataclasses import dataclass
import ipaddress
from pathlib import Path
import urllib.request


USER_AGENT = "skynet-filter-list-audit/1.0"
MAX_SOURCE_BYTES = 64 * 1024 * 1024
REPOSITORY_RAW_PREFIX = (
    "https://raw.githubusercontent.com/Ubimo/skynet-filter-list/main/"
)


@dataclass(frozen=True)
class SourceAudit:
    source: str
    ipv4: int
    ipv6: int
    invalid: int
    error: str | None = None


def read_source(
    source: str,
    repository_root: Path,
    timeout: float,
) -> str:
    if source.startswith(REPOSITORY_RAW_PREFIX):
        resolved_root = repository_root.resolve()
        local_path = (
            resolved_root
            / source.removeprefix(REPOSITORY_RAW_PREFIX)
        ).resolve()
        try:
            local_path.relative_to(resolved_root)
        except ValueError:
            raise ValueError(
                f"Local source path escapes repository: {source}"
            ) from None
        if local_path.is_file():
            return local_path.read_text(
                encoding="utf-8-sig",
                errors="replace",
            )

    request = urllib.request.Request(
        source,
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content = response.read(MAX_SOURCE_BYTES + 1)
    if len(content) > MAX_SOURCE_BYTES:
        raise ValueError(
            f"Source exceeds {MAX_SOURCE_BYTES} bytes: {source}"
        )
    return content.decode("utf-8-sig", errors="replace")


def audit_source(
    source: str,
    repository_root: Path,
    timeout: float,
    retries: int,
) -> SourceAudit:
    for attempt in range(retries + 1):
        try:
            body = read_source(
                source,
                repository_root,
                timeout,
            )
            break
        except Exception as error:
            if attempt == retries:
                return SourceAudit(
                    source=source,
                    ipv4=0,
                    ipv6=0,
                    invalid=0,
                    error=f"{type(error).__name__}: {error}",
                )

    ipv4 = 0
    ipv6 = 0
    invalid = 0
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", ";", "!")):
            continue
        first_field = stripped.split(maxsplit=1)[0]
        try:
            network = ipaddress.ip_network(first_field, strict=False)
        except ValueError:
            invalid += 1
            continue
        if isinstance(network, ipaddress.IPv4Network):
            ipv4 += 1
        else:
            ipv6 += 1

    return SourceAudit(source, ipv4, ipv6, invalid)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "manifest",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "filter.list",
    )
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    sources = [
        line.strip()
        for line in args.manifest.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    repository_root = args.manifest.resolve().parent
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                audit_source,
                source,
                repository_root,
                args.timeout,
                args.retries,
            ): source
            for source in sources
        }
        results = {
            futures[future]: future.result()
            for future in as_completed(futures)
        }
    audits = [results[source] for source in sources]

    print("IPv4\tIPv6\tInvalid\tSource\tError")
    for audit in audits:
        print(
            f"{audit.ipv4}\t{audit.ipv6}\t{audit.invalid}\t"
            f"{audit.source}\t{audit.error or ''}"
        )

    total_ipv4 = sum(audit.ipv4 for audit in audits)
    total_ipv6 = sum(audit.ipv6 for audit in audits)
    print(f"TOTAL\t{total_ipv4}\t{total_ipv6}")
    if any(audit.error for audit in audits):
        raise SystemExit(1)
    if any(audit.ipv4 == 0 for audit in audits):
        raise SystemExit(1)
    if any(audit.invalid for audit in audits):
        raise SystemExit(1)
    if total_ipv6:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
