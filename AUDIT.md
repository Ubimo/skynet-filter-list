# Current feed audit

Automatically generated; historical notes are in `AUDIT-HISTORY.md`.

- Checked at: 2026-10-23T08:29:31+00:00
- Configured sources: 23
- Contributing sources: 21
- Combined IPv4/CIDR entries: 284813
- Active / expired exceptions: 0 / 0
- Maximum fallback age: 72 hours
- Protected networks: 10 static + GitHub meta ok (68 ranges, last success 2026-10-23T08:29:31+00:00)
- Removed by protection: 6 addresses (firehol-level3: 6, firehol-myip: 1, firehol-webserver: 1, myip-ms-latest-blacklist: 1)

Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.
Last success means successful retrieval and validation, not an upstream observation date.

| Source | State | Included | Entries | Provider timestamp | Last success |
|---|---|---|---:|---|---|
| [greensnow](https://blocklist.greensnow.co/greensnow.txt) | ok | True | 5469 | unknown | 2026-10-23T08:29:31+00:00 |
| [binarydefense](https://www.binarydefense.com/banlist.txt) | ok | True | 807 | unknown | 2026-10-23T08:29:31+00:00 |
| [firehol-blocklist-net-ua](https://iplists.firehol.org/files/blocklist_net_ua.ipset) | ok | True | 226684 | unknown | 2026-10-23T08:29:31+00:00 |
| [cins-army](https://cinsscore.com/list/ci-badguys.txt) | ok | True | 15000 | unknown | 2026-10-23T08:29:31+00:00 |
| [firehol-cybercrime](https://iplists.firehol.org/files/cybercrime.ipset) | ok | True | 493 | 2026-10-21T15:42:01+00:00 | 2026-10-23T08:29:31+00:00 |
| [firehol-dshield-1d](https://iplists.firehol.org/files/dshield_1d.netset) | ok | False | 37 | 2026-10-23T02:44:58+00:00 | 2026-10-23T08:29:31+00:00 |
| [firehol-et-block](https://iplists.firehol.org/files/et_block.netset) | ok | True | 1615 | 2026-10-21T04:30:01+00:00 | 2026-10-23T08:29:31+00:00 |
| [firehol-et-compromised](https://iplists.firehol.org/files/et_compromised.ipset) | ok | True | 470 | 2026-10-22T20:30:44+00:00 | 2026-10-23T08:29:31+00:00 |
| [firehol-level1](https://iplists.firehol.org/files/firehol_level1.netset) | ok | True | 4637 | 2026-10-23T02:44:58+00:00 | 2026-10-23T08:29:31+00:00 |
| [firehol-level2](https://iplists.firehol.org/files/firehol_level2.netset) | ok | True | 22104 | 2026-10-23T03:21:19+00:00 | 2026-10-23T08:29:31+00:00 |
| [firehol-level3](https://iplists.firehol.org/files/firehol_level3.netset) | ok | True | 10139 | 2026-10-23T03:04:01+00:00 | 2026-10-23T08:29:31+00:00 |
| [firehol-webserver](https://iplists.firehol.org/files/firehol_webserver.netset) | ok | True | 1424 | 2026-10-22T21:00:48+00:00 | 2026-10-23T08:29:31+00:00 |
| [firehol-myip](https://iplists.firehol.org/files/myip.ipset) | ok | False | 1554 | 2026-10-22T21:00:48+00:00 | 2026-10-23T08:29:31+00:00 |
| [spamhaus-drop](https://www.spamhaus.org/drop/drop_v4.json) | ok | True | 1687 | 2026-10-22T12:44:02+00:00 | 2026-10-23T08:29:31+00:00 |
| [blocklist-de-strongips](https://lists.blocklist.de/lists/strongips.txt) | ok | True | 279 | unknown | 2026-10-23T08:29:31+00:00 |
| [myip-ms-latest-blacklist](https://myip.ms/files/blacklist/general/latest_blacklist.txt) | ok | True | 1574 | unknown | 2026-10-23T08:29:31+00:00 |
| [ipsum-level2](https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt) | ok | True | 36496 | unknown | 2026-10-23T08:29:31+00:00 |
| [interserver-iprbl](https://sigs.interserver.net/iprbl.txt) | ok | True | 5107 | unknown | 2026-10-23T08:29:31+00:00 |
| [blocklist-de-export-ips-all](https://www.blocklist.de/downloads/export-ips_all.txt) | ok | True | 28382 | unknown | 2026-10-23T08:29:31+00:00 |
| [abuseipdb-s100-30d](https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-30d.ipv4) | ok | True | 128536 | 2026-10-23T08:13:36+00:00 | 2026-10-23T08:29:31+00:00 |
| [drb-ra-IPC2s-30day](https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv) | ok | True | 221 | unknown | 2026-10-23T08:29:31+00:00 |
| [hagezi-tif](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt) | ok | True | 37441 | unknown | 2026-10-23T08:29:31+00:00 |
| [threatview-high-confidence](https://threatview.io/Downloads/IP-High-Confidence-Feed.txt) | ok | True | 19480 | unknown | 2026-10-23T08:29:31+00:00 |

## Automatic redundancy observation

| Candidate | Zero-contribution days | Additional addresses | Suppressed |
|---|---:|---:|---|
| cins-army | 0 | 1057 | False |
| firehol-dshield-1d | 23 | 0 | True |
| firehol-et-block | 2 | 0 | False |
| firehol-myip | 23 | 0 | True |
| threatview-high-confidence | 0 | 2749 | False |

Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.
A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.
Provider timestamps describe the supplied file, not necessarily each underlying threat observation.
Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.
