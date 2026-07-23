from __future__ import annotations

import ipaddress
from pathlib import Path
import sys
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from update_ipv4_feeds import (  # noqa: E402
    format_network,
    parse_csv_first_column,
    parse_first_field,
)


class IPv4FeedTests(unittest.TestCase):
    def test_generated_feeds_contain_only_ipv4(self) -> None:
        for path in (REPOSITORY_ROOT / "generated").glob("*.ipv4"):
            with self.subTest(path=path.name):
                entries = [
                    line.strip()
                    for line in path.read_text(encoding="utf-8").splitlines()
                    if line.strip()
                ]
                self.assertTrue(entries)
                for entry in entries:
                    self.assertIsInstance(
                        ipaddress.ip_network(entry, strict=False),
                        ipaddress.IPv4Network,
                    )

    def test_first_field_parser_excludes_ipv6(self) -> None:
        body = "\n".join(
            (
                "# comment",
                "192.0.2.1 metadata",
                "198.51.100.7/24",
                "2001:db8::1",
                "not-an-address",
            )
        )

        networks, ignored_ipv6 = parse_first_field(body)

        self.assertEqual(
            networks,
            {
                ipaddress.ip_network("192.0.2.1"),
                ipaddress.ip_network("198.51.100.0/24"),
            },
        )
        self.assertEqual(ignored_ipv6, 1)

    def test_csv_parser_excludes_ipv6_and_deduplicates(self) -> None:
        body = "\n".join(
            (
                "ip,description",
                "203.0.113.9,first",
                "203.0.113.9,duplicate",
                "2001:db8::9,IPv6",
            )
        )

        networks, ignored_ipv6 = parse_csv_first_column(body)

        self.assertEqual(networks, {ipaddress.ip_network("203.0.113.9")})
        self.assertEqual(ignored_ipv6, 1)

    def test_host_prefix_is_written_as_an_address(self) -> None:
        self.assertEqual(
            format_network(ipaddress.ip_network("192.0.2.1")),
            "192.0.2.1",
        )
        self.assertEqual(
            format_network(ipaddress.ip_network("198.51.100.0/24")),
            "198.51.100.0/24",
        )


if __name__ == "__main__":
    unittest.main()
