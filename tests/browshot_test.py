from contextlib import redirect_stdout
from io import StringIO
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
import unittest
from urllib.parse import parse_qs, urlsplit

from browshot import BrowshotClient


IMAGE = b'\x89PNG\r\n\x1a\n\x00\x80\xff'


class StubHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        self.reply()

    def do_POST(self):
        self.reply()

    def reply(self):
        request = urlsplit(self.path)
        query = parse_qs(request.query, keep_blank_values=True)
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        status = int(query.get('stub_status', ['200'])[0])
        if status != 200:
            self.send_body(status, 'application/json', b'{"error":"INVALID_REQUEST"}')
        elif request.path.endswith(('/simple', '/thumbnail')):
            self.send_body(200, 'image/png', IMAGE)
        elif request.path.endswith('/html'):
            self.send_body(200, 'text/html', b'<html>Example</html>')
        else:
            response = {
                'method': self.command,
                'path': request.path,
                'query': query,
                'upload': 'https://example.com/' in body.decode('utf-8') if body else False,
                'upload_content_type': self.headers.get('Content-Type', ''),
            }
            self.send_body(200, 'application/json', json.dumps(response).encode('utf-8'))

    def send_body(self, status, content_type, body):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class BrowshotClientTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), StubHandler)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = 'http://127.0.0.1:{}/api/v1/'.format(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.client = BrowshotClient('key & value', 0, self.base)

    def test_api_version(self):
        self.assertEqual('1.29', self.client.api_version())

    def test_catalog_and_account_endpoints(self):
        for path, call in (
            ('account/info', self.client.account_info),
            ('instance/list', self.client.instance_list),
            ('browser/list', self.client.browser_list),
            ('instance/info', lambda: self.client.instance_info(12)),
            ('browser/info', lambda: self.client.browser_info(16)),
        ):
            with self.subTest(path=path):
                response = call()
                self.assertEqual('/api/v1/' + path, response['path'])
                self.assertEqual(['key & value'], response['query']['key'])
                if path in ('instance/info', 'browser/info'):
                    self.assertEqual(['12' if path.startswith('instance') else '16'], response['query']['id'])

    def test_screenshot_endpoints(self):
        for path, call in (
            ('info', self.client.screenshot_info),
            ('host', self.client.screenshot_host),
            ('share', self.client.screenshot_share),
            ('delete', self.client.screenshot_delete),
        ):
            with self.subTest(path=path):
                parameters = {'id': 1, 'details': 2}
                response = call(77, parameters)
                self.assertEqual('/api/v1/screenshot/' + path, response['path'])
                self.assertEqual(['77'], response['query']['id'])
                self.assertEqual(['2'], response['query']['details'])
                self.assertEqual({'id': 1, 'details': 2}, parameters)

        listing = self.client.screenshot_list({'limit': 12})
        self.assertEqual('/api/v1/screenshot/list', listing['path'])
        self.assertEqual(['12'], listing['query']['limit'])
        search = self.client.screenshot_search('example.com/?a=1&b=2')
        self.assertEqual('/api/v1/screenshot/search', search['path'])
        self.assertEqual(['example.com/?a=1&b=2'], search['query']['url'])

    def test_create_encodes_unicode_and_preserves_arguments(self):
        options = {'instance_id': 12, 'cookie': 'scale=é & size=10'}
        url = 'https://example.com/?name=é'
        response = self.client.screenshot_create(url, options)
        self.assertEqual('/api/v1/screenshot/create', response['path'])
        self.assertEqual([url], response['query']['url'])
        self.assertEqual(['scale=é & size=10'], response['query']['cookie'])
        self.assertNotIn('url', options)

    def test_multiple_preserves_repeated_url_and_instance_parameters(self):
        urls = ['https://example.com/', 'https://example.net/?a=1&b=2']
        response = self.client.screenshot_multiple({'urls': urls, 'instances': [12, 65]})
        self.assertEqual('/api/v1/screenshot/multiple', response['path'])
        self.assertEqual(urls, response['query']['url'])
        self.assertEqual(['12', '65'], response['query']['instance_id'])

    def test_crawl_and_batch_metadata(self):
        response = self.client.crawl_create('example.com', 'https://example.com/')
        self.assertEqual('/api/v1/crawl/create', response['path'])
        self.assertEqual(['example.com'], response['query']['domain'])
        self.assertEqual(['https://example.com/'], response['query']['url'])
        for path, call in (('batch/info', self.client.batch_info), ('crawl/info', self.client.crawl_info)):
            with self.subTest(path=path):
                response = call(77)
                self.assertEqual('/api/v1/' + path, response['path'])
                self.assertEqual(['77'], response['query']['id'])

    def test_batch_uploads_the_file_as_multipart(self):
        with TemporaryDirectory() as directory:
            file = Path(directory, 'urls.csv')
            file.write_text('https://example.com/\n', encoding='utf-8')
            response = self.client.batch_create(file, {'instance_id': 12})
        self.assertEqual('POST', response['method'])
        self.assertEqual('/api/v1/batch/create', response['path'])
        self.assertTrue(response['upload_content_type'].startswith('multipart/form-data;'))
        self.assertTrue(response['upload'])
        self.assertEqual(['12'], response['query']['instance_id'])

    def test_simple_and_thumbnail_preserve_bytes(self):
        self.assertEqual({'code': 200, 'png': IMAGE}, self.client.simple('https://example.com/'))
        self.assertEqual(IMAGE, self.client.screenshot_thumbnail(77))
        with TemporaryDirectory() as directory:
            file = Path(directory, 'capture.png')
            self.assertEqual(file, self.client.screenshot_thumbnail_file(77, file))
            self.assertEqual(IMAGE, file.read_bytes())
            self.assertEqual({'code': 200, 'file': file}, self.client.simple_file('https://example.com/', file))
            self.assertEqual(IMAGE, file.read_bytes())

    def test_html_returns_rendered_bytes(self):
        self.assertEqual(b'<html>Example</html>', self.client.screenshot_html(77))

    def test_json_endpoints_preserve_api_error_bodies(self):
        response = self.client.screenshot_info(0, {'stub_status': 400})
        self.assertEqual({'error': 'INVALID_REQUEST'}, response)

    def test_simple_preserves_error_status_and_empty_result(self):
        self.assertEqual({'code': 404, 'png': ''}, self.client.simple('https://example.com/', {'stub_status': 404}))

    def test_debug_output_omits_api_key(self):
        self.client.debug = 1
        output = StringIO()
        with redirect_stdout(output):
            self.client.instance_list()
        self.assertIn('/api/v1/instance/list', output.getvalue())
        self.assertNotIn('key', output.getvalue())


if __name__ == '__main__':
    unittest.main()
