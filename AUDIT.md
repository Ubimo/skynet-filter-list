# Current feed audit

Automatically generated; historical notes are in `AUDIT-HISTORY.md`.

- Checked at: 2026-11-27T12:10:32+00:00
- Configured sources: 21
- Contributing sources: 20
- Combined IPv4/CIDR entries: 281629
- Active / expired exceptions: 0 / 0
- Maximum fallback age: 72 hours
- Protected networks: 10 static + GitHub meta ok (112 ranges, last success 2026-11-27T12:10:32+00:00)
- Removed by protection: 6 addresses (abuseipdb-s100-30d: 1, firehol-level3: 5)

Counts are unique IPv4/CIDR entries per source, not unique addresses across sources.
Last success means successful retrieval and validation, not an upstream observation date.

| Source | State | Included | Entries | Provider timestamp | Last success |
|---|---|---|---:|---|---|
| [greensnow](https://blocklist.greensnow.co/greensnow.txt) | ok | True | 2184 | unknown | 2026-11-27T12:10:32+00:00 |
| [binarydefense](https://www.binarydefense.com/banlist.txt) | ok | True | 951 | unknown | 2026-11-27T12:10:32+00:00 |
| [firehol-blocklist-net-ua](https://iplists.firehol.org/files/blocklist_net_ua.ipset) | ok | True | 194520 | unknown | 2026-11-27T12:10:32+00:00 |
| [cins-army](https://cinsscore.com/list/ci-badguys.txt) | ok | True | 15000 | unknown | 2026-11-27T12:10:32+00:00 |
| [firehol-cybercrime](https://iplists.firehol.org/files/cybercrime.ipset) | ok | True | 537 | 2026-11-24T04:01:50+00:00 | 2026-11-27T12:10:32+00:00 |
| [firehol-dshield-1d](https://iplists.firehol.org/files/dshield_1d.netset) | ok | False | 31 | 2026-11-27T03:44:47+00:00 | 2026-11-27T12:10:32+00:00 |
| [firehol-et-block](https://iplists.firehol.org/files/et_block.netset) | ok | True | 1626 | 2026-11-25T05:30:01+00:00 | 2026-11-27T12:10:32+00:00 |
| [firehol-et-compromised](https://iplists.firehol.org/files/et_compromised.ipset) | ok | True | 578 | 2026-11-26T21:27:35+00:00 | 2026-11-27T12:10:32+00:00 |
| [firehol-level1](https://iplists.firehol.org/files/firehol_level1.netset) | ok | True | 4612 | 2026-11-27T03:44:47+00:00 | 2026-11-27T12:10:32+00:00 |
| [firehol-level2](https://iplists.firehol.org/files/firehol_level2.netset) | ok | True | 17669 | 2026-11-27T09:28:46+00:00 | 2026-11-27T12:10:32+00:00 |
| [firehol-level3](https://iplists.firehol.org/files/firehol_level3.netset) | ok | True | 13131 | 2026-11-27T06:44:46+00:00 | 2026-11-27T12:10:32+00:00 |
| [spamhaus-drop](https://www.spamhaus.org/drop/drop_v4.json) | ok | True | 1736 | 2026-11-27T11:56:44+00:00 | 2026-11-27T12:10:32+00:00 |
| [blocklist-de-strongips](https://lists.blocklist.de/lists/strongips.txt) | ok | True | 280 | unknown | 2026-11-27T12:10:32+00:00 |
| [ipsum-level2](https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt) | ok | True | 38900 | unknown | 2026-11-27T12:10:32+00:00 |
| [interserver-iprbl](https://sigs.interserver.net/iprbl.txt) | ok | True | 3173 | unknown | 2026-11-27T12:10:32+00:00 |
| [blocklist-de-export-ips-all](https://www.blocklist.de/downloads/export-ips_all.txt) | ok | True | 25239 | unknown | 2026-11-27T12:10:32+00:00 |
| [abuseipdb-s100-30d](https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-30d.ipv4) | ok | True | 161107 | 2026-11-27T11:34:26+00:00 | 2026-11-27T12:10:32+00:00 |
| [drb-ra-IPC2s-30day](https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv) | ok | True | 210 | unknown | 2026-11-27T12:10:32+00:00 |
| [hagezi-tif](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt) | ok | True | 35401 | unknown | 2026-11-27T12:10:32+00:00 |
| [threatfox-ipport](https://threatfox-api.abuse.ch/api/v1/) | ok | True | 7833 | unknown | 2026-11-27T12:10:32+00:00 |
| [threatview-high-confidence](https://threatview.io/Downloads/IP-High-Confidence-Feed.txt) | ok | True | 15651 | unknown | 2026-11-27T12:10:32+00:00 |

## Automatic redundancy observation

| Candidate | Zero-contribution days | Additional addresses | Suppressed |
|---|---:|---:|---|
| cins-army | 0 | 1209 | False |
| firehol-dshield-1d | 58 | 0 | True |
| firehol-et-block | 2 | 0 | False |
| threatview-high-confidence | 0 | 2356 | False |

Suppression requires at least 14 elapsed days and daily observations against healthy non-candidate sources.
A gap over 48 hours or new coverage resets observation; a suppressed source is automatically restored when needed.
Provider timestamps describe the supplied file, not necessarily each underlying threat observation.
Failure details, exclusions, turnover and content SHA-256 hashes are in `generated/status.json`.
