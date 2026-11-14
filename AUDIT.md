# Current feed audit

Automatically generated; historical notes are in `AUDIT-HISTORY.md`.

- Checked at: 2026-11-14T10:18:59+00:00
- Configured sources: 24
- Contributing sources: 22
- Combined IPv4/CIDR entries: 289656
- Active / expired exceptions: 0 / 0
- Maximum fallback age: 72 hours
- Protected networks: 10 static + GitHub meta ok (108 ranges, last success 2026-11-14T10:18:59+00:00)
- Removed by protection: 6 addresses (abuseipdb-s100-30d: 1, firehol-level3: 5)

Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.
Last success means successful retrieval and validation, not an upstream observation date.

| Source | State | Included | Entries | Provider timestamp | Last success |
|---|---|---|---:|---|---|
| [greensnow](https://blocklist.greensnow.co/greensnow.txt) | ok | True | 3162 | unknown | 2026-11-14T10:18:59+00:00 |
| [binarydefense](https://www.binarydefense.com/banlist.txt) | ok | True | 324 | unknown | 2026-11-14T10:18:59+00:00 |
| [firehol-blocklist-net-ua](https://iplists.firehol.org/files/blocklist_net_ua.ipset) | ok | True | 227547 | unknown | 2026-11-14T10:18:59+00:00 |
| [cins-army](https://cinsscore.com/list/ci-badguys.txt) | ok | True | 15000 | unknown | 2026-11-14T10:18:59+00:00 |
| [firehol-cybercrime](https://iplists.firehol.org/files/cybercrime.ipset) | ok | True | 521 | 2026-11-13T13:22:16+00:00 | 2026-11-14T10:18:59+00:00 |
| [firehol-dshield-1d](https://iplists.firehol.org/files/dshield_1d.netset) | ok | False | 34 | 2026-11-14T02:14:42+00:00 | 2026-11-14T10:18:59+00:00 |
| [firehol-et-block](https://iplists.firehol.org/files/et_block.netset) | ok | True | 1641 | 2026-11-12T05:30:02+00:00 | 2026-11-14T10:18:59+00:00 |
| [firehol-et-compromised](https://iplists.firehol.org/files/et_compromised.ipset) | ok | True | 584 | 2026-11-13T21:06:39+00:00 | 2026-11-14T10:18:59+00:00 |
| [firehol-level1](https://iplists.firehol.org/files/firehol_level1.netset) | ok | True | 4647 | 2026-11-14T02:14:42+00:00 | 2026-11-14T10:18:59+00:00 |
| [firehol-level2](https://iplists.firehol.org/files/firehol_level2.netset) | ok | True | 16093 | 2026-11-14T05:11:07+00:00 | 2026-11-14T10:18:59+00:00 |
| [firehol-level3](https://iplists.firehol.org/files/firehol_level3.netset) | ok | True | 13156 | 2026-11-14T05:05:53+00:00 | 2026-11-14T10:18:59+00:00 |
| [firehol-webserver](https://iplists.firehol.org/files/firehol_webserver.netset) | ok | True | 976 | 2026-11-09T10:31:00+00:00 | 2026-11-14T10:18:59+00:00 |
| [firehol-myip](https://iplists.firehol.org/files/myip.ipset) | ok | False | 1099 | 2026-11-09T10:31:00+00:00 | 2026-11-14T10:18:59+00:00 |
| [spamhaus-drop](https://www.spamhaus.org/drop/drop_v4.json) | ok | True | 1758 | 2026-11-13T15:56:44+00:00 | 2026-11-14T10:18:59+00:00 |
| [blocklist-de-strongips](https://lists.blocklist.de/lists/strongips.txt) | ok | True | 292 | unknown | 2026-11-14T10:18:59+00:00 |
| [myip-ms-latest-blacklist](https://myip.ms/files/blacklist/general/latest_blacklist.txt) | ok | True | 1099 | unknown | 2026-11-14T10:18:59+00:00 |
| [ipsum-level2](https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt) | ok | True | 39541 | unknown | 2026-11-14T10:18:59+00:00 |
| [interserver-iprbl](https://sigs.interserver.net/iprbl.txt) | ok | True | 3828 | unknown | 2026-11-14T10:18:59+00:00 |
| [blocklist-de-export-ips-all](https://www.blocklist.de/downloads/export-ips_all.txt) | ok | True | 23388 | unknown | 2026-11-14T10:18:59+00:00 |
| [abuseipdb-s100-30d](https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-30d.ipv4) | ok | True | 147181 | 2026-11-14T10:05:49+00:00 | 2026-11-14T10:18:59+00:00 |
| [drb-ra-IPC2s-30day](https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv) | ok | True | 235 | unknown | 2026-11-14T10:18:59+00:00 |
| [hagezi-tif](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt) | ok | True | 36028 | unknown | 2026-11-14T10:18:59+00:00 |
| [threatfox-ipport](https://threatfox-api.abuse.ch/api/v1/) | ok | True | 817 | unknown | 2026-11-14T10:18:59+00:00 |
| [threatview-high-confidence](https://threatview.io/Downloads/IP-High-Confidence-Feed.txt) | ok | True | 14521 | unknown | 2026-11-14T10:18:59+00:00 |

## Automatic redundancy observation

| Candidate | Zero-contribution days | Additional addresses | Suppressed |
|---|---:|---:|---|
| cins-army | 0 | 1039 | False |
| firehol-dshield-1d | 45 | 0 | True |
| firehol-et-block | 2 | 0 | False |
| firehol-myip | 45 | 0 | True |
| threatview-high-confidence | 0 | 2369 | False |

Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.
A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.
Provider timestamps describe the supplied file, not necessarily each underlying threat observation.
Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.
