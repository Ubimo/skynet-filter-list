from datetime import timedelta
import contextlib
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from feed_analysis import overlaps
from feed_protection import load_protected, parse_github_meta
from lookup_ip import lookup
from rebuild_snapshot import rebuild
import test_ipv4_feeds as fixtures
from test_ipv4_feeds import NOW, BODY

META_URL = 'https://example.com/meta'
META = json.dumps({'web': ['9.9.9.0/30', '9.9.7.0/30', '9.9.5.0/30', '9.9.3.0/30', '2001:db8::/32'],
                   'domains': {'website': ['*.github.com']}})


class ProtectionConfigTests(unittest.TestCase):
    def test_github_meta_bounds(self):
        keys = ['web']
        self.assertEqual(len(parse_github_meta(META, keys)), 4)
        for body in ('[]', '{}', json.dumps({'web': '9.9.9.0/30'}),
                     json.dumps({'web': ['9.9.9.0/30', '9.8.0.0/15']}),           # too broad
                     json.dumps({'web': ['9.9.9.0/30', '9.9.7.0/30', '10.0.0.0/24', '9.9.3.0/30']}),  # special
                     json.dumps({'web': ['9.9.9.0/30', '9.9.7.0/30']}),           # too few
                     json.dumps({'web': ['9.1.0.0/16', '9.3.0.0/16', '9.5.0.0/16', '9.7.0.0/16']}),  # too many addresses
                     'not json'):
            with self.subTest(body=body), self.assertRaises(ValueError):
                parse_github_meta(body, keys)

    def test_static_entries_and_meta_config_are_validated(self):
        root = Path(self.id().replace('.', '_'))
        configs = (
            {'networks': [{'cidr': '8.0.0.0/8', 'reason': 'too broad'}]},
            {'networks': [{'cidr': '8.8.8.8/32', 'reason': ''}]},
            {'networks': [{'cidr': '8.8.8.8/32', 'reason': 'a'}, {'cidr': '8.8.8.8/32', 'reason': 'b'}]},
            {'networks': [{'cidr': '10.1.0.0/24', 'reason': 'special-use'}]},
            {'networks': [{'cidr': '2001:db8::/48', 'reason': 'IPv6'}]},
            {'networks': [{'cidr': '8.8.8.0/16', 'reason': 'not canonical'}]},
            {'networks': [], 'unknown': True},
            {'github_meta': {'url': 'http://api.github.com/meta', 'keys': ['web']}},
            {'github_meta': {'url': META_URL, 'keys': []}},
        )
        for config in configs:
            with self.subTest(config=config), self.assertRaises(ValueError):
                load_protected(root, read=lambda path, c=config: json.dumps(c))


class ProtectionIntegrationTests(unittest.TestCase):
    setUp = fixtures.UpdateTests.setUp
    state = fixtures.UpdateTests.state
    audit = fixtures.UpdateTests.audit

    def protect(self, networks=(), meta=True):
        config = {'networks': [{'cidr': n, 'reason': 'test infrastructure'} for n in networks]}
        if meta:
            config['github_meta'] = {'url': META_URL, 'keys': ['web']}
        (self.root / 'protected.json').write_text(json.dumps(config), encoding='utf-8')

    def run_update(self, now=NOW, meta=META, body=BODY + '9.9.9.1\n'):
        bodies = {feed['url']: body for feed in self.feeds}
        bodies[META_URL] = meta
        def fetch(url):
            value = bodies[url]
            if isinstance(value, Exception):
                raise value
            return value
        with contextlib.redirect_stdout(io.StringIO()):
            return fixtures.update(self.root, now=now, fetch=fetch, workers=2)

    def full(self):
        return json.loads((self.root / 'generated/status.json').read_text())

    def published(self):
        return (self.root / 'generated/combined.ipv4').read_text()

    def test_static_and_github_protection_remove_infrastructure(self):
        self.protect(['8.8.4.0/30'])
        self.assertFalse(self.run_update())
        self.assertEqual(self.published(), '8.8.4.4\n')
        protection = self.full()['protection']
        self.assertEqual(protection['github_meta']['status'], 'ok')
        self.assertEqual(protection['removed_addresses'], 4)
        self.assertEqual(protection['removed_by_source'], {'one': 4, 'two': 4})
        self.assertIn('Removed by protection: 4 addresses (one: 4, two: 4)', (self.root / 'AUDIT.md').read_text())
        found = lookup('9.9.9.1', self.root)
        self.assertFalse(found['blocked_in_published_snapshot'])
        self.assertEqual(found['protected'], [{'cidr': '9.9.9.0/30', 'origin': 'GitHub meta'}])
        self.assertEqual(lookup('8.8.4.1', self.root)['protected'][0]['origin'], 'protected.json')
        self.audit()

    def test_failed_or_invalid_meta_keeps_last_snapshot_and_fails_run(self):
        self.protect()
        self.assertFalse(self.run_update())
        first = self.full()['protection']['github_meta']
        for hour, meta in enumerate((OSError('offline'), json.dumps({'web': ['9.0.0.0/8']})), start=1):
            with self.subTest(meta=str(meta)):
                now = NOW + timedelta(hours=hour)
                self.assertTrue(self.run_update(now, meta))
                github = self.full()['protection']['github_meta']
                self.assertEqual(github['status'], 'stale')
                self.assertEqual((github['sha256'], github['last_success']), (first['sha256'], first['last_success']))
                self.assertNotIn('9.9.9.1', self.published())
                self.audit(now)
        self.assertFalse(self.run_update(NOW + timedelta(hours=3)))
        self.assertEqual(self.full()['protection']['github_meta']['status'], 'ok')
        self.audit(NOW + timedelta(hours=3))

    def test_meta_without_baseline_is_missing_but_static_protection_applies(self):
        self.protect(['9.9.9.0/30'])
        self.assertTrue(self.run_update(meta=OSError('offline')))
        github = self.full()['protection']['github_meta']
        self.assertEqual((github['status'], github['last_success']), ('missing', None))
        self.assertNotIn('9.9.9.1', self.published())
        self.audit()

    def test_published_protected_address_is_rejected(self):
        self.protect(['8.8.4.0/30'], meta=False)
        self.run_update()
        with (self.root / 'generated/combined.ipv4').open('a') as output:
            output.write('8.8.4.1\n')
        with self.assertRaisesRegex(ValueError, 'protected infrastructure'):
            self.audit()

    def test_tampered_github_snapshot_is_rejected(self):
        self.protect()
        self.run_update()
        path = self.root / 'generated/protected-github.ipv4'
        path.write_text(path.read_text().replace('9.9.9.0/30\n', ''))
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            self.audit()

    def test_new_protection_requires_regeneration_and_rebuild_applies_it(self):
        self.run_update()
        self.assertIn('9.9.9.1', self.published())
        self.protect(['9.9.9.0/30'])
        with self.assertRaisesRegex(ValueError, 'protect'):
            self.audit()
        rebuild(self.root)
        self.assertNotIn('9.9.9.1', self.published())
        self.assertEqual(self.full()['protection']['github_meta']['status'], 'missing')
        self.audit()
        # The next update fetches GitHub meta and replaces the offline placeholder.
        self.assertFalse(self.run_update(NOW + timedelta(hours=1)))
        self.assertEqual(self.full()['protection']['github_meta']['status'], 'ok')
        self.audit(NOW + timedelta(hours=1))


class ProtectedRepositoryTests(unittest.TestCase):
    def test_router_can_always_reach_github_and_dns(self):
        shield = load_protected(ROOT)
        must_protect = ('185.199.108.133', '185.199.109.133', '185.199.110.133', '185.199.111.133',
                        '140.82.121.3', '140.82.121.4', '1.1.1.1', '8.8.8.8', '9.9.9.9')
        import ipaddress
        for address in must_protect:
            with self.subTest(address=address):
                self.assertTrue(any(ipaddress.ip_address(address) in n for n in shield['networks']))
        published = {ipaddress.ip_network(line) for line in (ROOT / 'generated/combined.ipv4').read_text().splitlines()
                     if line and not line.startswith('#')}
        self.assertFalse(overlaps(published, shield['networks']))


if __name__ == '__main__':
    unittest.main()
