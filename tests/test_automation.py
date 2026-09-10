from datetime import datetime, timedelta, timezone
import contextlib
import io
import ipaddress
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from feed_analysis import combine, intervals, select_sources, subtract, turnover
from feed_freshness import metadata, StaleSourceError
from feed_policy import parse
from lookup_ip import lookup
import test_ipv4_feeds as fixtures
from test_ipv4_feeds import NOW, BODY, FEED


class FreshnessTests(unittest.TestCase):
    def test_provider_age_not_retrieval_time(self):
        feed = dict(FEED, freshness={'type': 'iso_comment', 'max_age_hours': 72})
        body = '# Last updated: 2026-09-10 00:00:00 UTC\n' + BODY
        first, second = metadata(body, feed, NOW), metadata(body, feed, NOW + timedelta(hours=24))
        self.assertEqual(first, second)
        with self.assertRaises(StaleSourceError):
            metadata(body, feed, NOW + timedelta(hours=73))

    def test_missing_and_future_timestamps(self):
        feed = dict(FEED, freshness={'type': 'iso_comment', 'max_age_hours': 72})
        for body in (BODY, '# Last updated: 2027-09-10 00:00:00 UTC\n' + BODY):
            with self.assertRaises(ValueError):
                metadata(body, feed, NOW)

    def test_firehol_uses_source_date_not_mirror_date(self):
        feed = dict(FEED, freshness={'type': 'firehol', 'max_age_hours': 168})
        body = '# Source File Date: Tue Sep  1 00:00:00 UTC 2026\n# This File Date: Thu Sep 10 00:00:00 UTC 2026\n' + BODY
        with self.assertRaises(StaleSourceError):
            metadata(body, feed, NOW)

    def test_spamhaus_metadata_attribution_and_cidr(self):
        feed = dict(FEED, parser='spamhaus_json', freshness={'type': 'spamhaus_json', 'max_age_hours': 72})
        row = {'type': 'metadata', 'timestamp': int(NOW.timestamp()), 'records': 1,
               'copyright': '(c) The Spamhaus Project', 'terms': 'https://www.spamhaus.org/drop/terms/'}
        body = json.dumps({'cidr': '8.8.8.0/24'}) + '\n' + json.dumps(row)
        result = metadata(body, feed, NOW)
        self.assertIn(row['copyright'], result['attribution'])
        self.assertEqual(len(parse(body, feed).networks), 1)
        row['records'] = 2
        with self.assertRaises(ValueError):
            metadata(json.dumps({'cidr': '8.8.8.0/24'}) + '\n' + json.dumps(row), feed, NOW)


class IntervalTests(unittest.TestCase):
    def test_subtraction_matches_small_exhaustive_sets(self):
        for a in range(8):
            for b in range(a, 8):
                base = [(0, 3), (5, 9)]
                actual = {x for lo, hi in subtract(base, [(a, b)]) for x in range(lo, hi + 1)}
                expected = (set(range(4)) | set(range(5, 10))) - set(range(a, b + 1))
                self.assertEqual(actual, expected)

    def test_combination_and_host_exception_do_not_expand_coverage(self):
        networks = {ipaddress.ip_network(n) for n in ('8.8.8.0/30', '8.8.8.4/30', '8.8.8.1/32')}
        combined = combine([networks], [{'cidr': '8.8.8.3/32'}])
        actual = {int(a) for n in combined for a in n}
        self.assertEqual(actual, {int(a) for n in networks for a in n} - {int(ipaddress.ip_address('8.8.8.3'))})
        self.assertEqual(len(combine([networks], [])), 1)

    def test_same_count_complete_replacement_detected(self):
        old = {ipaddress.ip_network('8.8.8.0/24')}
        new = {ipaddress.ip_network('8.8.9.0/24')}
        change = turnover(new, old, FEED)
        self.assertEqual(change['added_ratio'], 1)
        self.assertEqual(change['removed_ratio'], 1)


class ObservationTests(unittest.TestCase):
    def setUp(self):
        self.feeds = [dict(FEED, name='candidate', redundancy_candidate=True), dict(FEED, name='core')]
        self.networks = {f['name']: {ipaddress.ip_network('8.8.8.8')} for f in self.feeds}
        self.records = {f['name']: {'status': 'ok'} for f in self.feeds}

    def observe(self, day, previous):
        return select_sources(self.feeds, self.records, self.networks, previous, NOW + timedelta(days=day))

    def test_requires_fourteen_elapsed_days_not_repeated_runs(self):
        previous = {}
        for _ in range(20):
            previous = self.observe(0, previous)
        self.assertEqual(previous['candidate']['days'], 1)
        for day in range(1, 14):
            previous = self.observe(day, previous)
            self.assertFalse(previous['candidate']['suppressed'])
        previous = self.observe(14, previous)
        self.assertTrue(previous['candidate']['suppressed'])
        self.assertFalse(self.records['candidate']['included'])

    def test_gap_resets_observation(self):
        previous = self.observe(0, {})
        previous = self.observe(3, previous)
        self.assertEqual(previous['candidate']['days'], 1)

    def test_covering_source_failure_reinstates_candidate(self):
        previous = {}
        for day in range(15):
            previous = self.observe(day, previous)
        self.records['core']['status'] = 'stale'
        previous = self.observe(15, previous)
        self.assertFalse(previous['candidate']['suppressed'])
        self.assertTrue(self.records['candidate']['included'])

    def test_new_unique_coverage_reinstates_candidate(self):
        previous = {}
        for day in range(15):
            previous = self.observe(day, previous)
        self.networks['candidate'].add(ipaddress.ip_network('8.8.4.4'))
        previous = self.observe(15, previous)
        self.assertEqual(previous['candidate']['unique_addresses'], 1)
        self.assertTrue(self.records['candidate']['included'])

    def test_candidates_cannot_justify_each_others_removal(self):
        self.feeds[1]['redundancy_candidate'] = True
        previous = {}
        for day in range(16):
            previous = self.observe(day, previous)
        self.assertTrue(all(record['included'] for record in self.records.values()))


class IntegrationTests(unittest.TestCase):
    setUp = fixtures.UpdateTests.setUp
    run_update = fixtures.UpdateTests.run_update
    state = fixtures.UpdateTests.state
    audit = fixtures.UpdateTests.audit
    def configure(self):
        (self.root / 'sources.json').write_text(json.dumps(self.feeds))

    def test_provider_expiry_disables_recently_downloaded_fallback(self):
        self.feeds[0] = dict(FEED, freshness={'type': 'iso_comment', 'max_age_hours': 1})
        self.configure()
        self.run_update(bodies={self.feeds[0]['url']: '# Last updated: 2026-09-10 00:00:00 UTC\n' + BODY,
                                self.feeds[1]['url']: BODY})
        self.run_update(NOW + timedelta(hours=2), {self.feeds[0]['url']: OSError('down'), self.feeds[1]['url']: BODY})
        self.assertEqual(self.state()['one']['status'], 'disabled')
        self.audit(NOW + timedelta(hours=2))

    def test_known_stale_feed_quarantines_then_recovers_automatically(self):
        self.feeds[0] = dict(FEED, freshness={'type': 'iso_comment', 'max_age_hours': 72}, quarantine_on_stale=True)
        self.configure()
        self.assertFalse(self.run_update(bodies={self.feeds[0]['url']: '# Last updated: 2026-03-04 00:00:00 UTC\n' + BODY,
                                               self.feeds[1]['url']: BODY}))
        self.assertEqual(self.state()['one']['status'], 'quarantined')
        self.audit()
        self.assertFalse(self.run_update(bodies={self.feeds[0]['url']: '# Last updated: 2026-09-10 00:00:00 UTC\n' + BODY,
                                               self.feeds[1]['url']: BODY}))
        self.assertEqual(self.state()['one']['status'], 'ok')
        self.audit()

    def test_churn_keeps_good_snapshot_and_records_reason(self):
        self.run_update()
        self.run_update(NOW + timedelta(hours=1), {self.feeds[0]['url']: BODY.replace('8.8.4.', '8.8.5.'),
                                                  self.feeds[1]['url']: BODY})
        self.assertEqual(self.state()['one']['status'], 'stale')
        self.assertIn('turnover', self.state()['one']['error'])
        self.audit(NOW + timedelta(hours=1))

    def test_exception_expires_and_lookup_explains_source(self):
        exception = {'cidr': '8.8.4.1/32', 'reason': 'Temporary test exception',
                     'expires_at': (NOW + timedelta(hours=1)).isoformat()}
        (self.root / 'allowlist.json').write_text(json.dumps([exception]))
        self.run_update()
        found = lookup('8.8.4.1', self.root)
        self.assertFalse(found['blocked_in_published_snapshot'])
        self.assertEqual(len(found['sources']), 2)
        self.assertEqual(found['exceptions_at_publication'][0]['reason'], exception['reason'])
        self.audit()
        self.run_update(NOW + timedelta(hours=2))
        self.assertTrue(lookup('8.8.4.1', self.root)['blocked_in_published_snapshot'])
        self.audit(NOW + timedelta(hours=2))

    def test_combined_file_tampering_is_rejected(self):
        self.run_update()
        with (self.root / 'generated/combined.ipv4').open('a') as output:
            output.write('0.0.0.0/0\n')
        with self.assertRaisesRegex(ValueError, 'Combined file'):
            self.audit()

    def test_exception_expiring_before_publication_requires_regeneration(self):
        exception = {'cidr': '8.8.4.1/32', 'reason': 'Brief exception',
                     'expires_at': (NOW + timedelta(minutes=1)).isoformat()}
        (self.root / 'allowlist.json').write_text(json.dumps([exception]))
        self.run_update()
        with self.assertRaisesRegex(ValueError, 'Exception expired'):
            self.audit(NOW + timedelta(minutes=2))

    def test_quarantine_discards_legacy_baseline_without_provider_age(self):
        self.run_update()
        self.feeds[0] = dict(FEED, freshness={'type': 'iso_comment', 'max_age_hours': 72}, quarantine_on_stale=True)
        self.configure()
        self.run_update(bodies={self.feeds[0]['url']: '# Last updated: 2026-03-04 00:00:00 UTC\n' + BODY,
                                self.feeds[1]['url']: BODY})
        self.assertIsNone(self.state()['one']['last_success'])
        self.assertFalse(self.run_update(bodies={self.feeds[0]['url']: '# Last updated: 2026-09-10 00:00:00 UTC\n8.8.4.1\n',
                                                self.feeds[1]['url']: BODY}))
        self.audit()

    def test_overbroad_unexplained_or_timeless_exceptions_are_rejected(self):
        for exception in ({'cidr': '8.0.0.0/8', 'reason': 'too broad', 'expires_at': '2026-10-01T00:00:00+00:00'},
                          {'cidr': '8.8.8.8/32', 'reason': '', 'expires_at': '2026-10-01T00:00:00+00:00'},
                          {'cidr': '8.8.8.8/32', 'reason': 'missing timezone', 'expires_at': '2026-10-01T00:00:00'}):
            (self.root / 'allowlist.json').write_text(json.dumps([exception]))
            with self.assertRaises(ValueError):
                self.run_update()


if __name__ == '__main__':
    unittest.main()
