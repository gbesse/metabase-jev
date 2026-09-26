"""Run a Metabase saved question and add bounded semantic decisions."""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from jev_common import JevClient

def classify_card(base_url, card_id, field, question, *, threshold=0.8, limit=100, fetch=None, client=None):
    parsed = urllib.parse.urlparse(base_url)
    if parsed.scheme != 'https' and not (parsed.scheme == 'http' and parsed.hostname in ('localhost','127.0.0.1')):
        raise ValueError('Metabase URL must be HTTPS or loopback HTTP')
    if not 1 <= limit <= 1000 or not str(card_id).isdigit():
        raise ValueError('Invalid card ID or limit')
    key = os.environ.get('METABASE_API_KEY')
    if not key and fetch is None:
        raise ValueError('METABASE_API_KEY is required')
    url = base_url.rstrip('/') + '/api/card/' + str(card_id) + '/query/json'
    if fetch is None:
        request = urllib.request.Request(url, data=b'{}', headers={'x-api-key': key, 'Content-Type':'application/json'}, method='POST')
        with urllib.request.urlopen(request, timeout=20) as response:
            rows = json.load(response)
    else:
        rows = fetch(url)
    if not isinstance(rows, list) or len(rows) > limit:
        raise ValueError('Metabase result exceeds row limit')
    judge = client or JevClient(question, threshold=threshold, max_calls=limit)
    for row in rows:
        if not isinstance(row, dict) or any(k in row for k in ('jev_route','jev_probability','jev_state_sha256')):
            raise ValueError('Invalid or already classified row')
        result = judge.decide(row.get(field))
        yield dict(row, jev_route=result['route'], jev_probability=result['probability'], jev_state_sha256=result['state_sha256'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--card-id', required=True)
    parser.add_argument('--field', required=True)
    parser.add_argument('--question', required=True)
    args = parser.parse_args()
    try:
        for row in classify_card(args.url, args.card_id, args.field, args.question):
            print(json.dumps(row, ensure_ascii=False))
    except (ValueError, OSError) as exc:
        print(type(exc).__name__ + ': ' + str(exc), file=sys.stderr)
        raise SystemExit(1)

if __name__ == '__main__':
    main()
