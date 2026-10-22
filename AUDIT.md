# Current feed audit

Automatically generated; historical notes are in `AUDIT-HISTORY.md`.

- Checked at: 2026-10-22T08:33:19+00:00
- Configured sources: 24
- Contributing sources: 22
- Combined IPv4/CIDR entries: 283598
- Active / expired exceptions: 0 / 0
- Maximum fallback age: 72 hours
- Protected networks: 10 static + GitHub meta ok (68 ranges, last success 2026-10-22T08:33:19+00:00)
- Removed by protection: 6 addresses (firehol-level3: 6, firehol-myip: 1, firehol-webserver: 1, myip-ms-latest-blacklist: 1)

Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.
Last success means successful retrieval and validation, not an upstream observation date.

| Source | State | Included | Entries | Provider timestamp | Last success |
|---|---|---|---:|---|---|
| [greensnow](https://blocklist.greensnow.co/greensnow.txt) | ok | True | 5399 | unknown | 2026-10-22T08:33:19+00:00 |
| [binarydefense](https://www.binarydefense.com/banlist.txt) | ok | True | 414 | unknown | 2026-10-22T08:33:19+00:00 |
| [firehol-blocklist-net-ua](https://iplists.firehol.org/files/blocklist_net_ua.ipset) | ok | True | 227201 | unknown | 2026-10-22T08:33:19+00:00 |
| [cins-army](https://cinsscore.com/list/ci-badguys.txt) | ok | True | 15000 | unknown | 2026-10-22T08:33:19+00:00 |
| [firehol-cybercrime](https://iplists.firehol.org/files/cybercrime.ipset) | ok | True | 493 | 2026-10-21T15:42:01+00:00 | 2026-10-22T08:33:19+00:00 |
| [firehol-dshield-1d](https://iplists.firehol.org/files/dshield_1d.netset) | ok | False | 34 | 2026-10-22T03:45:04+00:00 | 2026-10-22T08:33:19+00:00 |
| [firehol-et-block](https://iplists.firehol.org/files/et_block.netset) | ok | True | 1615 | 2026-10-21T04:30:01+00:00 | 2026-10-22T08:33:19+00:00 |
| [firehol-et-compromised](https://iplists.firehol.org/files/et_compromised.ipset) | ok | True | 477 | 2026-10-21T20:24:08+00:00 | 2026-10-22T08:33:19+00:00 |
| [firehol-level1](https://iplists.firehol.org/files/firehol_level1.netset) | ok | True | 4638 | 2026-10-22T03:45:04+00:00 | 2026-10-22T08:33:19+00:00 |
| [firehol-level2](https://iplists.firehol.org/files/firehol_level2.netset) | ok | True | 21677 | 2026-10-22T04:08:45+00:00 | 2026-10-22T08:33:19+00:00 |
| [firehol-level3](https://iplists.firehol.org/files/firehol_level3.netset) | ok | True | 10203 | 2026-10-22T04:06:55+00:00 | 2026-10-22T08:33:19+00:00 |
| [firehol-webserver](https://iplists.firehol.org/files/firehol_webserver.netset) | ok | True | 1463 | 2026-10-21T18:30:50+00:00 | 2026-10-22T08:33:19+00:00 |
| [firehol-myip](https://iplists.firehol.org/files/myip.ipset) | ok | False | 1593 | 2026-10-21T18:30:50+00:00 | 2026-10-22T08:33:19+00:00 |
| [spamhaus-drop](https://www.spamhaus.org/drop/drop_v4.json) | ok | True | 1687 | 2026-10-21T14:14:02+00:00 | 2026-10-22T08:33:19+00:00 |
| [blocklist-de-strongips](https://lists.blocklist.de/lists/strongips.txt) | ok | True | 278 | unknown | 2026-10-22T08:33:19+00:00 |
| [myip-ms-latest-blacklist](https://myip.ms/files/blacklist/general/latest_blacklist.txt) | ok | True | 1590 | unknown | 2026-10-22T08:33:19+00:00 |
| [ipsum-level2](https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt) | ok | True | 36348 | unknown | 2026-10-22T08:33:19+00:00 |
| [interserver-iprbl](https://sigs.interserver.net/iprbl.txt) | ok | True | 4983 | unknown | 2026-10-22T08:33:19+00:00 |
| [blocklist-de-export-ips-all](https://www.blocklist.de/downloads/export-ips_all.txt) | ok | True | 27871 | unknown | 2026-10-22T08:33:19+00:00 |
| [abuseipdb-s100-30d](https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-30d.ipv4) | ok | True | 128687 | 2026-10-22T08:14:10+00:00 | 2026-10-22T08:33:19+00:00 |
| [drb-ra-IPC2s-30day](https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv) | ok | True | 222 | unknown | 2026-10-22T08:33:19+00:00 |
| [hagezi-tif](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt) | ok | True | 37331 | unknown | 2026-10-22T08:33:19+00:00 |
| [threatfox-ipport](https://threatfox.abuse.ch/export/csv/ip-port/recent/) | stale | True | 2465 | 2026-10-21T08:18:41+00:00 | 2026-10-21T08:30:56+00:00 |
| [threatview-high-confidence](https://threatview.io/Downloads/IP-High-Confidence-Feed.txt) | ok | True | 19216 | unknown | 2026-10-22T08:33:19+00:00 |

## Automatic redundancy observation

| Candidate | Zero-contribution days | Additional addresses | Suppressed |
|---|---:|---:|---|
| cins-army | 0 | 1024 | False |
| firehol-dshield-1d | 22 | 0 | True |
| firehol-et-block | 1 | 0 | False |
| firehol-myip | 22 | 0 | True |
| threatview-high-confidence | 0 | 2614 | False |

Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.
A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.
Provider timestamps describe the supplied file, not necessarily each underlying threat observation.
Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.
