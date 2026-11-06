# Current feed audit

Automatically generated; historical notes are in `AUDIT-HISTORY.md`.

- Checked at: 2026-11-06T10:48:22+00:00
- Configured sources: 23
- Contributing sources: 21
- Combined IPv4/CIDR entries: 287195
- Active / expired exceptions: 0 / 0
- Maximum fallback age: 72 hours
- Protected networks: 10 static + GitHub meta ok (68 ranges, last success 2026-11-06T10:48:22+00:00)
- Removed by protection: 5 addresses (firehol-level3: 5)

Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.
Last success means successful retrieval and validation, not an upstream observation date.

| Source | State | Included | Entries | Provider timestamp | Last success |
|---|---|---|---:|---|---|
| [greensnow](https://blocklist.greensnow.co/greensnow.txt) | ok | True | 3667 | unknown | 2026-11-06T10:48:22+00:00 |
| [binarydefense](https://www.binarydefense.com/banlist.txt) | ok | True | 993 | unknown | 2026-11-06T10:48:22+00:00 |
| [firehol-blocklist-net-ua](https://iplists.firehol.org/files/blocklist_net_ua.ipset) | ok | True | 219858 | unknown | 2026-11-06T10:48:22+00:00 |
| [cins-army](https://cinsscore.com/list/ci-badguys.txt) | ok | True | 15000 | unknown | 2026-11-06T10:48:22+00:00 |
| [firehol-cybercrime](https://iplists.firehol.org/files/cybercrime.ipset) | ok | True | 513 | 2026-11-04T18:02:29+00:00 | 2026-11-06T10:48:22+00:00 |
| [firehol-dshield-1d](https://iplists.firehol.org/files/dshield_1d.netset) | ok | False | 32 | 2026-11-06T03:44:40+00:00 | 2026-11-06T10:48:22+00:00 |
| [firehol-et-block](https://iplists.firehol.org/files/et_block.netset) | ok | True | 1645 | 2026-11-05T05:30:01+00:00 | 2026-11-06T10:48:22+00:00 |
| [firehol-et-compromised](https://iplists.firehol.org/files/et_compromised.ipset) | ok | True | 511 | 2026-11-05T21:37:44+00:00 | 2026-11-06T10:48:22+00:00 |
| [firehol-level1](https://iplists.firehol.org/files/firehol_level1.netset) | ok | True | 4650 | 2026-11-06T03:44:40+00:00 | 2026-11-06T10:48:22+00:00 |
| [firehol-level2](https://iplists.firehol.org/files/firehol_level2.netset) | ok | True | 18464 | 2026-11-06T04:41:25+00:00 | 2026-11-06T10:48:22+00:00 |
| [firehol-level3](https://iplists.firehol.org/files/firehol_level3.netset) | ok | True | 12068 | 2026-11-06T04:39:07+00:00 | 2026-11-06T10:48:22+00:00 |
| [firehol-webserver](https://iplists.firehol.org/files/firehol_webserver.netset) | ok | True | 1191 | 2026-11-05T12:30:50+00:00 | 2026-11-06T10:48:22+00:00 |
| [firehol-myip](https://iplists.firehol.org/files/myip.ipset) | ok | False | 1321 | 2026-11-05T12:30:50+00:00 | 2026-11-06T10:48:22+00:00 |
| [spamhaus-drop](https://www.spamhaus.org/drop/drop_v4.json) | ok | True | 1762 | 2026-11-05T16:44:02+00:00 | 2026-11-06T10:48:22+00:00 |
| [blocklist-de-strongips](https://lists.blocklist.de/lists/strongips.txt) | ok | True | 299 | unknown | 2026-11-06T10:48:22+00:00 |
| [myip-ms-latest-blacklist](https://myip.ms/files/blacklist/general/latest_blacklist.txt) | ok | True | 1279 | unknown | 2026-11-06T10:48:22+00:00 |
| [ipsum-level2](https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt) | ok | True | 35261 | unknown | 2026-11-06T10:48:22+00:00 |
| [interserver-iprbl](https://sigs.interserver.net/iprbl.txt) | ok | True | 4428 | unknown | 2026-11-06T10:48:22+00:00 |
| [blocklist-de-export-ips-all](https://www.blocklist.de/downloads/export-ips_all.txt) | ok | True | 26140 | unknown | 2026-11-06T10:48:22+00:00 |
| [abuseipdb-s100-30d](https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-30d.ipv4) | ok | True | 132872 | 2026-11-06T10:33:39+00:00 | 2026-11-06T10:48:22+00:00 |
| [drb-ra-IPC2s-30day](https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv) | ok | True | 212 | unknown | 2026-11-06T10:48:22+00:00 |
| [hagezi-tif](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt) | ok | True | 36184 | unknown | 2026-11-06T10:48:22+00:00 |
| [threatview-high-confidence](https://threatview.io/Downloads/IP-High-Confidence-Feed.txt) | ok | True | 17736 | unknown | 2026-11-06T10:48:22+00:00 |

## Automatic redundancy observation

| Candidate | Zero-contribution days | Additional addresses | Suppressed |
|---|---:|---:|---|
| cins-army | 0 | 992 | False |
| firehol-dshield-1d | 37 | 0 | True |
| firehol-et-block | 1 | 0 | False |
| firehol-myip | 37 | 0 | True |
| threatview-high-confidence | 0 | 3151 | False |

Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.
A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.
Provider timestamps describe the supplied file, not necessarily each underlying threat observation.
Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.
