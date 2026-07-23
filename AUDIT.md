# Filter List Audit

- Audit date: July 23, 2026
- Operational sources checked: 25
- Working sources: 25
- HTTP errors: 0
- Empty or non-SkyNet-compatible operational sources: 0
- IPv6 entries in operational sources after normalization: 0
- Duplicate URLs in `filter.list`: 0

The audit checked successful retrieval, required at least one IPv4/CIDR line,
and rejected any IPv6 address or CIDR in the first whitespace-delimited field.
This matches the processing performed by SkyNet's `banmalware`
implementation while enforcing SkyNet's IPv4-only input constraint. Entry
counts are a snapshot and may change between requests for dynamic sources.

| No. | IP/CIDR lines | URL |
|---:|---:|---|
| 1 | 3,231 | https://blocklist.greensnow.co/greensnow.txt |
| 2 | 5 | https://feodotracker.abuse.ch/downloads/ipblocklist.txt |
| 3 | 864 | https://iplists.firehol.org/files/bds_atif.ipset |
| 4 | 127,837 | https://iplists.firehol.org/files/blocklist_net_ua.ipset |
| 5 | 15,000 | https://iplists.firehol.org/files/ciarmy.ipset |
| 6 | 627 | https://iplists.firehol.org/files/coinbl_hosts_browser.ipset |
| 7 | 373 | https://iplists.firehol.org/files/cybercrime.ipset |
| 8 | 36 | https://iplists.firehol.org/files/dshield_1d.netset |
| 9 | 35 | https://iplists.firehol.org/files/dyndns_ponmocup.ipset |
| 10 | 575 | https://iplists.firehol.org/files/et_compromised.ipset |
| 11 | 4,585 | https://iplists.firehol.org/files/firehol_level1.netset |
| 12 | 13,620 | https://iplists.firehol.org/files/firehol_level3.netset |
| 13 | 778 | https://iplists.firehol.org/files/firehol_webserver.netset |
| 14 | 13,843 | https://iplists.firehol.org/files/iblocklist_ciarmy_malicious.netset |
| 15 | 894 | https://iplists.firehol.org/files/myip.ipset |
| 16 | 335 | https://lists.blocklist.de/lists/strongips.txt |
| 17 | 852 | https://raw.githubusercontent.com/Ubimo/skynet-filter-list/main/generated/myip-ms-latest-blacklist.ipv4 |
| 18 | 290 | https://raw.githubusercontent.com/jumpsmm7/GeneratedAdblock/master/IPlist.list |
| 19 | 34,518 | https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt |
| 20 | 1,694 | https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt |
| 21 | 7,766 | https://sigs.interserver.net/iprbl.txt |
| 22 | 28,027 | https://raw.githubusercontent.com/Ubimo/skynet-filter-list/main/generated/blocklist-de-export-ips-all.ipv4 |
| 23 | 61,647 | https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-7d.ipv4 |
| 24 | 60,425 | https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt |
| 25 | 285 | https://raw.githubusercontent.com/Ubimo/skynet-filter-list/main/generated/drb-ra-IPC2s-30day.ipv4 |

The 25 source responses contained 378,142 IPv4/CIDR lines in total before
cross-source deduplication.

## IPv4-only normalization

The original audit only required at least one IPv4 entry per source. A source
could therefore pass while also containing IPv6. The stricter audit found two
mixed upstream feeds:

| Upstream feed | IPv4 | IPv6 excluded |
|---|---:|---:|
| `myip.ms/latest_blacklist.txt` | 852 | 41 |
| `blocklist.de/export-ips_all.txt` | 28,027 | 592 |

`scripts/update_ipv4_feeds.py` now extracts their IPv4 address/CIDR entries
into generated files. `filter.list` references those generated files, so the
IPv4 coverage is retained while SkyNet receives no IPv6 input.

## Source pruning

The following changes reduce stale data, duplicate coverage, and unnecessary
blocking:

- Removed retired or stale feeds: `alienvault_reputation`, `bi_any_2_30d`,
  `iblocklist_pedophiles`, `iblocklist_spamhaus_drop`, `malc0de`,
  `normshield_high_bruteforce`, `spamhaus_edrop`, and `urlvir`.
- Removed redundant sources: `dshield.netset`, `et_block`, `et_spamhaus`,
  `firehol_level2`, the FireHOL GreenSnow mirror, and the separate
  `spamhaus_drop` mirror.
- Removed Tor exit-node blocking by policy: Tor exit nodes are not inherently
  malicious.
- Removed `voipbl.org/update`: VoIP/PBX abuse is not in scope for the protected
  installation.
- Replaced IPsum level 1 with level 3 and the AbuseIPDB 30-day feed with the
  seven-day feed to reduce low-confidence or older observations.
- Added HaGeZi's Threat Intelligence Feed. During candidate evaluation, 15,796
  of its 57,044 entries were not covered by the previous source union.

## C2 CSV normalization

Upstream:
`https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv`

- HTTP: 200
- Valid, unique IPv4 addresses: 285
- Directly SkyNet-compatible lines: 0
- Cause: a CSV comma immediately follows the IP address (`IP,description`)
- Solution: `scripts/update_ipv4_feeds.py` generates
  `generated/drb-ra-IPC2s-30day.ipv4` with one IP address per line.
- Update schedule: daily at 03:17 UTC through
  `.github/workflows/update-ipv4-feeds.yml`; it can also be triggered manually.

## Intentionally excluded

- Tor exit-node lists: excluded by blocking policy
- `https://voipbl.org/update`: no exposed VoIP/PBX service is in scope
- `https://darklist.de/raw.php`: most recently returned no IP entries
- `https://iplists.firehol.org/files/normshield_high_attack.ipset`: empty and outdated
- `https://www.talosintelligence.com/documents/ip-blacklist`: HTTP 403
