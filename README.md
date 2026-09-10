# Skynet Custom Filter List

Curated IPv4 threat feeds for SkyNet, with automatic validation, freshness checks,
independent fallback and exact aggregation. All automation runs in GitHub Actions.

## Router setup

The existing URL remains unchanged:

```sh
firewall banmalware https://raw.githubusercontent.com/Ubimo/skynet-filter-list/main/filter.list
```

`filter.list` now points to **one** file, `generated/combined.ipv4`. It contains the
exact union of usable source snapshots, minus active exceptions, with duplicates
and overlapping/adjacent networks collapsed. Aggregation never adds addresses.
SkyNet needs one data download instead of one per source. Individual snapshots
remain available for validation, source attribution and automatic recovery.

See [AUDIT.md](AUDIT.md) for current counts, provider timestamps and the redundancy
observation table. [generated/status.json](generated/status.json) contains hashes,
exclusions, turnover measurements, failure reasons and observation state.

## Automatic source selection

There are 25 configured sources. `sources.json` is the maintained upstream
manifest; do not edit generated files. IPsum uses level 2, AbuseIPDB the score-100
seven-day feed, and Spamhaus DROP is retrieved directly as JSON from Spamhaus.
Spamhaus copyright, source, provider date and terms are preserved in its snapshot
and in the combined file.

Feodo's file was dated March 4, 2026 during the September 10 review. It is
**quarantined while stale**, checked on every update, and automatically becomes
eligible again only when fresh data passes all validation. Known stale Feodo data
is not treated as an unexpected job failure. An address from Feodo can still be
blocked if another eligible source independently includes it.

Four sources are candidates for automatic suppression from the active union:

- `firehol-et-block`
- `firehol-dshield-1d`
- `firehol-myip`
- `firehol-ciarmy`

A candidate must add zero addresses beyond **healthy non-candidate sources** for
at least 14 elapsed days with at least 14 distinct UTC observation dates. Multiple
runs on one day count only once. A gap longer than 48 hours, an unhealthy candidate
or new unique coverage resets its observation. Candidates cannot justify one
another's removal. A suppressed source continues to be fetched for observation;
it is automatically included again if it becomes useful or its healthy coverage
providers fail. The audit proves that suppression does not change the final union.
No manual follow-up is needed after the observation period. The first possible
suppression is September 24, 2026, depending on actual run times and observations.

## Safety and freshness

- Reject default routes and unapproved upstream networks broader than `/12`.
- Remove unapproved special-use ranges (private, loopback, link-local, CGNAT,
  documentation, multicast and reserved ranges), including overlaps.
- FireHOL level 1 intentionally includes fullbogons. Only its exact reviewed
  special-use prefixes in `allowed_special` are exempt; public ranges are not.
- Reject invalid non-comment rows, malformed UTF-8, insufficient entries and
  excessive special-use entries (more than 1% of retained entries, with one
  tolerated). CSV and Spamhaus JSON have explicit parsers.
- Reject count or unique public-address coverage outside 0.5x to 2x the last
  accepted baseline. Bogons are excluded from the public-coverage metric.
- Also reject turnover above 80% of either the old or the new public-address
  coverage, even if counts stay identical. `max_churn_ratio` can be explicitly
  adjusted per source after review. Added/removed address counts and ratios are
  recorded on successful updates; rejected changes appear in the failure reason.

Freshness uses provider metadata, independently of download success:

| Source type | Provider timestamp | Maximum age |
|---|---|---:|
| FireHOL | `Source File Date`, not the mirror's processing date | 168 hours |
| Spamhaus DROP | JSON metadata timestamp | 72 hours |
| AbuseIPDB | `Last updated` comment | 72 hours |
| Feodo | `Last updated` comment | 72 hours |

Missing required timestamps and implausible future dates fail validation. Sources
without a supported provider timestamp are explicitly shown as `unknown`; the
system does not invent their data age. Provider dates describe the supplied file,
not necessarily every observation or component inside an aggregate feed.

The broader prefixes that can result from exact output aggregation are validated
by full set equivalence to the already checked inputs, rather than applying the
upstream `/12` guard to the merged file. This preserves safety without preventing
lossless compression. These controls do not prove that every listed public IP is
malicious.

## Outages and recovery

Feeds update independently. A failure retains the last accepted file only when
its hash and contents remain valid and it is at most **72 hours since successful
retrieval and validation**. Where a provider date is required, its age limit must
also hold. Downloading the same outdated file never refreshes its provider age.
Expired/unusable sources are excluded from the combined file on the next update.
Their snapshots and baselines remain for diagnosis and recovery. An anomalous
replacement is not accepted just because it has been retried.

Unexpected failures produce `stale` or `disabled` status and fail the workflow
**after** eligible healthy updates are published. `quarantined` is the expected
Feodo stale-data state; `included: false` with healthy status can indicate a
redundant source under continued observation. All states are visible in the audit.

GitHub Actions runs daily at 03:17 UTC and can be dispatched manually. Execution
can be delayed. If Actions stops completely, this code cannot expire data or
change rules already loaded on a router. Router refresh/unban behavior determines
when changes take effect there. The output is IPv4-only; DNS and IPv6 protection
require their own configuration.

## Explain a block and add a temporary exception

```sh
python scripts/lookup_ip.py 8.8.8.8
```

The lookup prints whether the address is blocked in the published local snapshot,
which source networks match, whether each source contributes, and any exception
active at publication. It performs no DNS lookup or other network requests.

`allowlist.json` starts empty. To add an exception, provide a canonical IPv4 host
or network (`/24` or narrower), a nonempty reason and a timezone-aware expiry:

```json
[
  {
    "cidr": "203.0.113.7/32",
    "reason": "Example only: replace with the specific verified address",
    "expires_at": "2026-09-11T18:00:00+00:00"
  }
]
```

This example is not active. Exceptions are subtracted from the combined coverage,
including when a broader upstream CIDR contains the address. Expired exceptions
stop applying on the next successful rebuild, and their status remains visible.
Editing `allowlist.json` triggers the workflow. Do not publish unrelated network
ranges as exceptions.

## Validation and publication

```sh
python -m unittest discover -s tests -v
python scripts/update_ipv4_feeds.py
python scripts/audit_sources.py --current
```

No third-party Python packages are required. Downloads are bounded to 64 MiB with
a 30-second socket timeout and one retry. Run only one updater per local checkout.

PR checks are offline and inspect the exact submitted files without regenerating
over them. The update job checks out current `main`, refreshes sources, validates
the exact candidate and pushes only if the base has not changed. It does not copy
old outputs onto newer code or force-push. After publishing, the raw files are
verified at the immutable commit SHA, including exact combined coverage, hashes,
source files, exceptions, manifest and report.

Updater exit codes: `0` means the update completed without unexpected source
failures (an expected quarantine is allowed); `2` means the update completed with
stale/disabled feeds; other errors abort. Run the audit even after exit `2`.
An empty combined list cannot pass publication validation. Individual file writes
are atomic, and the full candidate is published in one Git commit.

For a reviewed, intentional large source change, remove only that source's record
from `generated/status.json`, regenerate, audit and review the diff before
committing. Corrupt baseline files can instead be restored from Git history.
Changing a source URL or invalidating its old policy requires a reviewed baseline
reset. Automatic redundancy observation is not a substitute for source selection.

## Exclusions and history

`jumpsmm7/GeneratedAdblock/IPlist.list` remains excluded after its collapse to two
entries, including a reserved address, on September 10, 2026. Dedicated Tor exit
lists and out-of-scope VoIP/PBX feeds remain excluded. No new broad scanner feeds
have been added. HaGeZi TIF's domain version is an optional DNS-layer complement;
it must be configured in a DNS blocker, not inserted into this IPv4 manifest.

[AUDIT-HISTORY.md](AUDIT-HISTORY.md) preserves the historical July audit. Current
configuration and measurements are in `sources.json` and `AUDIT.md`.
