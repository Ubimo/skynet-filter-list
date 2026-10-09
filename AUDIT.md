# Current feed audit

Automatically generated; historical notes are in `AUDIT-HISTORY.md`.

- Checked at: 2026-10-09T10:29:23+00:00
- Configured sources: 24
- Contributing sources: 24
- Combined IPv4/CIDR entries: 238397
- Active / expired exceptions: 0 / 0
- Maximum fallback age: 72 hours
- Protected networks: 10 static + GitHub meta ok (65 ranges, last success 2026-10-09T10:29:23+00:00)
- Removed by protection: 5 addresses (firehol-level3: 5)

Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.
Last success means successful retrieval and validation, not an upstream observation date.

| Source | State | Included | Entries | Provider timestamp | Last success |
|---|---|---|---:|---|---|
| [greensnow](https://blocklist.greensnow.co/greensnow.txt) | ok | True | 3230 | unknown | 2026-10-09T10:29:23+00:00 |
| [binarydefense](https://www.binarydefense.com/banlist.txt) | ok | True | 2809 | unknown | 2026-10-09T10:29:23+00:00 |
| [firehol-blocklist-net-ua](https://iplists.firehol.org/files/blocklist_net_ua.ipset) | ok | True | 223545 | unknown | 2026-10-09T10:29:23+00:00 |
| [cins-army](https://cinsscore.com/list/ci-badguys.txt) | ok | True | 15000 | unknown | 2026-10-09T10:29:23+00:00 |
| [firehol-cybercrime](https://iplists.firehol.org/files/cybercrime.ipset) | ok | True | 473 | 2026-10-03T07:16:58+00:00 | 2026-10-09T10:29:23+00:00 |
| [firehol-dshield-1d](https://iplists.firehol.org/files/dshield_1d.netset) | ok | True | 31 | 2026-10-09T04:14:50+00:00 | 2026-10-09T10:29:23+00:00 |
| [firehol-et-block](https://iplists.firehol.org/files/et_block.netset) | ok | True | 1607 | 2026-10-08T04:30:01+00:00 | 2026-10-09T10:29:23+00:00 |
| [firehol-et-compromised](https://iplists.firehol.org/files/et_compromised.ipset) | ok | True | 604 | 2026-10-08T20:27:44+00:00 | 2026-10-09T10:29:23+00:00 |
| [firehol-level1](https://iplists.firehol.org/files/firehol_level1.netset) | ok | True | 4629 | 2026-10-09T04:14:50+00:00 | 2026-10-09T10:29:23+00:00 |
| [firehol-level2](https://iplists.firehol.org/files/firehol_level2.netset) | ok | True | 19254 | 2026-10-09T04:37:07+00:00 | 2026-10-09T10:29:23+00:00 |
| [firehol-level3](https://iplists.firehol.org/files/firehol_level3.netset) | ok | True | 12019 | 2026-10-09T04:34:11+00:00 | 2026-10-09T10:29:23+00:00 |
| [firehol-webserver](https://iplists.firehol.org/files/firehol_webserver.netset) | ok | True | 1234 | 2026-10-09T04:31:06+00:00 | 2026-10-09T10:29:23+00:00 |
| [firehol-myip](https://iplists.firehol.org/files/myip.ipset) | ok | True | 1375 | 2026-10-09T04:31:06+00:00 | 2026-10-09T10:29:23+00:00 |
| [spamhaus-drop](https://www.spamhaus.org/drop/drop_v4.json) | ok | True | 1671 | 2026-10-09T09:44:02+00:00 | 2026-10-09T10:29:23+00:00 |
| [blocklist-de-strongips](https://lists.blocklist.de/lists/strongips.txt) | ok | True | 381 | unknown | 2026-10-09T10:29:23+00:00 |
| [myip-ms-latest-blacklist](https://myip.ms/files/blacklist/general/latest_blacklist.txt) | ok | True | 1374 | unknown | 2026-10-09T10:29:23+00:00 |
| [ipsum-level2](https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt) | ok | True | 34669 | unknown | 2026-10-09T10:29:23+00:00 |
| [interserver-iprbl](https://sigs.interserver.net/iprbl.txt) | ok | True | 5533 | unknown | 2026-10-09T10:29:23+00:00 |
| [blocklist-de-export-ips-all](https://www.blocklist.de/downloads/export-ips_all.txt) | ok | True | 24959 | unknown | 2026-10-09T10:29:23+00:00 |
| [abuseipdb-s100-7d](https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-7d.ipv4) | ok | True | 72364 | 2026-10-09T10:11:45+00:00 | 2026-10-09T10:29:23+00:00 |
| [drb-ra-IPC2s-30day](https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv) | ok | True | 256 | unknown | 2026-10-09T10:29:23+00:00 |
| [hagezi-tif](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt) | ok | True | 35422 | unknown | 2026-10-09T10:29:23+00:00 |
| [threatfox-ipport](https://threatfox.abuse.ch/export/csv/ip-port/recent/) | ok | True | 2361 | 2026-10-09T09:45:55+00:00 | 2026-10-09T10:29:23+00:00 |
| [threatview-high-confidence](https://threatview.io/Downloads/IP-High-Confidence-Feed.txt) | ok | True | 17668 | unknown | 2026-10-09T10:29:23+00:00 |

## Automatic redundancy observation

| Candidate | Zero-contribution days | Additional addresses | Suppressed |
|---|---:|---:|---|
| cins-army | 0 | 1688 | False |
| firehol-dshield-1d | 9 | 0 | False |
| firehol-et-block | 1 | 0 | False |
| firehol-myip | 9 | 0 | False |
| threatview-high-confidence | 0 | 3158 | False |

Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.
A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.
Provider timestamps describe the supplied file, not necessarily each underlying threat observation.
Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.
