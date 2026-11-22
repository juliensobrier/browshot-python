import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from browshot import BrowshotClient


@unittest.skipUnless(os.environ.get('BROWSHOT_API_KEY'), 'Set BROWSHOT_API_KEY for live tests')
class BrowshotLiveTestCase(unittest.TestCase):
    def setUp(self):
        self.client = BrowshotClient(os.environ['BROWSHOT_API_KEY'])

    def fixture_id(self, format):
        id = os.environ.get('BROWSHOT_' + format.upper() + '_ID')
        if not id:
            self.skipTest('Set BROWSHOT_' + format.upper() + '_ID to an owned capture')
        return id

    def test_account_catalog_and_browser_info(self):
        self.assertIn('balance', self.client.account_info())
        catalog = self.client.instance_list()
        self.assertTrue(catalog['free'])
        self.assertTrue(catalog['shared'])
        profile = self.client.instance_info(catalog['free'][0]['id'])
        self.assertEqual(0, profile['screenshot_cost'])
        browsers = self.client.browser_list()
        first_id = next(iter(browsers))
        self.assertEqual(browsers[first_id]['name'], self.client.browser_info(first_id)['name'])

    def test_native_country_instances_cost_one_credit(self):
        instances = {instance['id']: instance for instance in self.client.instance_list()['shared']}
        countries = ('France', 'India', 'Finland', 'United Kingdom')
        for id in range(373, 389):
            with self.subTest(id=id):
                self.assertEqual(countries[(id - 373) // 4], instances[id]['country'])
                self.assertEqual(1, instances[id]['screenshot_cost'])

    def test_screenshot_metadata_and_thumbnail(self):
        id = self.fixture_id('screenshot')
        details = self.client.screenshot_info(id, {'details': 2})
        self.assertEqual('finished', details['status'])
        self.assertEqual(id, str(details['id']))
        self.assertTrue(self.client.screenshot_list({'limit': 1}))
        matches = self.client.screenshot_search(details['url'])
        self.assertIn(id, matches)
        png = self.client.screenshot_thumbnail(id, {'width': 64})
        self.assertTrue(png.startswith(b'\x89PNG\r\n\x1a\n'))

    def test_retina_and_ad_blocking_metadata(self):
        id = self.fixture_id('retina')
        details = self.client.screenshot_info(id, {'details': 1})
        self.assertEqual('finished', details['status'])
        self.assertEqual(2, details['device_scale'])
        self.assertEqual(1, details['hide_ads'])

    def test_pdf(self):
        self.check_artifact('pdf', b'%PDF-')

    def test_webm(self):
        self.check_artifact('webm', b'\x1a\x45\xdf\xa3')

    def test_mp4(self):
        self.check_artifact('mp4', b'ftyp', offset=4)

    def test_gif(self):
        self.check_artifact('gif', b'GIF8')

    def check_artifact(self, format, signature, offset=0):
        id = self.fixture_id(format)
        kind = 'pdf' if format == 'pdf' else 'video'
        download = getattr(self.client, 'screenshot_' + kind)
        save = getattr(self.client, 'screenshot_' + kind + '_file')

        info = self.client.screenshot_info(id)
        self.assertEqual('finished', info['status'])
        self.assertEqual(1, info[kind])
        self.assertTrue(info[kind + '_url'])
        content = download(id)
        self.assertEqual(signature, content[offset:offset + len(signature)])
        with TemporaryDirectory() as directory:
            file = Path(directory, 'fixture.' + format)
            self.assertEqual(file, save(id, file))
            self.assertEqual(content, file.read_bytes())

    def test_json_validation_errors_and_unavailable_downloads(self):
        self.assertIn('error', self.client.instance_info(-1))
        self.assertIn('error', self.client.screenshot_create('http://', {'instance_id': 12}))
        invalid = BrowshotClient('invalid-test-key')
        for client in (self.client, invalid):
            self.assertEqual(b'', client.screenshot_pdf(1))
            self.assertEqual(b'', client.screenshot_video(1))


if __name__ == '__main__':
    unittest.main()
