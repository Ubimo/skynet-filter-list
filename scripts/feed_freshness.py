"""Provider timestamps are independent of successful HTTP retrieval."""
from datetime import datetime, timedelta, timezone
import json
import re


class StaleSourceError(ValueError):
    def __init__(self, message, updated):
        super().__init__(message)
        self.updated = updated


def metadata(body, feed, now):
    policy = feed.get('freshness')
    if not policy:
        return {'upstream_updated_at': None, 'upstream_deadline': None, 'attribution': []}
    kind = policy['type']
    attribution = []
    if kind == 'spamhaus_json':
        rows = [json.loads(line) for line in body.splitlines() if line.strip()]
        meta = [row for row in rows if row.get('type') == 'metadata']
        if len(meta) != 1 or meta[0]['records'] != sum('cidr' in row for row in rows):
            raise ValueError('Missing/inconsistent Spamhaus metadata')
        row = meta[0]
        updated = datetime.fromtimestamp(row['timestamp'], timezone.utc)
        for key in ('copyright', 'terms'):
            if not isinstance(row.get(key), str) or not row[key].strip() or '\n' in row[key] or '\r' in row[key]:
                raise ValueError('Invalid Spamhaus attribution')
        attribution = [row['copyright'], 'Terms: ' + row['terms'], 'Source: ' + feed['url'],
                       'Upstream updated: ' + updated.isoformat(timespec='seconds')]
    elif kind == 'iso_comment':
        match = re.search(r'^#\s*Last updated:\s*(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC', body, re.M)
        if not match:
            raise ValueError('Missing provider Last updated timestamp')
        updated = datetime.strptime(match[1], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    elif kind == 'firehol':
        match = re.search(r'^# Source File Date:\s*(.+?)\s*$', body, re.M)
        if not match:
            raise ValueError('Missing FireHOL upstream Source File Date')
        updated = datetime.strptime(match[1], '%a %b %d %H:%M:%S UTC %Y').replace(tzinfo=timezone.utc)
    else:
        raise ValueError('Unknown freshness parser')
    deadline = updated + timedelta(hours=policy['max_age_hours'])
    if updated > now + timedelta(minutes=5):
        raise ValueError('Provider timestamp is in the future')
    if deadline < now:
        raise StaleSourceError(f'Upstream data expired: {updated.isoformat()} (limit {policy["max_age_hours"]}h)', updated)
    return {'upstream_updated_at': updated.isoformat(timespec='seconds'),
            'upstream_deadline': deadline.isoformat(timespec='seconds'), 'attribution': attribution}


def fallback_fresh(record, feed, now):
    if not feed.get('freshness'):
        return True
    try:
        updated = datetime.fromisoformat(record['upstream_updated_at'])
        # Recompute from current policy, rather than trusting a saved deadline.
        return updated <= now + timedelta(minutes=5) and now <= updated + timedelta(hours=feed['freshness']['max_age_hours'])
    except (KeyError, TypeError, ValueError):
        return False
