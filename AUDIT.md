# Current feed audit

Automatically generated; historical notes are in `AUDIT-HISTORY.md`.

- Checked at: 2026-09-28T11:32:56+00:00
- Configured sources: 23
- Contributing sources: 20
- Combined IPv4/CIDR entries: 97192
- Active / expired exceptions: 0 / 0
- Maximum fallback age: 72 hours

Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.
Last success means successful retrieval and validation, not an upstream observation date.

| Source | State | Included | Entries | Provider timestamp | Last success |
|---|---|---|---:|---|---|
| [greensnow](https://blocklist.greensnow.co/greensnow.txt) | ok | True | 4650 | unknown | 2026-09-28T11:32:56+00:00 |
| [binarydefense](https://www.binarydefense.com/banlist.txt) | ok | True | 382 | unknown | 2026-09-28T11:32:56+00:00 |
| [cins-army](https://cinsscore.com/list/ci-badguys.txt) | ok | True | 15000 | unknown | 2026-09-28T11:32:56+00:00 |
| [firehol-cybercrime](https://iplists.firehol.org/files/cybercrime.ipset) | ok | True | 469 | 2026-09-27T10:16:54+00:00 | 2026-09-28T11:32:56+00:00 |
| [firehol-dshield-1d](https://iplists.firehol.org/files/dshield_1d.netset) | ok | False | 30 | 2026-09-28T00:59:40+00:00 | 2026-09-28T11:32:56+00:00 |
| [firehol-et-block](https://iplists.firehol.org/files/et_block.netset) | ok | True | 1632 | 2026-09-25T04:30:01+00:00 | 2026-09-28T11:32:56+00:00 |
| [firehol-et-compromised](https://iplists.firehol.org/files/et_compromised.ipset) | ok | True | 669 | 2026-09-25T20:00:49+00:00 | 2026-09-28T11:32:56+00:00 |
| [firehol-level1](https://iplists.firehol.org/files/firehol_level1.netset) | ok | True | 4679 | 2026-09-28T03:59:47+00:00 | 2026-09-28T11:32:56+00:00 |
| [firehol-level2](https://iplists.firehol.org/files/firehol_level2.netset) | ok | True | 23495 | 2026-09-28T07:21:11+00:00 | 2026-09-28T11:32:56+00:00 |
| [firehol-level3](https://iplists.firehol.org/files/firehol_level3.netset) | ok | True | 12691 | 2026-09-28T07:04:01+00:00 | 2026-09-28T11:32:56+00:00 |
| [firehol-webserver](https://iplists.firehol.org/files/firehol_webserver.netset) | ok | True | 1505 | 2026-09-27T10:01:01+00:00 | 2026-09-28T11:32:56+00:00 |
| [firehol-myip](https://iplists.firehol.org/files/myip.ipset) | ok | False | 1927 | 2026-09-27T10:01:01+00:00 | 2026-09-28T11:32:56+00:00 |
| [spamhaus-drop](https://www.spamhaus.org/drop/drop_v4.json) | ok | True | 1693 | 2026-09-28T10:14:02+00:00 | 2026-09-28T11:32:56+00:00 |
| [blocklist-de-strongips](https://lists.blocklist.de/lists/strongips.txt) | ok | True | 383 | unknown | 2026-09-28T11:32:56+00:00 |
| [myip-ms-latest-blacklist](https://myip.ms/files/blacklist/general/latest_blacklist.txt) | ok | True | 1920 | unknown | 2026-09-28T11:32:56+00:00 |
| [ipsum-level2](https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt) | ok | True | 33544 | unknown | 2026-09-28T11:32:56+00:00 |
| [interserver-iprbl](https://sigs.interserver.net/iprbl.txt) | ok | True | 4696 | unknown | 2026-09-28T11:32:56+00:00 |
| [blocklist-de-export-ips-all](https://www.blocklist.de/downloads/export-ips_all.txt) | ok | True | 29936 | unknown | 2026-09-28T11:32:56+00:00 |
| [abuseipdb-s100-7d](https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-7d.ipv4) | ok | True | 74863 | 2026-09-28T11:10:38+00:00 | 2026-09-28T11:32:56+00:00 |
| [drb-ra-IPC2s-30day](https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv) | ok | True | 266 | unknown | 2026-09-28T11:32:56+00:00 |
| [hagezi-tif](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt) | ok | True | 34510 | unknown | 2026-09-28T11:32:56+00:00 |
| [threatfox-ipport](https://threatfox.abuse.ch/export/csv/ip-port/recent/) | ok | True | 2271 | 2026-09-28T11:05:05+00:00 | 2026-09-28T11:32:56+00:00 |
| [threatview-high-confidence](https://threatview.io/Downloads/IP-High-Confidence-Feed.txt) | disabled | False | 0 | unknown | never |

## Automatic redundancy observation

| Candidate | Zero-contribution days | Additional addresses | Suppressed |
|---|---:|---:|---|
| cins-army | 0 | 1060 | False |
| firehol-dshield-1d | 19 | 0 | True |
| firehol-et-block | 10 | 0 | False |
| firehol-myip | 19 | 0 | True |
| threatview-high-confidence | 0 | 0 | False |

Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.
A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.
Provider timestamps describe the supplied file, not necessarily each underlying threat observation.
Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.
