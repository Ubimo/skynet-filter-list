# Current feed audit

Automatically generated; historical notes are in `AUDIT-HISTORY.md`.

- Checked at: 2026-11-28T11:40:07+00:00
- Configured sources: 21
- Contributing sources: 20
- Combined IPv4/CIDR entries: 280663
- Active / expired exceptions: 0 / 0
- Maximum fallback age: 72 hours
- Protected networks: 10 static + GitHub meta ok (112 ranges, last success 2026-11-28T11:40:07+00:00)
- Removed by protection: 6 addresses (abuseipdb-s100-30d: 1, firehol-level3: 5)

Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.
Last success means successful retrieval and validation, not an upstream observation date.

| Source | State | Included | Entries | Provider timestamp | Last success |
|---|---|---|---:|---|---|
| [greensnow](https://blocklist.greensnow.co/greensnow.txt) | ok | True | 1700 | unknown | 2026-11-28T11:40:07+00:00 |
| [binarydefense](https://www.binarydefense.com/banlist.txt) | ok | True | 1283 | unknown | 2026-11-28T11:40:07+00:00 |
| [firehol-blocklist-net-ua](https://iplists.firehol.org/files/blocklist_net_ua.ipset) | ok | True | 193387 | unknown | 2026-11-28T11:40:07+00:00 |
| [cins-army](https://cinsscore.com/list/ci-badguys.txt) | ok | True | 15000 | unknown | 2026-11-28T11:40:07+00:00 |
| [firehol-cybercrime](https://iplists.firehol.org/files/cybercrime.ipset) | ok | True | 540 | 2026-11-28T02:09:06+00:00 | 2026-11-28T11:40:07+00:00 |
| [firehol-dshield-1d](https://iplists.firehol.org/files/dshield_1d.netset) | ok | False | 35 | 2026-11-28T05:44:44+00:00 | 2026-11-28T11:40:07+00:00 |
| [firehol-et-block](https://iplists.firehol.org/files/et_block.netset) | ok | True | 1627 | 2026-11-27T05:30:02+00:00 | 2026-11-28T11:40:07+00:00 |
| [firehol-et-compromised](https://iplists.firehol.org/files/et_compromised.ipset) | ok | True | 577 | 2026-11-27T21:25:38+00:00 | 2026-11-28T11:40:07+00:00 |
| [firehol-level1](https://iplists.firehol.org/files/firehol_level1.netset) | ok | True | 4610 | 2026-11-28T05:44:44+00:00 | 2026-11-28T11:40:07+00:00 |
| [firehol-level2](https://iplists.firehol.org/files/firehol_level2.netset) | ok | True | 17635 | 2026-11-28T06:52:41+00:00 | 2026-11-28T11:40:07+00:00 |
| [firehol-level3](https://iplists.firehol.org/files/firehol_level3.netset) | ok | True | 13148 | 2026-11-28T06:04:01+00:00 | 2026-11-28T11:40:07+00:00 |
| [spamhaus-drop](https://www.spamhaus.org/drop/drop_v4.json) | ok | True | 1736 | 2026-11-28T11:26:44+00:00 | 2026-11-28T11:40:07+00:00 |
| [blocklist-de-strongips](https://lists.blocklist.de/lists/strongips.txt) | ok | True | 279 | unknown | 2026-11-28T11:40:07+00:00 |
| [ipsum-level2](https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt) | ok | True | 39712 | unknown | 2026-11-28T11:40:07+00:00 |
| [interserver-iprbl](https://sigs.interserver.net/iprbl.txt) | ok | True | 2507 | unknown | 2026-11-28T11:40:07+00:00 |
| [blocklist-de-export-ips-all](https://www.blocklist.de/downloads/export-ips_all.txt) | ok | True | 24707 | unknown | 2026-11-28T11:40:07+00:00 |
| [abuseipdb-s100-30d](https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-30d.ipv4) | ok | True | 162706 | 2026-11-28T11:33:21+00:00 | 2026-11-28T11:40:07+00:00 |
| [drb-ra-IPC2s-30day](https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv) | ok | True | 212 | unknown | 2026-11-28T11:40:07+00:00 |
| [hagezi-tif](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt) | ok | True | 35624 | unknown | 2026-11-28T11:40:07+00:00 |
| [threatfox-ipport](https://threatfox-api.abuse.ch/api/v1/) | ok | True | 8383 | unknown | 2026-11-28T11:40:07+00:00 |
| [threatview-high-confidence](https://threatview.io/Downloads/IP-High-Confidence-Feed.txt) | ok | True | 16362 | unknown | 2026-11-28T11:40:07+00:00 |

## Automatic redundancy observation

| Candidate | Zero-contribution days | Additional addresses | Suppressed |
|---|---:|---:|---|
| cins-army | 0 | 709 | False |
| firehol-dshield-1d | 59 | 0 | True |
| firehol-et-block | 3 | 0 | False |
| threatview-high-confidence | 0 | 2133 | False |

Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.
A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.
Provider timestamps describe the supplied file, not necessarily each underlying threat observation.
Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.
