# Current feed audit

Automatically generated; historical notes are in `AUDIT-HISTORY.md`.

- Checked at: 2026-11-20T11:30:40+00:00
- Configured sources: 24
- Contributing sources: 20
- Combined IPv4/CIDR entries: 302918
- Active / expired exceptions: 0 / 0
- Maximum fallback age: 72 hours
- Protected networks: 10 static + GitHub meta ok (112 ranges, last success 2026-11-20T11:30:40+00:00)
- Removed by protection: 6 addresses (abuseipdb-s100-30d: 1, firehol-level3: 5)

Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.
Last success means successful retrieval and validation, not an upstream observation date.

| Source | State | Included | Entries | Provider timestamp | Last success |
|---|---|---|---:|---|---|
| [greensnow](https://blocklist.greensnow.co/greensnow.txt) | ok | True | 1347 | unknown | 2026-11-20T11:30:40+00:00 |
| [binarydefense](https://www.binarydefense.com/banlist.txt) | ok | True | 320 | unknown | 2026-11-20T11:30:40+00:00 |
| [firehol-blocklist-net-ua](https://iplists.firehol.org/files/blocklist_net_ua.ipset) | ok | True | 233791 | unknown | 2026-11-20T11:30:40+00:00 |
| [cins-army](https://cinsscore.com/list/ci-badguys.txt) | ok | True | 15000 | unknown | 2026-11-20T11:30:40+00:00 |
| [firehol-cybercrime](https://iplists.firehol.org/files/cybercrime.ipset) | ok | True | 533 | 2026-11-20T06:44:45+00:00 | 2026-11-20T11:30:40+00:00 |
| [firehol-dshield-1d](https://iplists.firehol.org/files/dshield_1d.netset) | ok | False | 34 | 2026-11-20T05:44:42+00:00 | 2026-11-20T11:30:40+00:00 |
| [firehol-et-block](https://iplists.firehol.org/files/et_block.netset) | ok | True | 1628 | 2026-11-18T05:30:01+00:00 | 2026-11-20T11:30:40+00:00 |
| [firehol-et-compromised](https://iplists.firehol.org/files/et_compromised.ipset) | ok | True | 590 | 2026-11-19T21:40:38+00:00 | 2026-11-20T11:30:40+00:00 |
| [firehol-level1](https://iplists.firehol.org/files/firehol_level1.netset) | ok | True | 4629 | 2026-11-20T05:44:42+00:00 | 2026-11-20T11:30:40+00:00 |
| [firehol-level2](https://iplists.firehol.org/files/firehol_level2.netset) | ok | True | 18104 | 2026-11-20T06:44:45+00:00 | 2026-11-20T11:30:40+00:00 |
| [firehol-level3](https://iplists.firehol.org/files/firehol_level3.netset) | ok | True | 13489 | 2026-11-20T06:04:01+00:00 | 2026-11-20T11:30:40+00:00 |
| [firehol-webserver](https://iplists.firehol.org/files/firehol_webserver.netset) | disabled | False | 976 | 2026-11-09T10:31:00+00:00 | 2026-11-15T10:47:38+00:00 |
| [firehol-myip](https://iplists.firehol.org/files/myip.ipset) | disabled | False | 1099 | 2026-11-09T10:31:00+00:00 | 2026-11-15T10:47:38+00:00 |
| [spamhaus-drop](https://www.spamhaus.org/drop/drop_v4.json) | ok | True | 1746 | 2026-11-20T09:56:44+00:00 | 2026-11-20T11:30:40+00:00 |
| [blocklist-de-strongips](https://lists.blocklist.de/lists/strongips.txt) | ok | True | 286 | unknown | 2026-11-20T11:30:40+00:00 |
| [myip-ms-latest-blacklist](https://myip.ms/files/blacklist/general/latest_blacklist.txt) | disabled | False | 1099 | 2026-11-09T11:25:55+00:00 | 2026-11-16T11:15:40+00:00 |
| [ipsum-level2](https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt) | ok | True | 41548 | unknown | 2026-11-20T11:30:40+00:00 |
| [interserver-iprbl](https://sigs.interserver.net/iprbl.txt) | ok | True | 4518 | unknown | 2026-11-20T11:30:40+00:00 |
| [blocklist-de-export-ips-all](https://www.blocklist.de/downloads/export-ips_all.txt) | ok | True | 25122 | unknown | 2026-11-20T11:30:40+00:00 |
| [abuseipdb-s100-30d](https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-30d.ipv4) | ok | True | 155409 | 2026-11-20T11:06:34+00:00 | 2026-11-20T11:30:40+00:00 |
| [drb-ra-IPC2s-30day](https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv) | ok | True | 208 | unknown | 2026-11-20T11:30:40+00:00 |
| [hagezi-tif](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt) | ok | True | 36793 | unknown | 2026-11-20T11:30:40+00:00 |
| [threatfox-ipport](https://threatfox-api.abuse.ch/api/v1/) | ok | True | 1647 | unknown | 2026-11-20T11:30:40+00:00 |
| [threatview-high-confidence](https://threatview.io/Downloads/IP-High-Confidence-Feed.txt) | ok | True | 16567 | unknown | 2026-11-20T11:30:40+00:00 |

## Automatic redundancy observation

| Candidate | Zero-contribution days | Additional addresses | Suppressed |
|---|---:|---:|---|
| cins-army | 0 | 1465 | False |
| firehol-dshield-1d | 51 | 0 | True |
| firehol-et-block | 0 | 249 | False |
| firehol-myip | 0 | 0 | False |
| threatview-high-confidence | 0 | 2359 | False |

Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.
A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.
Provider timestamps describe the supplied file, not necessarily each underlying threat observation.
Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.
