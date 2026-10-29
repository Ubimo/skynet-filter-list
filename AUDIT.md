# Current feed audit

Automatically generated; historical notes are in `AUDIT-HISTORY.md`.

- Checked at: 2026-10-29T09:54:18+00:00
- Configured sources: 23
- Contributing sources: 21
- Combined IPv4/CIDR entries: 286544
- Active / expired exceptions: 0 / 0
- Maximum fallback age: 72 hours
- Protected networks: 10 static + GitHub meta ok (68 ranges, last success 2026-10-29T09:54:18+00:00)
- Removed by protection: 5 addresses (firehol-level3: 5)

Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.
Last success means successful retrieval and validation, not an upstream observation date.

| Source | State | Included | Entries | Provider timestamp | Last success |
|---|---|---|---:|---|---|
| [greensnow](https://blocklist.greensnow.co/greensnow.txt) | ok | True | 4661 | unknown | 2026-10-29T09:54:18+00:00 |
| [binarydefense](https://www.binarydefense.com/banlist.txt) | ok | True | 430 | unknown | 2026-10-29T09:54:18+00:00 |
| [firehol-blocklist-net-ua](https://iplists.firehol.org/files/blocklist_net_ua.ipset) | ok | True | 224704 | unknown | 2026-10-29T09:54:18+00:00 |
| [cins-army](https://cinsscore.com/list/ci-badguys.txt) | ok | True | 15000 | unknown | 2026-10-29T09:54:18+00:00 |
| [firehol-cybercrime](https://iplists.firehol.org/files/cybercrime.ipset) | ok | True | 504 | 2026-10-26T00:08:57+00:00 | 2026-10-29T09:54:18+00:00 |
| [firehol-dshield-1d](https://iplists.firehol.org/files/dshield_1d.netset) | ok | False | 36 | 2026-10-28T22:44:22+00:00 | 2026-10-29T09:54:18+00:00 |
| [firehol-et-block](https://iplists.firehol.org/files/et_block.netset) | ok | True | 1616 | 2026-10-27T04:30:01+00:00 | 2026-10-29T09:54:18+00:00 |
| [firehol-et-compromised](https://iplists.firehol.org/files/et_compromised.ipset) | ok | True | 524 | 2026-10-28T20:29:55+00:00 | 2026-10-29T09:54:18+00:00 |
| [firehol-level1](https://iplists.firehol.org/files/firehol_level1.netset) | ok | True | 4658 | 2026-10-29T01:44:27+00:00 | 2026-10-29T09:54:18+00:00 |
| [firehol-level2](https://iplists.firehol.org/files/firehol_level2.netset) | ok | True | 19810 | 2026-10-29T05:13:26+00:00 | 2026-10-29T09:54:18+00:00 |
| [firehol-level3](https://iplists.firehol.org/files/firehol_level3.netset) | ok | True | 10015 | 2026-10-29T05:04:01+00:00 | 2026-10-29T09:54:18+00:00 |
| [firehol-webserver](https://iplists.firehol.org/files/firehol_webserver.netset) | ok | True | 1566 | 2026-10-28T05:00:50+00:00 | 2026-10-29T09:54:18+00:00 |
| [firehol-myip](https://iplists.firehol.org/files/myip.ipset) | ok | False | 1649 | 2026-10-29T05:01:08+00:00 | 2026-10-29T09:54:18+00:00 |
| [spamhaus-drop](https://www.spamhaus.org/drop/drop_v4.json) | ok | True | 1759 | 2026-10-29T09:14:02+00:00 | 2026-10-29T09:54:18+00:00 |
| [blocklist-de-strongips](https://lists.blocklist.de/lists/strongips.txt) | ok | True | 291 | unknown | 2026-10-29T09:54:18+00:00 |
| [myip-ms-latest-blacklist](https://myip.ms/files/blacklist/general/latest_blacklist.txt) | ok | True | 1655 | unknown | 2026-10-29T09:54:18+00:00 |
| [ipsum-level2](https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt) | ok | True | 38101 | unknown | 2026-10-29T09:54:18+00:00 |
| [interserver-iprbl](https://sigs.interserver.net/iprbl.txt) | ok | True | 5145 | unknown | 2026-10-29T09:54:18+00:00 |
| [blocklist-de-export-ips-all](https://www.blocklist.de/downloads/export-ips_all.txt) | ok | True | 26777 | unknown | 2026-10-29T09:54:18+00:00 |
| [abuseipdb-s100-30d](https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-30d.ipv4) | ok | True | 130447 | 2026-10-29T09:34:00+00:00 | 2026-10-29T09:54:18+00:00 |
| [drb-ra-IPC2s-30day](https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv) | ok | True | 208 | unknown | 2026-10-29T09:54:18+00:00 |
| [hagezi-tif](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt) | ok | True | 37266 | unknown | 2026-10-29T09:54:18+00:00 |
| [threatview-high-confidence](https://threatview.io/Downloads/IP-High-Confidence-Feed.txt) | ok | True | 20437 | unknown | 2026-10-29T09:54:18+00:00 |

## Automatic redundancy observation

| Candidate | Zero-contribution days | Additional addresses | Suppressed |
|---|---:|---:|---|
| cins-army | 0 | 822 | False |
| firehol-dshield-1d | 29 | 0 | True |
| firehol-et-block | 8 | 0 | False |
| firehol-myip | 29 | 0 | True |
| threatview-high-confidence | 0 | 3883 | False |

Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.
A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.
Provider timestamps describe the supplied file, not necessarily each underlying threat observation.
Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.
