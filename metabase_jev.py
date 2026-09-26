"""Run a Metabase saved question and add bounded semantic decisions."""
import argparse
import json
import os
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path
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
            raw = response.read(5000001)
            if len(raw) > 5000000:
                raise ValueError('Metabase response exceeds 5 MB')
            rows = json.loads(raw)
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

def export_card(rows, *, output=None, strict=False):
    rows = list(rows)
    if strict and any(row['jev_route'] != 'yes' for row in rows):
        raise ValueError('At least one row requires review or failed')
    lines = ''.join(json.dumps(row, ensure_ascii=False, separators=(',', ':')) + '\n' for row in rows)
    if output is None:
        sys.stdout.write(lines)
        return len(rows)
    destination = Path(output)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=destination.parent,
                                     prefix='.jev-', suffix='.tmp', delete=False) as temp:
        temporary = Path(temp.name)
        try:
            temp.write(lines)
            temp.flush()
            os.fsync(temp.fileno())
        except Exception:
            temporary.unlink(missing_ok=True)
            raise
    try:
        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return len(rows)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--card-id', required=True)
    parser.add_argument('--field', required=True)
    parser.add_argument('--question', required=True)
    parser.add_argument('--threshold', type=float, default=0.8)
    parser.add_argument('--limit', type=int, default=100)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()
    try:
        export_card(classify_card(args.url, args.card_id, args.field, args.question,
                                  threshold=args.threshold, limit=args.limit),
                    output=args.output, strict=args.strict)
    except (ValueError, OSError) as exc:
        print(type(exc).__name__ + ': ' + str(exc), file=sys.stderr)
        raise SystemExit(1)

if __name__ == '__main__':
    main()
