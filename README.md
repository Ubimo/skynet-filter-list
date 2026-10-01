# Skynet Filter List

A curated, validated IPv4 blocklist for [Skynet](https://github.com/Adamm00/IPSet_ASUS)
on Asuswrt-Merlin routers. GitHub Actions fetches the upstream feeds daily, checks
each one for integrity and freshness, merges them into a single
deduplicated list and publishes it only after an exact audit.

Current counts, provider dates and source states: [AUDIT.md](AUDIT.md).
Machine-readable details (hashes, turnover, failure reasons): [generated/status.json](generated/status.json).

## Router setup

```sh
firewall banmalware https://raw.githubusercontent.com/Ubimo/skynet-filter-list/main/filter.list
```

`filter.list` points to one file, `generated/combined.ipv4`, so Skynet downloads a
single list instead of one per source.

Schedule Skynet's refresh **after** the daily build (03:17 UTC, can be delayed),
for example every day at 07:25 router time:

```sh
firewall settings banmalware daily 7
```

With a weekly schedule the router can be up to seven days behind, which defeats
the freshness checks below. The repository must stay **public**: Skynet downloads
the list without credentials.

## What ends up in the list

`combined.ipv4` is the exact union of all usable sources, minus active exceptions,
minus protected infrastructure and minus all special-use ranges, with duplicates
and adjacent networks collapsed. Aggregation never adds addresses.

It never contains private, loopback, link-local, CGNAT, documentation, benchmark,
multicast or reserved space (`0/8`, `10/8`, `100.64/10`, `127/8`, `169.254/16`,
`172.16/12`, `192.0.0/24`, `192.0.2/24`, `192.168/16`, `198.18/15`,
`198.51.100/24`, `203.0.113/24`, `224/3`). This is enforced when building and
again when auditing.

The output is IPv4 only. Sources that may contain IPv6 must allow it explicitly
(`allow_ipv6`); those entries are dropped and counted in `status.json`. Domain
blocklists belong in a DNS blocker such as AdGuard Home or Diversion, not in this
repository.

## Sources

Configured in [`sources.json`](sources.json), the only file to edit by hand.

| Source | Feed | Age check |
|---|---|---|
| `spamhaus-drop` | Spamhaus DROP (JSON) | provider timestamp, 72 h |
| `abuseipdb-s100-7d` | AbuseIPDB score 100, 7 days (borestad) | provider timestamp, 72 h |
| `firehol-level1` | FireHOL level 1 | provider timestamp, 168 h |
| `firehol-level2` | FireHOL level 2 | provider timestamp, 168 h |
| `firehol-level3` | FireHOL level 3 | provider timestamp, 168 h |
| `firehol-webserver` | FireHOL webserver | provider timestamp, 168 h |
| `firehol-cybercrime` | FireHOL Cybercrime | provider timestamp, 168 h, quarantined when stale |
| `firehol-et-compromised` | Emerging Threats compromised (FireHOL) | provider timestamp, 168 h |
| `firehol-et-block` | Emerging Threats block (FireHOL) | provider timestamp, 168 h |
| `firehol-dshield-1d` | DShield top blocks, 1 day (FireHOL) | provider timestamp, 168 h |
| `firehol-myip` | myip.ms (FireHOL) | provider timestamp, 168 h |
| `firehol-blocklist-net-ua` | blocklist.net.ua (FireHOL); upstream frozen since 2026-09-21 | **none** (explicitly disabled) |
| `cins-army` | CINS Army | content, 168 h |
| `ipsum-level2` | IPsum level 2 | content, 168 h |
| `blocklist-de-export-ips-all` | blocklist.de all | content, 168 h |
| `blocklist-de-strongips` | blocklist.de strong IPs | content, 168 h |
| `greensnow` | GreenSnow | content, 168 h |
| `binarydefense` | Binary Defense banlist | content, 168 h |
| `interserver-iprbl` | InterServer RBL | content, 168 h |
| `myip-ms-latest-blacklist` | myip.ms latest | content, 168 h |
| `hagezi-tif` | HaGeZi Threat Intelligence Feed (IPs) | content, 168 h |
| `drb-ra-IPC2s-30day` | C2IntelFeeds, C2 IPs, 30 days | content, 168 h |
| `threatfox-ipport` | abuse.ch ThreatFox, recent `ip:port` IOCs (botnet C2), confidence ≥ 75 | provider timestamp, 72 h |
| `threatview-high-confidence` | Threatview.io high-confidence IPs | content, 168 h |

Spamhaus copyright, terms, source and provider date are carried into its snapshot
and into the combined file.

Each provider's terms of use apply. ThreatFox (abuse.ch) grants free use under
fair-use principles and may require a paid subscription for commercial use;
Threatview does not state redistribution terms. Neither explicitly covers
republishing in a public repository.

## Validation

Every source must pass all checks before its data is accepted:

- **Integrity**: HTTPS only (no downgrade), at most 64 MiB, strict UTF-8, no
  invalid rows, at least one valid IPv4 entry. A reviewed source may drop up
  to `max_invalid_rows` malformed upstream rows (at most 100; counted as
  `excluded_invalid`); published snapshots never contain any.
- **Formats**: plain lists (first field), CSV, Spamhaus JSON, and ThreatFox CSV
  (`threatfox_csv`: the address from `ioc_value`, rows below `min_confidence`
  dropped, any unexpected row rejects the file).
- **Scope**: no network broader than `/12`, no default route. Special-use entries
  are removed; more than 1% of them (one is tolerated) rejects the file. FireHOL
  level 1 may keep its reviewed fullbogon prefixes (`allowed_special`) in its own
  snapshot only.
- **No size limits**: growth, shrinkage and turnover are accepted immediately, for
  every source and for the combined list (owner's decision, 2026-10-01). Turnover is
  still recorded in `status.json` for information.
- **Freshness by provider timestamp**: FireHOL `Source File Date` (not the mirror's
  processing date), Spamhaus JSON metadata, or a `# Last updated:` comment. Missing
  or future timestamps are rejected. Re-downloading an old file never makes it newer.
- **Freshness by content**: sources without a provider timestamp record
  `content_changed_at`. Content unchanged for more than 168 hours
  (`max_unchanged_hours` per source) counts as expired. `"max_unchanged_hours":
  null` is an explicit, reviewed opt-out for a source kept on purpose although it
  no longer changes.

These checks guard against broken, stale or manipulated feeds. They do not prove
that every listed address is malicious.

## Source states

| State | Meaning | In the list |
|---|---|---|
| `ok` | fetched and validated in this run | yes (unless suppressed) |
| `stale` | fetch or validation failed, or content unchanged too long; the last accepted data is kept for at most 72 hours after its last successful validation, and only while its provider date is still within limits | yes |
| `disabled` | failed beyond that window, provider data expired, or no valid baseline | no |
| `quarantined` | known stale-data condition for sources with `quarantine_on_stale`; checked every run, returns automatically | no |

`stale` and `disabled` fail the workflow, but only after all healthy updates have
been published. `quarantined` is expected and does not fail it.

## Redundancy suppression

Sources marked `redundancy_candidate` (`firehol-et-block`, `firehol-dshield-1d`,
`firehol-myip`, `cins-army`, `threatview-high-confidence`) are dropped from the union while they add nothing
beyond the healthy non-candidate sources, and only after at least 14 elapsed days
with 14 distinct daily observations. A gap over 48 hours or any unique address
resets the observation; candidates cannot justify each other's removal. Suppressed
sources are still fetched and return automatically as soon as they add coverage or
a covering source fails. The audit proves that suppression never changes the
published union.

## Exceptions

To unblock an address temporarily, add it to [`allowlist.json`](allowlist.json):

```json
[
  {
    "cidr": "203.0.113.7/32",
    "reason": "Why this specific address must not be blocked",
    "expires_at": "2026-10-31T18:00:00+00:00"
  }
]
```

Rules: a canonical IPv4 host or network of `/24` or narrower, a non-empty reason
and a timezone-aware expiry. Exceptions are subtracted even from broader upstream
networks. Expired entries stop applying on the next build and stay visible in the
audit. Editing the file triggers the workflow.

## Protected infrastructure

Some addresses must never be blocked, because the router itself depends on them.
[`protected.json`](protected.json) removes them from the published list
permanently, even when an upstream source lists them (on 2026-09-30, FireHOL
level 3 contained three of the four `raw.githubusercontent.com` addresses, from
which Skynet downloads this list, and two `github.com` addresses).

- **`networks`**: reviewed static entries, always applied, even if every download
  fails: GitHub's own ranges and the Cloudflare, Google and Quad9 DNS resolvers.
  Each entry needs a canonical public IPv4 network of `/16` or narrower and a
  reason.
- **`github_meta`**: GitHub's published IPv4 ranges for the listed keys
  (`web`, `api`, `git`, `pages`) from `https://api.github.com/meta`, fetched on
  every update (authenticated, the token is sent only to `api.github.com`) and
  stored as `generated/protected-github.ipv4`. A response with a range broader
  than `/16`, special-use space, fewer than 4 ranges or more than 131,072
  addresses is rejected. On failure the last good snapshot stays in force and the
  run fails so it gets noticed; it never expires.

The audit fails if the published list contains any protected address, and
`status.json`/`AUDIT.md` show how many addresses protection removed and from which
sources. To add an entry, edit `protected.json` and rebuild offline in the same PR:

```sh
python scripts/rebuild_snapshot.py
python -m unittest discover -s tests -v
python scripts/audit_sources.py
```

A new or changed `github_meta` configuration is recorded as `missing` (static
protection only) until the next update run fetches it.

## Lookup

To find out why an address is blocked or protected (offline, no network requests):

```sh
python scripts/lookup_ip.py 8.8.8.8
```

## Automation

The workflow [`.github/workflows/update-ipv4-feeds.yml`](.github/workflows/update-ipv4-feeds.yml)
runs daily at 03:17 UTC, on pushes to `main` that touch configuration or code,
and manually via *Run workflow*.

**Update job** (on `main`):

1. Regression tests. The committed-snapshot test is skipped here
   (`SKIP_COMMITTED_SNAPSHOT=1`) because the new snapshot is audited right after
   refresh; a configuration change can therefore never block the run that
   applies it.
2. Refresh all sources and build the candidate.
3. Audit the exact candidate against the current time.
4. Publish in one commit, only if `main` has not changed in the meantime. No
   force-push, no copying old outputs onto newer code.
5. Download the published raw files at the exact commit SHA and audit them again.

**PR check**: runs the tests and audits the submitted files offline, without
regenerating them. Newly added sources are accepted as pending until their first
refresh (`--allow-new-sources`); everything already recorded must match exactly.

The runner is pinned to `ubuntu-24.04`, all actions are pinned by commit SHA, and
Dependabot proposes action updates weekly. No third-party Python packages are
used.

Updater exit codes: `0` success (an expected quarantine is fine), `2` completed
with stale or disabled sources or failed GitHub meta protection, anything else
aborted.

If Actions stops entirely, nothing here can expire data already loaded on a
router; the router keeps its last downloaded list.

## Maintenance

**Add a source**: add an entry to `sources.json` (unique `name` and `https://`
URL, optional `freshness`, `parser`, `max_unchanged_hours`, `max_invalid_rows`,
`min_confidence`, `allow_ipv6`, `redundancy_candidate`) and open a PR. The first refresh after merging fetches it.

**Remove a source**: delete it from `sources.json` and rebuild the snapshot
offline in the same PR:

```sh
python scripts/rebuild_snapshot.py
python -m unittest discover -s tests -v
python scripts/audit_sources.py
```

The rebuild uses only the committed, already validated snapshots, removes the
source's record and file, and recomputes the combined list and redundancy
evidence.

**Change a source URL**: remove only that source's record from
`generated/status.json`, run the updater, audit and review the diff. Corrupt
snapshot files can be restored from Git history.

**Run locally** (one updater per checkout at a time):

```sh
python -m unittest discover -s tests -v
python scripts/update_ipv4_feeds.py
python scripts/audit_sources.py --current
```

Never edit files under `generated/`, `AUDIT.md` or `filter.list` by hand; they are
produced by the scripts and verified byte for byte.

## Repository layout

| Path | Purpose |
|---|---|
| `sources.json` | source manifest and per-source policy |
| `allowlist.json` | temporary exceptions |
| `protected.json` | permanently protected infrastructure (static + GitHub meta) |
| `filter.list` | manifest read by Skynet |
| `generated/combined.ipv4` | published blocklist |
| `generated/<source>.ipv4` | validated snapshot per source |
| `generated/protected-github.ipv4` | validated GitHub meta snapshot |
| `generated/status.json` | state, hashes, metrics, errors, redundancy evidence, protection |
| `AUDIT.md` | human-readable report, generated |
| `scripts/update_ipv4_feeds.py` | fetch, validate, build |
| `scripts/audit_sources.py` | exact audit of local or published files |
| `scripts/rebuild_snapshot.py` | offline rebuild after removing sources |
| `scripts/lookup_ip.py` | explain why an address is blocked |
| `scripts/feed_policy.py`, `feed_freshness.py`, `feed_analysis.py`, `feed_protection.py` | parsing, freshness, interval and protection logic |
| `tests/` | unit and integration tests |

## History

- **2026-09-10**: `jumpsmm7/GeneratedAdblock/IPlist.list` excluded after it
  collapsed to two entries, one of them reserved.
- **2026-09-28**:
  - Special-use ranges removed from the combined list; previously FireHOL level 1
    fullbogons (including RFC1918, CGNAT and multicast) were published.
  - `firehol-blocklist-net-ua` removed: provider date unchanged since
    2026-09-21 while it made up about 90% of all entries.
  - Duplicates removed: `emerging-block-ips` (address-identical to
    `firehol-et-block`, which has an age check) and `firehol-ciarmy-malicious`
    (delayed copy of the CI Army data).
  - `firehol-ciarmy` replaced by the direct CINS list `cins-army`, about six
    hours fresher.
  - Feodo Tracker removed: unchanged since 2026-03-04 and quarantined since;
    abuse.ch SSLBL is discontinued as well.
  - Content-based freshness, combined plausibility check, offline rebuild and
    pending new sources added.
  - ThreatFox (`threatfox-ipport`) and Threatview (`threatview-high-confidence`)
    added.
  - `firehol-blocklist-net-ua` re-added at the owner's request, without any age
    limit. Its upstream (also the original CSV at blocklist.net.ua) has not
    changed since 2026-09-21; by the provider's own unban dates, 14% of its
    entries had expired at that point. It stays until removed manually.

- **2026-10-01**: Protected infrastructure added (`protected.json`, GitHub meta).
  FireHOL level 3 had blocked `raw.githubusercontent.com` (185.199.109–111.133)
  and `github.com` (140.82.121.3/.4).

- **2026-10-01**: All size limits removed at the owner's request: no 0.5x–2x
  check per source or for the combined list, no turnover limit, no
  `minimum_entries` (one valid entry suffices). Content, scope, freshness and
  special-use checks are unchanged.

Deliberately not included: dedicated Tor exit lists, VoIP/PBX feeds, broad scanner
lists, FireHOL level 4 and IPsum level 1 (higher false-positive risk).

The July 2026 audit is preserved in [AUDIT-HISTORY.md](AUDIT-HISTORY.md).
