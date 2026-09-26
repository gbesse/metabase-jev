import json
import os
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from metabase_jev import classify_card, export_card

class MetabaseTest(unittest.TestCase):
    def test_saved_question_result(self):
        class Client:
            def decide(self, text):
                return {'route':'yes','probability':0.91,'state_sha256':'abc'}
        rows = list(classify_card('https://metabase.example', 7, 'review', 'Good?',
                    fetch=lambda url: [{'review':'great'}], client=Client()))
        self.assertEqual('yes', rows[0]['jev_route'])

    def test_metabase_http_contract_and_atomic_export(self):
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                assert self.path == '/api/card/7/query/json'
                assert self.headers['x-api-key'] == 'test-key'
                body = json.dumps([{'review':'great'}]).encode()
                self.send_response(200)
                self.send_header('Content-Length',str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            def log_message(self, *args):
                pass
        class Client:
            def decide(self, text):
                return {'route':'yes','probability':0.91,'state_sha256':'abc'}
        server = ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread = threading.Thread(target=server.serve_forever,daemon=True)
        thread.start()
        try:
            with patch.dict(os.environ, {'METABASE_API_KEY':'test-key'}), tempfile.TemporaryDirectory() as directory:
                destination = Path(directory) / 'classified.jsonl'
                rows = classify_card(f'http://127.0.0.1:{server.server_port}',7,'review','Good?',client=Client())
                self.assertEqual(1, export_card(rows, output=destination, strict=True))
                self.assertEqual('yes', json.loads(destination.read_text())['jev_route'])
                with self.assertRaises(ValueError):
                    export_card([{'jev_route':'review'}],output=destination,strict=True)
                self.assertEqual('yes', json.loads(destination.read_text())['jev_route'])
        finally:
            server.shutdown()
            server.server_close()
