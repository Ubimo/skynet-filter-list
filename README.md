# Skynet Custom Filter List

Curated copy of the list from
[`jumpsmm7/GeneratedAdblock`](https://github.com/jumpsmm7/GeneratedAdblock).

## Files

- `filter.list`: operational list containing 25 IPv4-only sources successfully validated on July 23, 2026
- `generated/*.ipv4`: SkyNet-compatible versions of three upstream feeds that require normalization
- `scripts/update_ipv4_feeds.py`: reproducible update of the normalized IPv4 lists
- `scripts/audit_sources.py`: live validation that rejects operational sources containing IPv6
- `.github/workflows/update-ipv4-feeds.yml`: pull-request validation and daily feed updates
- `AUDIT.md`: validation results including IPv4 and excluded IPv6 counts

## Using the list with Skynet

```sh
firewall banmalware https://raw.githubusercontent.com/Ubimo/skynet-filter-list/main/filter.list
```

The repository must be public so that the router can retrieve the raw file without a GitHub token.

## Intentionally excluded from `filter.list`

- Tor exit-node lists: Tor relays are not inherently malicious and are outside this list's blocking policy
- `https://voipbl.org/update`: VoIP/PBX abuse is outside the scope of the protected installation
- `https://darklist.de/raw.php`: HTTP 200, but currently contains no IP entries
- `https://iplists.firehol.org/files/normshield_high_attack.ipset`: HTTP 200, but empty and, according to its header, not updated since April 19, 2025
- `https://www.talosintelligence.com/documents/ip-blacklist`: HTTP 403 with both `Invoke-WebRequest` and `curl`

## Source selection

The list favors current, directly maintained feeds over old snapshots and
duplicate mirrors. IPsum uses level 2 instead of level 1, and the AbuseIPDB
feed uses a seven-day instead of a 30-day window. HaGeZi's Threat Intelligence
Feed supplements the remaining sources. See `AUDIT.md` for the complete
pruning record and measured entry counts.

## Normalized IPv4 feeds

The upstream feed
`https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv`
contains lines in the format `IP,description`. SkyNet, however, only accepts an
IP address or CIDR as the first whitespace-delimited field. Therefore,
`filter.list` references the normalized file in `generated/`.

Two other upstream feeds contain both address families:

- `myip.ms/latest_blacklist.txt`
- `blocklist.de/export-ips_all.txt`

SkyNet only processes IPv4. The updater removes IPv6 entries from these feeds
without dropping their IPv4 coverage, and `filter.list` references the
normalized `.ipv4` files.

GitHub Actions updates all three files every day at 03:17 UTC. Pull requests run
with read-only repository permissions. Only the scheduled/main-branch update
job receives `contents: write`, and it stages only the three generated files.

Manual update:

```sh
python scripts/update_ipv4_feeds.py
python scripts/audit_sources.py
```

## Comparison with ViktorJp/Skynet

On July 13, 2026,
[`ViktorJp/Skynet/filter.list`](https://github.com/ViktorJp/Skynet/blob/main/filter.list)
was compared with this list. All 33 sources were reachable; 26 were already included.

`firehol_webserver.netset` was added. Fully or largely redundant sources, the
unchanged-since-2019 `maxmind_proxy_fraud.ipset`, and feeds that would broaden
blocking to the Tor network were not added. See `AUDIT.md` for details.

## Maintenance

Add new sources to `filter.list`, one per line. Before using a source, verify:

1. It returns HTTP 2xx without authentication.
2. Every address or CIDR in the first field is IPv4; mixed IPv4/IPv6 feeds must be normalized first.
3. The response contains at least one SkyNet-compatible IPv4 address or CIDR in the first field.
4. The response is not a login, error, or HTML page.
5. The source is stable and intended for automated retrieval.
6. The source does not broadly block privacy infrastructure solely because of its role.
