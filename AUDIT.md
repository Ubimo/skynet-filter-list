# Current feed audit

Automatically generated; historical notes are in `AUDIT-HISTORY.md`.

- Checked at: 2026-11-07T10:01:11+00:00
- Configured sources: 23
- Contributing sources: 21
- Combined IPv4/CIDR entries: 285393
- Active / expired exceptions: 0 / 0
- Maximum fallback age: 72 hours
- Protected networks: 10 static + GitHub meta ok (88 ranges, last success 2026-11-07T10:01:11+00:00)
- Removed by protection: 5 addresses (firehol-level3: 5)

Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.
Last success means successful retrieval and validation, not an upstream observation date.

| Source | State | Included | Entries | Provider timestamp | Last success |
|---|---|---|---:|---|---|
| [greensnow](https://blocklist.greensnow.co/greensnow.txt) | ok | True | 3648 | unknown | 2026-11-07T10:01:11+00:00 |
| [binarydefense](https://www.binarydefense.com/banlist.txt) | ok | True | 1332 | unknown | 2026-11-07T10:01:11+00:00 |
| [firehol-blocklist-net-ua](https://iplists.firehol.org/files/blocklist_net_ua.ipset) | ok | True | 219766 | unknown | 2026-11-07T10:01:11+00:00 |
| [cins-army](https://cinsscore.com/list/ci-badguys.txt) | ok | True | 15000 | unknown | 2026-11-07T10:01:11+00:00 |
| [firehol-cybercrime](https://iplists.firehol.org/files/cybercrime.ipset) | ok | True | 515 | 2026-11-07T00:17:05+00:00 | 2026-11-07T10:01:11+00:00 |
| [firehol-dshield-1d](https://iplists.firehol.org/files/dshield_1d.netset) | ok | False | 33 | 2026-11-07T04:44:41+00:00 | 2026-11-07T10:01:11+00:00 |
| [firehol-et-block](https://iplists.firehol.org/files/et_block.netset) | ok | True | 1646 | 2026-11-06T05:30:01+00:00 | 2026-11-07T10:01:11+00:00 |
| [firehol-et-compromised](https://iplists.firehol.org/files/et_compromised.ipset) | ok | True | 511 | 2026-11-05T21:37:44+00:00 | 2026-11-07T10:01:11+00:00 |
| [firehol-level1](https://iplists.firehol.org/files/firehol_level1.netset) | ok | True | 4649 | 2026-11-07T04:44:41+00:00 | 2026-11-07T10:01:11+00:00 |
| [firehol-level2](https://iplists.firehol.org/files/firehol_level2.netset) | ok | True | 18448 | 2026-11-07T05:17:00+00:00 | 2026-11-07T10:01:11+00:00 |
| [firehol-level3](https://iplists.firehol.org/files/firehol_level3.netset) | ok | True | 12171 | 2026-11-07T05:14:20+00:00 | 2026-11-07T10:01:11+00:00 |
| [firehol-webserver](https://iplists.firehol.org/files/firehol_webserver.netset) | ok | True | 1121 | 2026-11-06T14:00:50+00:00 | 2026-11-07T10:01:11+00:00 |
| [firehol-myip](https://iplists.firehol.org/files/myip.ipset) | ok | False | 1246 | 2026-11-06T14:00:50+00:00 | 2026-11-07T10:01:11+00:00 |
| [spamhaus-drop](https://www.spamhaus.org/drop/drop_v4.json) | ok | True | 1763 | 2026-11-06T15:44:02+00:00 | 2026-11-07T10:01:11+00:00 |
| [blocklist-de-strongips](https://lists.blocklist.de/lists/strongips.txt) | ok | True | 300 | unknown | 2026-11-07T10:01:11+00:00 |
| [myip-ms-latest-blacklist](https://myip.ms/files/blacklist/general/latest_blacklist.txt) | ok | True | 1183 | unknown | 2026-11-07T10:01:11+00:00 |
| [ipsum-level2](https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt) | ok | True | 34766 | unknown | 2026-11-07T10:01:11+00:00 |
| [interserver-iprbl](https://sigs.interserver.net/iprbl.txt) | ok | True | 4397 | unknown | 2026-11-07T10:01:11+00:00 |
| [blocklist-de-export-ips-all](https://www.blocklist.de/downloads/export-ips_all.txt) | ok | True | 26000 | unknown | 2026-11-07T10:01:11+00:00 |
| [abuseipdb-s100-30d](https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-30d.ipv4) | ok | True | 133063 | 2026-11-07T09:33:17+00:00 | 2026-11-07T10:01:11+00:00 |
| [drb-ra-IPC2s-30day](https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv) | ok | True | 224 | unknown | 2026-11-07T10:01:11+00:00 |
| [hagezi-tif](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt) | ok | True | 36099 | unknown | 2026-11-07T10:01:11+00:00 |
| [threatview-high-confidence](https://threatview.io/Downloads/IP-High-Confidence-Feed.txt) | ok | True | 17259 | unknown | 2026-11-07T10:01:11+00:00 |

## Automatic redundancy observation

| Candidate | Zero-contribution days | Additional addresses | Suppressed |
|---|---:|---:|---|
| cins-army | 0 | 546 | False |
| firehol-dshield-1d | 38 | 0 | True |
| firehol-et-block | 0 | 255 | False |
| firehol-myip | 38 | 0 | True |
| threatview-high-confidence | 0 | 2609 | False |

Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.
A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.
Provider timestamps describe the supplied file, not necessarily each underlying threat observation.
Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.
