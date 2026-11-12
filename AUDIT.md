# Current feed audit

Automatically generated; historical notes are in `AUDIT-HISTORY.md`.

- Checked at: 2026-11-12T14:59:06+00:00
- Configured sources: 24
- Contributing sources: 22
- Combined IPv4/CIDR entries: 290187
- Active / expired exceptions: 0 / 0
- Maximum fallback age: 72 hours
- Protected networks: 10 static + GitHub meta ok (103 ranges, last success 2026-11-12T14:59:06+00:00)
- Removed by protection: 6 addresses (abuseipdb-s100-30d: 1, firehol-level3: 5)

Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.
Last success means successful retrieval and validation, not an upstream observation date.

| Source | State | Included | Entries | Provider timestamp | Last success |
|---|---|---|---:|---|---|
| [greensnow](https://blocklist.greensnow.co/greensnow.txt) | ok | True | 2719 | unknown | 2026-11-12T14:59:06+00:00 |
| [binarydefense](https://www.binarydefense.com/banlist.txt) | ok | True | 1001 | unknown | 2026-11-12T14:59:06+00:00 |
| [firehol-blocklist-net-ua](https://iplists.firehol.org/files/blocklist_net_ua.ipset) | ok | True | 223698 | unknown | 2026-11-12T14:59:06+00:00 |
| [cins-army](https://cinsscore.com/list/ci-badguys.txt) | ok | True | 15000 | unknown | 2026-11-12T14:59:06+00:00 |
| [firehol-cybercrime](https://iplists.firehol.org/files/cybercrime.ipset) | ok | True | 520 | 2026-11-11T21:24:49+00:00 | 2026-11-12T14:59:06+00:00 |
| [firehol-dshield-1d](https://iplists.firehol.org/files/dshield_1d.netset) | ok | False | 31 | 2026-11-12T04:29:43+00:00 | 2026-11-12T14:59:06+00:00 |
| [firehol-et-block](https://iplists.firehol.org/files/et_block.netset) | ok | True | 1648 | 2026-11-11T05:30:01+00:00 | 2026-11-12T14:59:06+00:00 |
| [firehol-et-compromised](https://iplists.firehol.org/files/et_compromised.ipset) | ok | True | 487 | 2026-11-11T21:57:23+00:00 | 2026-11-12T14:59:06+00:00 |
| [firehol-level1](https://iplists.firehol.org/files/firehol_level1.netset) | ok | True | 4642 | 2026-11-12T07:29:44+00:00 | 2026-11-12T14:59:06+00:00 |
| [firehol-level2](https://iplists.firehol.org/files/firehol_level2.netset) | ok | True | 17688 | 2026-11-12T10:32:51+00:00 | 2026-11-12T14:59:06+00:00 |
| [firehol-level3](https://iplists.firehol.org/files/firehol_level3.netset) | ok | True | 13109 | 2026-11-12T10:32:23+00:00 | 2026-11-12T14:59:06+00:00 |
| [firehol-webserver](https://iplists.firehol.org/files/firehol_webserver.netset) | ok | True | 976 | 2026-11-09T10:31:00+00:00 | 2026-11-12T14:59:06+00:00 |
| [firehol-myip](https://iplists.firehol.org/files/myip.ipset) | ok | False | 1099 | 2026-11-09T10:31:00+00:00 | 2026-11-12T14:59:06+00:00 |
| [spamhaus-drop](https://www.spamhaus.org/drop/drop_v4.json) | ok | True | 1755 | 2026-11-12T14:26:44+00:00 | 2026-11-12T14:59:06+00:00 |
| [blocklist-de-strongips](https://lists.blocklist.de/lists/strongips.txt) | ok | True | 295 | unknown | 2026-11-12T14:59:06+00:00 |
| [myip-ms-latest-blacklist](https://myip.ms/files/blacklist/general/latest_blacklist.txt) | ok | True | 1099 | unknown | 2026-11-12T14:59:06+00:00 |
| [ipsum-level2](https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt) | ok | True | 35694 | unknown | 2026-11-12T14:59:06+00:00 |
| [interserver-iprbl](https://sigs.interserver.net/iprbl.txt) | ok | True | 4056 | unknown | 2026-11-12T14:59:06+00:00 |
| [blocklist-de-export-ips-all](https://www.blocklist.de/downloads/export-ips_all.txt) | ok | True | 25791 | unknown | 2026-11-12T14:59:06+00:00 |
| [abuseipdb-s100-30d](https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-30d.ipv4) | ok | True | 141736 | 2026-11-12T14:33:47+00:00 | 2026-11-12T14:59:06+00:00 |
| [drb-ra-IPC2s-30day](https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv) | ok | True | 230 | unknown | 2026-11-12T14:59:06+00:00 |
| [hagezi-tif](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt) | ok | True | 35383 | unknown | 2026-11-12T14:59:06+00:00 |
| [threatfox-ipport](https://threatfox-api.abuse.ch/api/v1/) | ok | True | 918 | unknown | 2026-11-12T14:59:06+00:00 |
| [threatview-high-confidence](https://threatview.io/Downloads/IP-High-Confidence-Feed.txt) | ok | True | 15673 | unknown | 2026-11-12T14:59:06+00:00 |

## Automatic redundancy observation

| Candidate | Zero-contribution days | Additional addresses | Suppressed |
|---|---:|---:|---|
| cins-army | 0 | 861 | False |
| firehol-dshield-1d | 43 | 0 | True |
| firehol-et-block | 0 | 2296 | False |
| firehol-myip | 43 | 0 | True |
| threatview-high-confidence | 0 | 2935 | False |

Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.
A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.
Provider timestamps describe the supplied file, not necessarily each underlying threat observation.
Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.
