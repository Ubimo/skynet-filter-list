from __future__ import annotations

import contextlib
from datetime import datetime, timedelta, timezone
import io
import ipaddress
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from feed_policy import check_change, download, load_feeds, metrics, parse, serialize
from update_ipv4_feeds import update
from audit_sources import validate
from rebuild_snapshot import rebuild

FEED = {'name': 'one', 'url': 'https://example.com/one', 'minimum_entries': 1}
NOW = datetime(2026, 9, 10, tzinfo=timezone.utc)
BODY = '8.8.4.1\n8.8.4.2\n8.8.4.3\n8.8.4.4\n'


class PolicyTests(unittest.TestCase):
    def test_csv_header_duplicates_and_ipv6(self):
        result = parse('ip,description\n8.8.8.8,one\n8.8.8.8,two\n2001:db8::1,v6\n',
                       dict(FEED, parser='csv', allow_ipv6=True))
        self.assertEqual(serialize(result.networks), '8.8.8.8\n')
        self.assertEqual(result.ipv6, 1)

    def test_invalid_rows_and_html_are_not_silently_discarded(self):
        for body in ('<html>error</html>\n8.8.8.8', '8.8.8.8\nnot-an-ip', ''):
            with self.subTest(body=body), self.assertRaises(ValueError):
                parse(body, FEED)

    def test_unexpected_ipv6_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unexpected IPv6'):
            parse('8.8.8.8\n2001:db8::1', FEED)

    def test_dangerous_networks_are_rejected_not_filtered(self):
        for network in ('0.0.0.0/0', '0.0.0.0/1', '8.0.0.0/8', '224.0.0.0/3'):
            with self.subTest(network=network), self.assertRaisesRegex(ValueError, 'broad'):
                parse('8.8.8.8\n' + network, FEED)

    def test_special_addresses_are_removed_from_upstream(self):
        for address in ('127.0.0.1', '172.18.0.2', '100.87.53.0', '242.130.55.162', '203.0.113.1'):
            with self.subTest(address=address):
                parsed = parse('8.8.8.8\n' + address, FEED)
                self.assertEqual(serialize(parsed.networks), '8.8.8.8\n')
                self.assertEqual(parsed.excluded_special, 1)
                with self.assertRaises(ValueError):
                    parse('8.8.8.8\n' + address, FEED, published=True)

    def test_network_overlapping_special_range_is_removed(self):
        parsed = parse('8.8.8.8\n192.0.0.0/16', FEED)
        self.assertEqual(parsed.excluded_special, 1)

    def test_excessive_special_addresses_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Too many special'):
            parse('8.8.8.8\n127.0.0.1\n127.0.0.2', FEED)

    def test_exact_bogon_exception_does_not_allow_subnets_or_default_route(self):
        feed = dict(FEED, allowed_special=['127.0.0.0/8', '224.0.0.0/3'])
        parsed = parse('8.8.8.8\n127.0.0.0/8\n224.0.0.0/3\n127.0.0.1', feed)
        self.assertEqual(len(parsed.networks), 3)
        self.assertEqual(parsed.excluded_special, 1)
        with self.assertRaises(ValueError):
            parse('0.0.0.0/0', feed)

    def test_cidr_coverage_changes_are_detected_with_same_entry_count(self):
        old = metrics(parse('8.8.8.8', FEED).networks, FEED)
        new = metrics(parse('8.8.8.0/24', FEED).networks, FEED)
        with self.assertRaisesRegex(ValueError, 'public_addresses'):
            check_change(new, old)

    def test_count_drop_and_growth_and_boundaries(self):
        old = {'entries': 100, 'public_addresses': 100}
        for count in (49, 201):
            with self.assertRaises(ValueError):
                check_change({'entries': count, 'public_addresses': 100}, old)
        for count in (50, 100, 200):
            check_change({'entries': count, 'public_addresses': count}, old)

    def test_coverage_is_unique_and_excludes_intentional_bogons(self):
        feed = dict(FEED, allowed_special=['127.0.0.0/8'])
        networks = {ipaddress.ip_network(n) for n in ('8.8.8.0/24', '8.8.8.8', '127.0.0.0/8')}
        self.assertEqual(metrics(networks, feed), {'entries': 3, 'public_addresses': 256})

    def test_download_rejects_oversized_and_invalid_utf8_bodies(self):
        for body, expected in ((b'x' * 9, ValueError), (b'\xff', UnicodeDecodeError)):
            with self.subTest(body=body), patch('feed_policy.MAX_SOURCE_BYTES', 8), \
                    patch('feed_policy.urllib.request.urlopen') as opened:
                response = opened.return_value.__enter__.return_value
                response.url = FEED['url']
                response.read.return_value = body
                with self.assertRaises(expected):
                    download(FEED['url'], retries=0)

    def test_download_retries_transient_failure(self):
        with patch('feed_policy.urllib.request.urlopen') as opened, patch('feed_policy.time.sleep'):
            response = opened.return_value.__enter__.return_value
            response.url = FEED['url']
            response.read.return_value = b'8.8.8.8\n'
            opened.side_effect = [TimeoutError('temporary'), opened.return_value]
            self.assertEqual(download(FEED['url']), '8.8.8.8\n')
            self.assertEqual(opened.call_count, 2)


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.feeds = [FEED, dict(FEED, name='two', url='https://example.com/two')]
        (self.root / 'sources.json').write_text(json.dumps(self.feeds), encoding='utf-8')
        (self.root / 'allowlist.json').write_text('[]', encoding='utf-8')

    def run_update(self, now=NOW, bodies=None):
        bodies = bodies or {feed['url']: BODY for feed in self.feeds}
        def fetch(url):
            value = bodies[url]
            if isinstance(value, Exception):
                raise value
            return value
        with contextlib.redirect_stdout(io.StringIO()):
            return update(self.root, now=now, fetch=fetch, workers=2)

    def state(self):
        return json.loads((self.root / 'generated/status.json').read_text())['sources']

    def audit(self, now=NOW):
        with contextlib.redirect_stdout(io.StringIO()):
            validate(self.root, now=now)

    def test_initial_snapshot_passes_exact_audit(self):
        self.assertFalse(self.run_update())
        self.audit()

    def test_failure_retains_good_source_and_updates_healthy_peer(self):
        self.run_update()
        old = (self.root / 'generated/one.ipv4').read_bytes()
        bodies = {self.feeds[0]['url']: TimeoutError('offline'), self.feeds[1]['url']: BODY + '8.8.4.5\n'}
        self.assertTrue(self.run_update(NOW + timedelta(hours=24), bodies))
        self.assertEqual((self.root / 'generated/one.ipv4').read_bytes(), old)
        self.assertEqual(self.state()['one']['status'], 'stale')
        self.assertEqual(self.state()['two']['metrics']['entries'], 5)
        self.audit(NOW + timedelta(hours=24))

    def test_repeated_failure_does_not_reset_age_and_expires_after_72_hours(self):
        self.run_update()
        bodies = {self.feeds[0]['url']: TimeoutError('offline'), self.feeds[1]['url']: BODY}
        for hours, expected in ((24, 'stale'), (72, 'stale'), (73, 'disabled')):
            self.run_update(NOW + timedelta(hours=hours), bodies)
            self.assertEqual(self.state()['one']['status'], expected)
            self.assertEqual(self.state()['one']['last_success'], NOW.isoformat(timespec='seconds'))
            self.audit(NOW + timedelta(hours=hours))
        self.assertFalse(self.state()['one']['included'])
        self.assertTrue((self.root / 'generated/one.ipv4').exists())

    def test_recovery_reenables_source(self):
        self.run_update()
        self.run_update(NOW + timedelta(hours=73), {self.feeds[0]['url']: OSError('down'), self.feeds[1]['url']: BODY})
        self.assertFalse(self.run_update(NOW + timedelta(hours=74)))
        self.assertEqual(self.state()['one']['status'], 'ok')
        self.assertTrue(self.state()['one']['included'])
        self.audit(NOW + timedelta(hours=74))

    def test_anomaly_remains_rejected_on_retries(self):
        self.run_update()
        bodies = {self.feeds[0]['url']: '8.8.4.1\n', self.feeds[1]['url']: BODY}
        for hours in (1, 25, 74, 100):
            self.assertTrue(self.run_update(NOW + timedelta(hours=hours), bodies))
            self.assertEqual(self.state()['one']['metrics']['entries'], 4)
            self.assertIn('Anomalous', self.state()['one']['error'])
            self.audit(NOW + timedelta(hours=hours))

    def test_failed_first_download_has_no_unverified_fallback(self):
        bodies = {self.feeds[0]['url']: OSError('down'), self.feeds[1]['url']: BODY}
        self.assertTrue(self.run_update(bodies=bodies))
        self.assertEqual(self.state()['one']['status'], 'disabled')
        self.audit()

    def test_corrupt_baseline_is_disabled_and_not_silently_reset(self):
        self.run_update()
        (self.root / 'generated/one.ipv4').write_text('0.0.0.0/0\n')
        for hours in (1, 2):
            self.assertTrue(self.run_update(NOW + timedelta(hours=hours)))
            self.assertEqual(self.state()['one']['status'], 'disabled')
            self.assertTrue(self.state()['one']['baseline_invalid'])
            self.audit(NOW + timedelta(hours=hours))

    def test_restoring_original_file_repairs_corrupt_baseline(self):
        self.run_update()
        path = self.root / 'generated/one.ipv4'
        original = path.read_bytes()
        path.write_text('0.0.0.0/0\n')
        self.run_update(NOW + timedelta(hours=1))
        path.write_bytes(original)
        self.assertFalse(self.run_update(NOW + timedelta(hours=2)))
        self.audit(NOW + timedelta(hours=2))

    def test_changed_upstream_cannot_inherit_another_sources_baseline(self):
        self.run_update()
        self.feeds[0] = dict(FEED, url='https://example.com/replacement')
        (self.root / 'sources.json').write_text(json.dumps(self.feeds))
        for hours in (1, 2):
            self.assertTrue(self.run_update(NOW + timedelta(hours=hours)))
            self.assertEqual(self.state()['one']['status'], 'disabled')
            self.audit(NOW + timedelta(hours=hours))

    def test_empty_and_duplicate_configuration_rejected(self):
        for config in ([], [FEED, FEED], [dict(FEED, name='../escape')], [dict(FEED, name='combined')],
                       [dict(FEED, allowed_special=['0.0.0.0/0'])]):
            (self.root / 'sources.json').write_text(json.dumps(config))
            with self.assertRaises(ValueError):
                load_feeds(self.root)

    def test_empty_duplicate_and_external_manifest_entries_rejected(self):
        self.run_update()
        path = self.root / 'filter.list'
        body = path.read_text()
        for invalid in ('', body + body, 'https://example.com/bypass\n'):
            path.write_text(invalid)
            with self.assertRaises(ValueError):
                self.audit()

    def test_missing_generated_file_is_not_vacuously_valid(self):
        self.run_update()
        (self.root / 'generated/one.ipv4').unlink()
        with self.assertRaises(OSError):
            self.audit()

    def test_tampered_file_and_hash_mismatch_rejected(self):
        self.run_update()
        (self.root / 'generated/one.ipv4').write_text(BODY + '8.8.4.5\n')
        with self.assertRaises(ValueError):
            self.audit()

    def test_stale_data_cannot_be_published_after_deadline(self):
        self.run_update()
        with self.assertRaisesRegex(ValueError, 'Expired'):
            self.audit(NOW + timedelta(hours=73))

    def test_all_sources_failing_without_baseline_cannot_publish_empty_manifest(self):
        self.assertTrue(self.run_update(bodies={f['url']: OSError('down') for f in self.feeds}))
        with self.assertRaisesRegex(ValueError, 'Empty manifest'):
            self.audit()

    def test_report_must_match_data(self):
        self.run_update()
        (self.root / 'AUDIT.md').write_text('stale report')
        with self.assertRaisesRegex(ValueError, 'AUDIT.md'):
            self.audit()

    def test_remote_reader_validates_returned_content_not_local_copy(self):
        self.run_update()
        def read(path):
            return BODY + '8.8.4.5\n' if path == 'generated/one.ipv4' else (self.root / path).read_text()
        with self.assertRaises(ValueError):
            validate(self.root, now=NOW, read=read)

    def write_feeds(self):
        (self.root / 'sources.json').write_text(json.dumps(self.feeds), encoding='utf-8')

    def test_unchanged_content_without_provider_date_goes_stale_then_disabled(self):
        one, two = (f['url'] for f in self.feeds)
        self.run_update()
        bodies = {one: BODY, two: BODY + '8.8.4.5\n'}
        self.assertFalse(self.run_update(NOW + timedelta(hours=100), bodies))
        self.assertEqual(self.state()['one']['content_changed_at'], NOW.isoformat(timespec='seconds'))
        # 169h unchanged exceeds the 168h default; last accepted data is 69h old.
        self.assertTrue(self.run_update(NOW + timedelta(hours=169), bodies))
        self.assertEqual(self.state()['one']['status'], 'stale')
        self.assertIn('unchanged', self.state()['one']['error'])
        self.assertTrue(self.state()['one']['included'])
        self.audit(NOW + timedelta(hours=169))
        # Retrying identical content never refreshes its age: disabled after 72h.
        self.assertTrue(self.run_update(NOW + timedelta(hours=173), bodies))
        self.assertEqual(self.state()['one']['status'], 'disabled')
        self.assertFalse(self.state()['one']['included'])
        self.audit(NOW + timedelta(hours=173))
        bodies[one] = BODY + '8.8.4.6\n'
        self.assertFalse(self.run_update(NOW + timedelta(hours=174), bodies))
        self.assertEqual(self.state()['one']['status'], 'ok')
        self.assertEqual(self.state()['one']['content_changed_at'],
                         (NOW + timedelta(hours=174)).isoformat(timespec='seconds'))
        self.audit(NOW + timedelta(hours=174))

    def test_unchanged_limit_is_configurable_and_validated(self):
        self.feeds[0] = dict(FEED, max_unchanged_hours=24)
        self.write_feeds()
        one, two = (f['url'] for f in self.feeds)
        self.run_update()
        self.assertTrue(self.run_update(NOW + timedelta(hours=25), {one: BODY, two: BODY + '8.8.4.5\n'}))
        self.assertEqual(self.state()['one']['status'], 'stale')
        self.assertEqual(self.state()['two']['status'], 'ok')
        for invalid in (0, -1, 'x', True):
            (self.root / 'sources.json').write_text(json.dumps([dict(FEED, max_unchanged_hours=invalid)]))
            with self.assertRaises(ValueError):
                load_feeds(self.root)

    def test_removed_source_and_large_combined_change_are_published_but_flagged(self):
        one, two = (f['url'] for f in self.feeds)
        self.assertFalse(self.run_update(bodies={one: BODY, two: '9.9.9.1\n9.9.9.2\n9.9.9.3\n9.9.9.4\n9.9.9.5\n'}))
        self.feeds = self.feeds[:1]
        self.write_feeds()
        self.assertFalse(self.run_update(NOW + timedelta(hours=1), {one: BODY}))
        state = json.loads((self.root / 'generated/status.json').read_text())
        self.assertEqual(set(state['sources']), {'one'})
        self.assertEqual(state['combined']['public_addresses'], 4)
        self.assertIn('9 -> 4', state['combined_anomaly'])
        self.assertIn('9 -> 4', json.loads((self.root / '.update-result.json').read_text())['combined_anomaly'])
        self.assertIn('Combined coverage anomaly', (self.root / 'AUDIT.md').read_text())
        self.audit(NOW + timedelta(hours=1))
        # Alarm fires once; the new coverage becomes the next baseline.
        self.assertFalse(self.run_update(NOW + timedelta(hours=2), {one: BODY}))
        self.assertIsNone(json.loads((self.root / 'generated/status.json').read_text())['combined_anomaly'])
        self.audit(NOW + timedelta(hours=2))

    def test_offline_rebuild_after_removing_source_passes_exact_audit(self):
        one, two = (f['url'] for f in self.feeds)
        self.run_update(bodies={one: BODY, two: '9.9.9.1\n'})
        self.feeds = self.feeds[:1]
        self.write_feeds()
        with self.assertRaisesRegex(ValueError, 'configured sources'):
            self.audit()
        self.assertEqual(rebuild(self.root), ['two'])
        self.audit()
        self.assertFalse((self.root / 'generated/two.ipv4').exists())
        self.assertNotIn('9.9.9.1', (self.root / 'generated/combined.ipv4').read_text())
        self.feeds.append(dict(FEED, name='three', url='https://example.com/three'))
        self.write_feeds()
        with self.assertRaisesRegex(ValueError, 'normal update'):
            rebuild(self.root)

    def test_new_source_is_pending_only_for_pr_checks_until_first_refresh(self):
        self.run_update()
        self.feeds.append(dict(FEED, name='three', url='https://example.com/three'))
        self.write_feeds()
        with self.assertRaisesRegex(ValueError, 'configured sources'):
            self.audit()
        with contextlib.redirect_stdout(io.StringIO()):
            validate(self.root, now=NOW, allow_pending=True)
        # A removed source is never "pending": stale records still fail.
        self.feeds = self.feeds[1:]
        self.write_feeds()
        with self.assertRaisesRegex(ValueError, 'configured sources'):
            validate(self.root, now=NOW, allow_pending=True)
        self.assertFalse(self.run_update(NOW + timedelta(hours=1),
                                         {f['url']: BODY + '8.8.4.9\n' for f in self.feeds}))
        self.assertEqual(self.state()['three']['status'], 'ok')
        self.audit(NOW + timedelta(hours=1))


class ParserExtensionTests(unittest.TestCase):
    THREATFOX = dict(FEED, parser='threatfox_csv', min_confidence=75)
    HEADER = ('# Last updated: 2026-09-10 00:00:00 UTC #\n'
              '# "first_seen_utc","ioc_id","ioc_value","ioc_type","threat_type","fk_malware",'
              '"malware_alias","malware_printable","last_seen_utc","confidence_level","is_compromised",'
              '"reference","tags","anonymous","reporter"\n')

    @staticmethod
    def row(value, confidence, kind='ip:port'):
        return (f'"2026-09-09 10:00:00", "1", "{value}", "{kind}", "botnet_cc", "x", "None", "X", "", '
                f'"{confidence}", "False", "", "", "0", "r"\n')

    def test_threatfox_extracts_address_and_filters_confidence(self):
        body = self.HEADER + self.row('8.8.8.8:443', 100) + self.row('8.8.8.8:8080', 75) \
            + self.row('8.8.4.4:4444', 50) + self.row('[2001:db8::1]:443', 90)
        parsed = parse(body, dict(self.THREATFOX, allow_ipv6=True))
        self.assertEqual({str(n) for n in parsed.networks}, {'8.8.8.8/32'})
        self.assertEqual(parsed.ipv6, 1)
        with self.assertRaisesRegex(ValueError, 'IPv6'):
            parse(body, self.THREATFOX)

    def test_threatfox_rejects_unexpected_rows(self):
        for bad in (self.row('8.8.8.8:443', 'high'), self.row('example.com:443', 100, 'domain'),
                    '"2026-09-09 10:00:00", "1", "8.8.8.8:443"\n', self.row('8.8.8.8', 100)):
            with self.subTest(row=bad[:60]), self.assertRaisesRegex(ValueError, 'ThreatFox'):
                parse(self.HEADER + self.row('8.8.8.8:443', 100) + bad, self.THREATFOX)

    def test_threatfox_published_snapshot_is_plain(self):
        parsed = parse(self.HEADER + self.row('8.8.8.8:443', 100), self.THREATFOX)
        body = serialize(parsed.networks)
        self.assertEqual(body, '8.8.8.8\n')
        self.assertEqual(parse(body, self.THREATFOX, published=True).networks, parsed.networks)

    def test_invalid_rows_tolerated_only_up_to_limit_and_never_when_published(self):
        body = BODY + '120.229.26.013\n81.183.41.001\n'
        with self.assertRaisesRegex(ValueError, '2 invalid'):
            parse(body, FEED)
        with self.assertRaisesRegex(ValueError, '2 invalid'):
            parse(body, dict(FEED, max_invalid_rows=1))
        parsed = parse(body, dict(FEED, max_invalid_rows=2))
        self.assertEqual((len(parsed.networks), parsed.invalid), (4, 2))
        with self.assertRaisesRegex(ValueError, 'invalid'):
            parse(body, dict(FEED, max_invalid_rows=2), published=True)

    def test_new_options_are_validated(self):
        root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__('shutil').rmtree(root))
        for option in ({'min_confidence': 101}, {'min_confidence': True}, {'max_invalid_rows': -1},
                       {'max_invalid_rows': 101}, {'max_invalid_rows': '3'}, {'parser': 'unknown'}):
            (root / 'sources.json').write_text(json.dumps([dict(FEED, **option)]))
            with self.subTest(option=option), self.assertRaises(ValueError):
                load_feeds(root)

    def test_configured_new_sources_use_their_parsers(self):
        feeds = {f['name']: f for f in load_feeds(ROOT)}
        self.assertEqual(feeds['threatfox-ipport']['parser'], 'threatfox_csv')
        self.assertEqual(feeds['threatfox-ipport']['freshness']['type'], 'iso_comment')
        self.assertGreater(feeds['threatview-high-confidence']['max_invalid_rows'], 0)


class RepositoryTests(unittest.TestCase):
    # The update job skips this: it validates the freshly generated candidate
    # after refresh instead, so a config change (e.g. a removed source) cannot
    # block the refresh that would make the committed snapshot consistent again.
    @unittest.skipIf(os.environ.get('SKIP_COMMITTED_SNAPSHOT') == '1', 'validated after refresh')
    def test_exact_committed_snapshot(self):
        validate(ROOT, allow_pending=True)

    def test_removed_upstream_is_not_configured(self):
        self.assertFalse(any('jumpsmm7/GeneratedAdblock' in f['url'] for f in load_feeds(ROOT)))


if __name__ == '__main__':
    unittest.main()
