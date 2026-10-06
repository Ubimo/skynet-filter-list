# Current feed audit

Automatically generated; historical notes are in `AUDIT-HISTORY.md`.

- Checked at: 2026-10-06T10:51:49+00:00
- Configured sources: 24
- Contributing sources: 24
- Combined IPv4/CIDR entries: 228100
- Active / expired exceptions: 0 / 0
- Maximum fallback age: 72 hours
- Protected networks: 10 static + GitHub meta ok (65 ranges, last success 2026-10-06T10:51:49+00:00)
- Removed by protection: 5 addresses (firehol-level3: 5)

Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.
Last success means successful retrieval and validation, not an upstream observation date.

| Source | State | Included | Entries | Provider timestamp | Last success |
|---|---|---|---:|---|---|
| [greensnow](https://blocklist.greensnow.co/greensnow.txt) | ok | True | 3658 | unknown | 2026-10-06T10:51:49+00:00 |
| [binarydefense](https://www.binarydefense.com/banlist.txt) | ok | True | 1976 | unknown | 2026-10-06T10:51:49+00:00 |
| [firehol-blocklist-net-ua](https://iplists.firehol.org/files/blocklist_net_ua.ipset) | ok | True | 215904 | unknown | 2026-10-06T10:51:49+00:00 |
| [cins-army](https://cinsscore.com/list/ci-badguys.txt) | ok | True | 15000 | unknown | 2026-10-06T10:51:49+00:00 |
| [firehol-cybercrime](https://iplists.firehol.org/files/cybercrime.ipset) | ok | True | 473 | 2026-10-03T07:16:58+00:00 | 2026-10-06T10:51:49+00:00 |
| [firehol-dshield-1d](https://iplists.firehol.org/files/dshield_1d.netset) | ok | True | 30 | 2026-10-06T04:59:59+00:00 | 2026-10-06T10:51:49+00:00 |
| [firehol-et-block](https://iplists.firehol.org/files/et_block.netset) | ok | True | 1622 | 2026-10-05T04:30:02+00:00 | 2026-10-06T10:51:49+00:00 |
| [firehol-et-compromised](https://iplists.firehol.org/files/et_compromised.ipset) | ok | True | 621 | 2026-10-02T20:46:08+00:00 | 2026-10-06T10:51:49+00:00 |
| [firehol-level1](https://iplists.firehol.org/files/firehol_level1.netset) | ok | True | 4613 | 2026-10-06T04:59:59+00:00 | 2026-10-06T10:51:49+00:00 |
| [firehol-level2](https://iplists.firehol.org/files/firehol_level2.netset) | ok | True | 12593 | 2026-10-06T05:21:18+00:00 | 2026-10-06T10:51:49+00:00 |
| [firehol-level3](https://iplists.firehol.org/files/firehol_level3.netset) | ok | True | 12708 | 2026-10-06T05:19:46+00:00 | 2026-10-06T10:51:49+00:00 |
| [firehol-webserver](https://iplists.firehol.org/files/firehol_webserver.netset) | ok | True | 1241 | 2026-10-06T00:00:48+00:00 | 2026-10-06T10:51:49+00:00 |
| [firehol-myip](https://iplists.firehol.org/files/myip.ipset) | ok | True | 1395 | 2026-10-06T00:00:48+00:00 | 2026-10-06T10:51:49+00:00 |
| [spamhaus-drop](https://www.spamhaus.org/drop/drop_v4.json) | ok | True | 1640 | 2026-10-06T02:44:02+00:00 | 2026-10-06T10:51:49+00:00 |
| [blocklist-de-strongips](https://lists.blocklist.de/lists/strongips.txt) | ok | True | 384 | unknown | 2026-10-06T10:51:49+00:00 |
| [myip-ms-latest-blacklist](https://myip.ms/files/blacklist/general/latest_blacklist.txt) | ok | True | 1401 | unknown | 2026-10-06T10:51:49+00:00 |
| [ipsum-level2](https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt) | ok | True | 32741 | unknown | 2026-10-06T10:51:49+00:00 |
| [interserver-iprbl](https://sigs.interserver.net/iprbl.txt) | ok | True | 5633 | unknown | 2026-10-06T10:51:49+00:00 |
| [blocklist-de-export-ips-all](https://www.blocklist.de/downloads/export-ips_all.txt) | ok | True | 19169 | unknown | 2026-10-06T10:51:49+00:00 |
| [abuseipdb-s100-7d](https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-7d.ipv4) | ok | True | 72800 | 2026-10-06T10:40:23+00:00 | 2026-10-06T10:51:49+00:00 |
| [drb-ra-IPC2s-30day](https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv) | ok | True | 241 | unknown | 2026-10-06T10:51:49+00:00 |
| [hagezi-tif](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt) | ok | True | 33707 | unknown | 2026-10-06T10:51:49+00:00 |
| [threatfox-ipport](https://threatfox.abuse.ch/export/csv/ip-port/recent/) | ok | True | 2293 | 2026-10-06T10:40:16+00:00 | 2026-10-06T10:51:49+00:00 |
| [threatview-high-confidence](https://threatview.io/Downloads/IP-High-Confidence-Feed.txt) | ok | True | 13219 | unknown | 2026-10-06T10:51:49+00:00 |

## Automatic redundancy observation

| Candidate | Zero-contribution days | Additional addresses | Suppressed |
|---|---:|---:|---|
| cins-army | 0 | 1507 | False |
| firehol-dshield-1d | 6 | 0 | False |
| firehol-et-block | 0 | 30399 | False |
| firehol-myip | 6 | 0 | False |
| threatview-high-confidence | 0 | 2387 | False |

Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.
A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.
Provider timestamps describe the supplied file, not necessarily each underlying threat observation.
Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.
