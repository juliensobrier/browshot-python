#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) Julien Sobrier
#
# This file is part of printio released under MIT license.
# See the LICENSE for more information.
"""

Test the library.

"""

import os
import sys
import unittest
#import datetime

libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not libpath in sys.path:
    sys.path.insert(1, libpath)
    print(libpath)
del libpath

from browshot import BrowshotClient



class BrowshotClient_ParseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = BrowshotClient('vPTtKKLBtPUNxVwwfEKlVvekuxHyTXyi')
        #self.client.debug = 1


    def test_api_version(self):
        self.assertEqual('1.21', self.client.api_version())

    def test_simple(self):
        data = self.client.simple('http://mobilito.net/', {'cache': 60 * 60 * 24 * 365})
        #data = self.client.simple({'url': 'http://mobilito.net'})
        self.assertEqual(200,  data['code'])
        self.assertEqual(True, len(data['png']) > 0)

        # Fail
        data = self.client.simple('')
        # self.assertEqual(400,  data['code'])
        with open(os.path.join(os.path.dirname(__file__), 'fail.png'), mode='rb') as fail_image:
            self.assertEqual(fail_image.read(), data['png'])


    #def test_simple_file(self):
        #data = self.client.simple_file('http://mobilito.net/', '/tmp/mobilito.png', {'cache': 60 * 60 * 24 * 365})
        #self.assertEqual(200,                  data['code'])
        #self.assertEqual('/tmp/mobilito.png',  data['file'])


    def test_instance_list(self):
        instances = self.client.instance_list()

        self.assertEqual(True, 'free' in instances)
        self.assertEqual(True, len(instances['free']) > 0)

        self.assertEqual(True, 'shared' in instances)
        self.assertEqual(True, len(instances['shared']) > 0)

        self.assertEqual(True, 'private' in instances)
        self.assertEqual(1,    len(instances['private']))

        free = instances['free'][0]
        self.assertEqual(True, 'id' in free)
        self.assertEqual(True, 'width' in free)
        self.assertEqual(True, 'height' in free)
        self.assertEqual(True, 'load' in free)
        self.assertEqual(True, 'browser' in free)
        self.assertEqual(True, 'id' in free['browser'])
        self.assertEqual(True, 'name' in free['browser'])
        self.assertEqual(True, 'javascript' in free['browser'])
        self.assertEqual(True, 'flash' in free['browser'])
        self.assertEqual(True, 'mobile' in free['browser'])
        self.assertEqual(True, 'type' in free)
        self.assertEqual(True, 'screenshot_cost' in free)
        self.assertEqual(0,    int(free['screenshot_cost']))


    def test_instance_info(self):
        instances = self.client.instance_list()
        free = instances['free'][0]
		
        instance = self.client.instance_info(free['id'])
        self.assertEqual(free['id'], instance['id'])
        self.assertEqual(int(free['width']), int(instance['width']))
        self.assertEqual(int(free['height']), int(instance['height']))
        #self.assertEqual(free['load'], instance['load']) # can change
        self.assertEqual(free['browser']['id'], instance['browser']['id'])
        self.assertEqual(free['browser']['name'], instance['browser']['name'])
        self.assertEqual(free['browser']['javascript'], instance['browser']['javascript'])
        self.assertEqual(free['browser']['flash'], instance['browser']['flash'])
        self.assertEqual(int(free['browser']['mobile']), int(instance['browser']['mobile']))
        self.assertEqual(free['type'], instance['type'])
        self.assertEqual(int(free['screenshot_cost']), int(instance['screenshot_cost']))


    def test_instance_info_wrong(self):
        instance = self.client.instance_info(-1)

        self.assertEqual(True, 'error' in instance)
        self.assertEqual(True, 'status' in instance)


    def test_browser_list(self):
        browsers = self.client.browser_list()
        self.assertEqual(True, len(browsers.keys()) > 0)

        browser_id = list(browsers.keys())[0] # In Python 3 dict.keys() returns an iterable but not indexable object.
        self.assertEqual(True, int(browser_id) > 0)

        browser = browsers[browser_id]
        self.assertEqual(True, 'name' in browser)
        self.assertEqual(True, 'user_agent' in browser)
        self.assertEqual(True, 'appname' in browser)
        self.assertEqual(True, 'vendorsub' in browser)
        self.assertEqual(True, 'appcodename' in browser)
        self.assertEqual(True, 'platform' in browser)
        self.assertEqual(True, 'vendor' in browser)
        self.assertEqual(True, 'appversion' in browser)
        self.assertEqual(True, 'javascript' in browser)
        self.assertEqual(True, 'mobile' in browser)
        self.assertEqual(True, 'flash' in browser)


    def test_screenshot_create_wrong(self):
        screenshot = self.client.screenshot_create()
        self.assertEqual(True, 'error' in screenshot)

        screenshot = self.client.screenshot_create('-')
        self.assertEqual(True, 'error' in screenshot)


    def test_screenshot_create(self):
        screenshot = self.client.screenshot_create('http://browshot.com/')

        self.assertEqual(True, 'id' in screenshot)
        self.assertEqual(True, 'status' in screenshot)
        self.assertEqual(True, 'priority' in screenshot)

        if screenshot['status'] == 'finished':
            self.assertEqual(True, 'screenshot_url' in screenshot)
            self.assertEqual(True, 'url' in screenshot)
            self.assertEqual(True, 'size' in screenshot)
            self.assertEqual(True, 'width' in screenshot)
            self.assertEqual(True, 'height' in screenshot)
            self.assertEqual(True, 'request_time' in screenshot)
            self.assertEqual(True, 'started' in screenshot)
            self.assertEqual(True, 'load' in screenshot)
            self.assertEqual(True, 'content' in screenshot)
            self.assertEqual(True, 'finished' in screenshot)
            self.assertEqual(True, 'instance_id' in screenshot)
            self.assertEqual(True, 'response_code' in screenshot)
            self.assertEqual(True, 'final_url' in screenshot)
            self.assertEqual(True, 'content_type' in screenshot)
            self.assertEqual(True, 'scale' in screenshot)
            self.assertEqual(True, 'cost' in screenshot)


    def test_screenshot_info_wrong(self):
        screenshot = self.client.screenshot_info()
        self.assertEqual(True, 'error' in screenshot)


    def test_screenshot_info(self):
        screenshot = self.client.screenshot_create('http://browshot.com/')
        info  = self.client.screenshot_info(screenshot['id'])
		
        self.assertEqual(True, 'id' in info)
        self.assertEqual(True, 'status' in info)
        self.assertEqual(True, 'priority' in info)

        if info['status'] == 'finished':
            self.assertEqual(True, 'screenshot_url' in info)
            self.assertEqual(True, 'url' in info)
            self.assertEqual(True, 'size' in info)
            self.assertEqual(True, 'width' in info)
            self.assertEqual(True, 'height' in info)
            # self.assertEqual(True, 'request_time' in info)
            # self.assertEqual(True, 'started' in info)
            # self.assertEqual(True, 'load' in info)
            # self.assertEqual(True, 'content' in info)
            # self.assertEqual(True, 'finished' in info)
            self.assertEqual(True, 'instance_id' in info)
            # self.assertEqual(True, 'response_code' in info)
            self.assertEqual(True, 'final_url' in info)
            # self.assertEqual(True, 'content_type' in info)
            self.assertEqual(True, 'scale' in info)
            self.assertEqual(True, 'cost' in info)
            self.assertEqual(False, 'images' in info)
            self.assertEqual(False, 'scripts' in info)

    def test_screenshot_info_0(self):
        screenshot = self.client.screenshot_create('http://browshot.com/')
        info  = self.client.screenshot_info(screenshot['id'], { 'details' :  0 })

        self.assertEqual(True, 'id' in info)
        self.assertEqual(True, 'status' in info)
        self.assertEqual(True, 'priority' in info)

        if info['status'] == 'finished':
            self.assertEqual(True, 'screenshot_url' in info)
            self.assertEqual(True, 'url' in info)
            self.assertEqual(True, 'size' in info)
            self.assertEqual(True, 'width' in info)
            self.assertEqual(True, 'height' in info)
            self.assertEqual(True, 'instance_id' in info)
            self.assertEqual(True, 'final_url' in info)
            self.assertEqual(True, 'scale' in info)
            self.assertEqual(True, 'cost' in info)

            self.assertEqual(False, 'response_code' in info)
            self.assertEqual(False, 'content_type' in info)

            self.assertEqual(False, 'started' in info)
            self.assertEqual(False, 'finished' in info)
            self.assertEqual(False, 'load' in info)
            self.assertEqual(False, 'request_time' in info)
            self.assertEqual(False, 'content' in info)

            self.assertEqual(False, 'images' in info)
            self.assertEqual(False, 'scripts' in info)
            self.assertEqual(False, 'iframes' in info)

    def test_screenshot_info_1(self):
        screenshot = self.client.screenshot_create('http://browshot.com/')
        info  = self.client.screenshot_info(screenshot['id'], { 'details' :  1 })

        self.assertEqual(True, 'id' in info)
        self.assertEqual(True, 'status' in info)
        self.assertEqual(True, 'priority' in info)

        if info['status'] == 'finished':
            self.assertEqual(True, 'screenshot_url' in info)
            self.assertEqual(True, 'url' in info)
            self.assertEqual(True, 'size' in info)
            self.assertEqual(True, 'width' in info)
            self.assertEqual(True, 'height' in info)
            self.assertEqual(True, 'instance_id' in info)
            self.assertEqual(True, 'final_url' in info)
            self.assertEqual(True, 'scale' in info)
            self.assertEqual(True, 'cost' in info)

            self.assertEqual(True, 'response_code' in info)
            self.assertEqual(True, 'content_type' in info)

            self.assertEqual(False, 'started' in info)
            self.assertEqual(False, 'finished' in info)
            self.assertEqual(False, 'load' in info)
            self.assertEqual(False, 'request_time' in info)
            self.assertEqual(False, 'content' in info)

            self.assertEqual(False, 'images' in info)
            self.assertEqual(False, 'scripts' in info)
            self.assertEqual(False, 'iframes' in info)

    def test_screenshot_info_2(self):
        screenshot = self.client.screenshot_create('http://browshot.com/')
        info  = self.client.screenshot_info(screenshot['id'], { 'details' :  2 })

        self.assertEqual(True, 'id' in info)
        self.assertEqual(True, 'status' in info)
        self.assertEqual(True, 'priority' in info)

        if info['status'] == 'finished':
            self.assertEqual(True, 'screenshot_url' in info)
            self.assertEqual(True, 'url' in info)
            self.assertEqual(True, 'size' in info)
            self.assertEqual(True, 'width' in info)
            self.assertEqual(True, 'height' in info)
            self.assertEqual(True, 'instance_id' in info)
            self.assertEqual(True, 'final_url' in info)
            self.assertEqual(True, 'scale' in info)
            self.assertEqual(True, 'cost' in info)

            self.assertEqual(True, 'response_code' in info)
            self.assertEqual(True, 'content_type' in info)

            self.assertEqual(True, 'started' in info)
            self.assertEqual(True, 'finished' in info)
            self.assertEqual(True, 'load' in info)
            self.assertEqual(True, 'request_time' in info)
            self.assertEqual(True, 'content' in info)

            self.assertEqual(False, 'images' in info)
            self.assertEqual(False, 'scripts' in info)
            self.assertEqual(False, 'iframes' in info)

    #def test_screenshot_info_3(self):
        #screenshot = self.client.screenshot_create('http://browshot.com/')
        #info  = self.client.screenshot_info(screenshot['id'], { 'details' :  3 })

        #self.assertEqual(True, 'id' in info)
        #self.assertEqual(True, 'status' in info)
        #self.assertEqual(True, 'priority' in info)

        #if info['status'] == 'finished':
            #self.assertEqual(True, 'screenshot_url' in info)
            #self.assertEqual(True, 'url' in info)
            #self.assertEqual(True, 'size' in info)
            #self.assertEqual(True, 'width' in info)
            #self.assertEqual(True, 'height' in info)
            #self.assertEqual(True, 'instance_id' in info)
            #self.assertEqual(True, 'final_url' in info)
            #self.assertEqual(True, 'scale' in info)
            #self.assertEqual(True, 'cost' in info)

            #self.assertEqual(True, 'response_code' in info)
            #self.assertEqual(True, 'content_type' in info)

            #self.assertEqual(True, 'started' in info)
            #self.assertEqual(True, 'finished' in info)
            #self.assertEqual(True, 'load' in info)
            #self.assertEqual(True, 'request_time' in info)
            #self.assertEqual(True, 'content' in info)

            #self.assertEqual(True, 'images' in info)
            #self.assertEqual(True, 'scripts' in info)
            #self.assertEqual(True, 'iframes' in info)


    def test_screenshot_list(self):
        screenshots = self.client.screenshot_list()
        self.assertEqual(True, len(screenshots.keys()) > 0)

        screenshot_id = list(screenshots.keys())[0]
        self.assertEqual(True, int(screenshot_id) > 0)

        screenshot = screenshots[screenshot_id]
		
        self.assertEqual(True, 'id' in screenshot)
        self.assertEqual(True, 'status' in screenshot)
        self.assertEqual(True, 'priority' in screenshot)

        if screenshot['status'] == 'finished':
            self.assertEqual(True, 'screenshot_url' in screenshot)
            self.assertEqual(True, 'url' in screenshot)
            self.assertEqual(True, 'size' in screenshot)
            self.assertEqual(True, 'width' in screenshot)
            self.assertEqual(True, 'height' in screenshot)
            # self.assertEqual(True, 'request_time' in screenshot)
            # self.assertEqual(True, 'started' in screenshot)
            # self.assertEqual(True, 'load' in screenshot)
            # self.assertEqual(True, 'content' in screenshot)
            # self.assertEqual(True, 'finished' in screenshot)
            self.assertEqual(True, 'instance_id' in screenshot)
            # self.assertEqual(True, 'response_code' in screenshot)
            self.assertEqual(True, 'final_url' in screenshot)
            # self.assertEqual(True, 'content_type' in screenshot)
            self.assertEqual(True, 'scale' in screenshot)
            self.assertEqual(True, 'cost' in screenshot)


    def test_thumbnail(self):
        screenshots = self.client.screenshot_list()
        self.assertEqual(True, len(screenshots.keys()) > 0)

        screenshot_id = list(screenshots.keys())[0]
        self.assertEqual(True, int(screenshot_id) > 0)

        thumbnail = self.client.screenshot_thumbnail(screenshot_id)
        self.assertEqual(True, thumbnail != '')
        self.assertEqual(b'PNG', thumbnail[1:4])


    def test_screenshot_share(self):
        share = self.client.screenshot_host(0)
        self.assertEqual('error', share['status'])

    def test_screenshot_search(self):
        screenshots = self.client.screenshot_search('google')
        self.assertEqual(True, len(screenshots.keys()) > 0)

        screenshot_id = list(screenshots.keys())[0]
        self.assertEqual(True, int(screenshot_id) > 0)

        screenshot = screenshots[screenshot_id]
		
        self.assertEqual(True, 'id' in screenshot)
        self.assertEqual(True, 'status' in screenshot)
        self.assertEqual(True, 'priority' in screenshot)

        if screenshot['status'] == 'finished':
            self.assertEqual(True, 'screenshot_url' in screenshot)
            self.assertEqual(True, 'url' in screenshot)
            self.assertEqual(True, 'size' in screenshot)
            self.assertEqual(True, 'width' in screenshot)
            self.assertEqual(True, 'height' in screenshot)
            self.assertEqual(True, 'request_time' in screenshot)
            self.assertEqual(True, 'started' in screenshot)
            self.assertEqual(True, 'load' in screenshot)
            self.assertEqual(True, 'content' in screenshot)
            self.assertEqual(True, 'finished' in screenshot)
            self.assertEqual(True, 'instance_id' in screenshot)
            self.assertEqual(True, 'response_code' in screenshot)
            self.assertEqual(True, 'final_url' in screenshot)
            self.assertEqual(True, 'content_type' in screenshot)
            self.assertEqual(True, 'scale' in screenshot)
            self.assertEqual(True, 'cost' in screenshot)

    def test_hosting(self):
        screenshots = self.client.screenshot_list()
        self.assertEqual(True, len(screenshots.keys()) > 0)

        screenshot_id = list(screenshots.keys())[0]
        self.assertEqual(True, int(screenshot_id) > 0)

        hosting = self.client.screenshot_host(screenshot_id)
        self.assertEqual('error', hosting['status'])

        hosting = self.client.screenshot_host(screenshot_id, { 'hosting' : 'browshot' })
        self.assertEqual('error', hosting['status'])

        hosting = self.client.screenshot_host(screenshot_id, { 'hosting' : 's3' })
        self.assertEqual('error', hosting['status'])

        hosting = self.client.screenshot_host(screenshot_id, { 'hosting' : 's3', 'bucket' : 'mine' })
        self.assertEqual('error', hosting['status'])


    def test_account_info(self):
        account = self.client.account_info()

        self.assertEqual(True, 'balance' in account)
        self.assertEqual(0,  int(account['balance']))
        self.assertEqual(True, 'active' in account)
        self.assertEqual(1,  int(account['active']))
        #self.assertEqual(True, 'instances' in account)

    def test_account_info_wrong(self):
        client = BrowshotClient()
        #client.debug = True
        account = client.account_info()

        self.assertEqual(True, 'error' in account)


if __name__ == "__main__":
    unittest.main()