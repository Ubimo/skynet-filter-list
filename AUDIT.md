# Filter List Audit

- Audit date: July 22, 2026
- Operational sources checked: 40
- Working sources: 40
- HTTP errors: 0
- Empty or non-SkyNet-compatible operational sources: 0
- Duplicate URLs in `filter.list`: 0

The audit checked successful HTTP retrieval and the presence of at least one
IPv4/CIDR line in the first whitespace-delimited field. This matches the
processing performed by SkyNet's `banmalware` implementation. The large
AbuseIPDB feed was also retrieved successfully within the 15-second limit used
by SkyNet. Entry counts are a snapshot and may change between requests for
dynamic sources.

| No. | IP/CIDR lines | URL |
|---:|---:|---|
| 1 | 3,480 | https://blocklist.greensnow.co/greensnow.txt |
| 2 | 5 | https://feodotracker.abuse.ch/downloads/ipblocklist.txt |
| 3 | 609 | https://iplists.firehol.org/files/alienvault_reputation.ipset |
| 4 | 864 | https://iplists.firehol.org/files/bds_atif.ipset |
| 5 | 1,159 | https://iplists.firehol.org/files/bi_any_2_30d.ipset |
| 6 | 127,599 | https://iplists.firehol.org/files/blocklist_net_ua.ipset |
| 7 | 15,000 | https://iplists.firehol.org/files/ciarmy.ipset |
| 8 | 627 | https://iplists.firehol.org/files/coinbl_hosts_browser.ipset |
| 9 | 373 | https://iplists.firehol.org/files/cybercrime.ipset |
| 10 | 20 | https://iplists.firehol.org/files/dshield.netset |
| 11 | 31 | https://iplists.firehol.org/files/dshield_1d.netset |
| 12 | 35 | https://iplists.firehol.org/files/dyndns_ponmocup.ipset |
| 13 | 1,591 | https://iplists.firehol.org/files/et_block.netset |
| 14 | 590 | https://iplists.firehol.org/files/et_compromised.ipset |
| 15 | 1,567 | https://iplists.firehol.org/files/et_spamhaus.netset |
| 16 | 4,574 | https://iplists.firehol.org/files/firehol_level1.netset |
| 17 | 22,009 | https://iplists.firehol.org/files/firehol_level2.netset |
| 18 | 12,378 | https://iplists.firehol.org/files/firehol_level3.netset |
| 19 | 791 | https://iplists.firehol.org/files/firehol_webserver.netset |
| 20 | 4,129 | https://iplists.firehol.org/files/greensnow.ipset |
| 21 | 13,843 | https://iplists.firehol.org/files/iblocklist_ciarmy_malicious.netset |
| 22 | 29,188 | https://iplists.firehol.org/files/iblocklist_pedophiles.netset |
| 23 | 900 | https://iplists.firehol.org/files/iblocklist_spamhaus_drop.netset |
| 24 | 21 | https://iplists.firehol.org/files/malc0de.ipset |
| 25 | 910 | https://iplists.firehol.org/files/myip.ipset |
| 26 | 196 | https://iplists.firehol.org/files/normshield_high_bruteforce.ipset |
| 27 | 1,569 | https://iplists.firehol.org/files/spamhaus_drop.netset |
| 28 | 336 | https://iplists.firehol.org/files/spamhaus_edrop.netset |
| 29 | 171 | https://iplists.firehol.org/files/urlvir.ipset |
| 30 | 334 | https://lists.blocklist.de/lists/strongips.txt |
| 31 | 948 | https://myip.ms/files/blacklist/general/latest_blacklist.txt |
| 32 | 291 | https://raw.githubusercontent.com/jumpsmm7/GeneratedAdblock/master/IPlist.list |
| 33 | 1,746 | https://raw.githubusercontent.com/SecOps-Institute/Tor-IP-Addresses/master/tor-exit-nodes.lst |
| 34 | 110,867 | https://raw.githubusercontent.com/stamparm/ipsum/master/levels/1.txt |
| 35 | 1,692 | https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt |
| 36 | 7,625 | https://sigs.interserver.net/iprbl.txt |
| 37 | 28,679 | https://www.blocklist.de/downloads/export-ips_all.txt |
| 38 | 95,418 | https://voipbl.org/update |
| 39 | 104,572 | https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-30d.ipv4 |
| 40 | 291 | https://raw.githubusercontent.com/Ubimo/skynet-filter-list/main/generated/drb-ra-IPC2s-30day.ipv4 |

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

- `https://darklist.de/raw.php`: most recently returned no IP entries
- `https://iplists.firehol.org/files/normshield_high_attack.ipset`: empty and outdated
- `https://www.talosintelligence.com/documents/ip-blacklist`: HTTP 403
