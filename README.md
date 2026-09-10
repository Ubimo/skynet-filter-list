# Skynet Custom Filter List

Curated IPv4 threat feeds for SkyNet. All operational sources are served as
validated snapshots from this repository, so upstream errors cannot bypass
validation on the router.

## Using the list

```sh
firewall banmalware https://raw.githubusercontent.com/Ubimo/skynet-filter-list/main/filter.list
```

The URL is unchanged. The repository must remain public. There are 25 configured
sources; the active count and latest results are generated in [AUDIT.md](AUDIT.md).
IPsum uses level 2; AbuseIPDB uses its score-100 seven-day feed.

## Source policy

`sources.json` is the maintained upstream manifest. `filter.list` is generated and
contains only this repository's validated `.ipv4` URLs. Do not edit generated
files by hand. The updater supports whitespace-delimited IPv4/CIDR feeds and the
C2IntelFeeds CSV format. IPv6 removal is explicitly enabled for the three feeds
that require it; an unexpected switch to mixed IPv4/IPv6 elsewhere is rejected.

- Reject default routes and unapproved networks broader than `/12`.
- Remove unapproved special-use ranges (private, loopback, link-local, CGNAT,
  documentation, multicast and reserved ranges), including overlapping networks.
- FireHOL level 1 intentionally contains fullbogons. Only the exact reviewed
  special-use prefixes in its `allowed_special` setting are retained. This is
  not a blanket exemption for private addresses or broad public networks.
- Reject responses with invalid non-comment rows, invalid UTF-8, insufficient
  entries, or excessive special-use entries (more than 1% of retained entries,
  with one tolerated). An explicit CSV header is supported.
- Deduplicate and sort each snapshot. Reject a decrease of more than 50% or an
  increase of more than 100% in either entry count or unique public IPv4 address
  coverage relative to the last accepted snapshot. Intentional bogons are
  excluded from the public-coverage metric. This detects CIDR expansion that
  entry counts alone would miss. Thresholds are conservative operational
  defaults, not a guarantee against every bad upstream change.

These controls validate format and guard against anomalous changes; they do not
prove that every public IP is malicious. Content hashes bind each published
snapshot to its audit record. Source retrieval is bounded to 64 MiB, with a
30-second socket timeout and one retry. No third-party Python packages are needed.

## Temporary outages and recovery

Each feed updates independently. If a download fails or fails validation, its
last accepted file is retained only if its hash, contents and policy still
validate. It stays in `filter.list` for at most **72 hours since the last
successful retrieval and validation**. On a later update after that deadline it
is omitted from `filter.list`; its file and baseline remain available for
inspection and recovery. A new source without a good baseline is omitted on
failure. A successful, non-anomalous download restores the source automatically.
Failures do not reset the age or anomaly baseline.

Every failure is recorded in `generated/status.json` and makes the workflow fail
**after** publishing eligible healthy updates. `AUDIT.md` and the Actions job
summary show `ok`, `stale`, or `disabled`. Configure GitHub Actions failure
notifications for the repository to receive these alerts.

The 72-hour limit is applied whenever the updater runs. If GitHub Actions stops
running altogether, it cannot expire a feed or change a router's already loaded
rules. Monitor the last successful workflow execution. Likewise, a successful
fetch of an unchanged upstream file does not prove that upstream observations
are recent; `last_success` is a validation timestamp, not threat-observation age.
Routers pick up source removal on their next list refresh; existing loaded bans
remain subject to SkyNet's own refresh/unban behavior.

## Updating and validating

GitHub Actions schedules an update daily at 03:17 UTC (execution can be delayed).
It can also be started manually. PR validation is offline and checks the exact
submitted data; it never regenerates over a proposed change. Tests cover parser
safety, anomaly rejection, fallback expiry/recovery, corruption and the published
manifest. The update job checks out current `main`, generates and validates one
candidate, and pushes only if the base has not changed. A concurrent change to
`main` causes failure and requires a fresh run, rather than transplanting outputs
onto untested code. After push, all active raw files, their hashes, the manifest,
configuration and report are checked at the immutable published commit SHA.

```sh
python -m unittest discover -s tests -v
python scripts/update_ipv4_feeds.py
python scripts/audit_sources.py --current
```

Updater exit codes: `0` means all sources healthy; `2` means a completed update
with retained/disabled sources; other errors abort the update. Inspect status and
run the audit even after exit `2`. An empty operational manifest cannot pass the
publication audit. File replacement is atomic per file; publication uses one Git
commit for the full set. Run only one local updater per checkout at a time.

For an intentional large upstream change, inspect the new feed first. To reset
its baseline, remove **only that source's entry** from `generated/status.json`,
run the updater and audit, review its counts and diff, and commit the complete
validated result. The updater never accepts an anomalous change merely because
it has been retried. Restore a corrupted snapshot from Git history before retrying,
or explicitly reset its baseline after reviewing the replacement. Policy changes
that invalidate the old baseline likewise require this deliberate review.

## Exclusions and history

- `jumpsmm7/GeneratedAdblock/IPlist.list` was removed on September 10, 2026:
  the review found only two entries, one in reserved `240.0.0.0/4` space,
  compared with 290 entries in the July audit.
- Dedicated Tor exit lists are excluded: Tor use alone is not malicious.
- VoIP/PBX-specific feeds are outside the protected installation's scope.
- Previously rejected empty, retired or inaccessible feeds remain excluded.

[AUDIT-HISTORY.md](AUDIT-HISTORY.md) preserves the July 2026 audit as historical
context. It does not describe today's source selection. Current upstream URLs,
minimum counts and exact exceptions are in [sources.json](sources.json); current
measured results are in [AUDIT.md](AUDIT.md).
