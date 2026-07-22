# Filter List Audit

- Audit date: July 22, 2026
- Operational sources checked: 25
- Working sources: 25
- HTTP errors: 0
- Empty or non-SkyNet-compatible operational sources: 0
- Duplicate URLs in `filter.list`: 0

The audit checked successful HTTP retrieval and the presence of at least one
IPv4/CIDR line in the first whitespace-delimited field. This matches the
processing performed by SkyNet's `banmalware` implementation. The large
AbuseIPDB feed was also retrieved successfully within the 15-second limit used
by SkyNet. `blocklist.de/export-ips_all` timed out once during the parallel
audit and returned HTTP 200 with valid data on the immediate isolated retry.
Entry counts are a snapshot and may change between requests for dynamic
sources.

| No. | IP/CIDR lines | URL |
|---:|---:|---|
| 1 | 3,473 | https://blocklist.greensnow.co/greensnow.txt |
| 2 | 5 | https://feodotracker.abuse.ch/downloads/ipblocklist.txt |
| 3 | 864 | https://iplists.firehol.org/files/bds_atif.ipset |
| 4 | 127,827 | https://iplists.firehol.org/files/blocklist_net_ua.ipset |
| 5 | 15,000 | https://iplists.firehol.org/files/ciarmy.ipset |
| 6 | 627 | https://iplists.firehol.org/files/coinbl_hosts_browser.ipset |
| 7 | 373 | https://iplists.firehol.org/files/cybercrime.ipset |
| 8 | 31 | https://iplists.firehol.org/files/dshield_1d.netset |
| 9 | 35 | https://iplists.firehol.org/files/dyndns_ponmocup.ipset |
| 10 | 590 | https://iplists.firehol.org/files/et_compromised.ipset |
| 11 | 4,574 | https://iplists.firehol.org/files/firehol_level1.netset |
| 12 | 12,378 | https://iplists.firehol.org/files/firehol_level3.netset |
| 13 | 791 | https://iplists.firehol.org/files/firehol_webserver.netset |
| 14 | 13,843 | https://iplists.firehol.org/files/iblocklist_ciarmy_malicious.netset |
| 15 | 910 | https://iplists.firehol.org/files/myip.ipset |
| 16 | 334 | https://lists.blocklist.de/lists/strongips.txt |
| 17 | 903 | https://myip.ms/files/blacklist/general/latest_blacklist.txt |
| 18 | 291 | https://raw.githubusercontent.com/jumpsmm7/GeneratedAdblock/master/IPlist.list |
| 19 | 18,178 | https://raw.githubusercontent.com/stamparm/ipsum/master/levels/3.txt |
| 20 | 1,692 | https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt |
| 21 | 7,627 | https://sigs.interserver.net/iprbl.txt |
| 22 | 27,999 | https://www.blocklist.de/downloads/export-ips_all.txt |
| 23 | 61,305 | https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-7d.ipv4 |
| 24 | 57,044 | https://raw.githubusercontent.com/hagezi/dns-blocklists/main/ips/tif.txt |
| 25 | 291 | https://raw.githubusercontent.com/Ubimo/skynet-filter-list/main/generated/drb-ra-IPC2s-30day.ipv4 |

The 25 source responses contained 356,985 IPv4/CIDR lines in total before
cross-source deduplication.

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
- Valid, unique IPv4 addresses: 291
- Directly SkyNet-compatible lines: 0
- Cause: a CSV comma immediately follows the IP address (`IP,description`)
- Solution: `scripts/update_c2_feed.py` generates
  `generated/drb-ra-IPC2s-30day.ipv4` with one IP address per line.
- Update schedule: daily at 03:17 UTC through
  `.github/workflows/update-c2-feed.yml`; it can also be triggered manually.

## Intentionally excluded

- Tor exit-node lists: excluded by blocking policy
- `https://voipbl.org/update`: no exposed VoIP/PBX service is in scope
- `https://darklist.de/raw.php`: most recently returned no IP entries
- `https://iplists.firehol.org/files/normshield_high_attack.ipset`: empty and outdated
- `https://www.talosintelligence.com/documents/ip-blacklist`: HTTP 403
