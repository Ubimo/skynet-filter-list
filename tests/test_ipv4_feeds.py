from __future__ import annotations

import contextlib
from datetime import datetime, timedelta, timezone
import io
import ipaddress
import json
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


class RepositoryTests(unittest.TestCase):
    def test_exact_committed_snapshot(self):
        validate(ROOT)

    def test_removed_upstream_is_not_configured(self):
        self.assertFalse(any('jumpsmm7/GeneratedAdblock' in f['url'] for f in load_feeds(ROOT)))


if __name__ == '__main__':
    unittest.main()
