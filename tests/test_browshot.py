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
del libpath

from browshot import BrowshotClient


class BrowshotClient_ParseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = BrowshotClient('vPTtKKLBtPUNxVwwfEKlVvekuxHyTXyi')
        #self.client.debug = 1


    def test_api_version(self):
        self.assertEquals('1.4', self.client.api_version())

    def test_simple(self):
        data = self.client.simple('http://mobilito.net/', {'cache': 60 * 60 * 24 * 365})
        #data = self.client.simple({'url': 'http://mobilito.net'})
        self.assertEquals(200,  data['code'])
        self.assertEquals(True, len(data['png']) > 0)
        
        # Fail
        data = self.client.simple('http://')
        self.assertEquals(400,  data['code'])
        self.assertEquals('',    data['png'])


    #def test_simple_file(self):
        #data = self.client.simple_file('http://mobilito.net/', '/tmp/mobilito.png', {'cache': 60 * 60 * 24 * 365})
        #self.assertEquals(200,                  data['code'])
        #self.assertEquals('/tmp/mobilito.png',  data['file'])


    def test_instance_list(self):
        instances = self.client.instance_list()

        self.assertEquals(True, 'free' in instances)
        self.assertEquals(True, len(instances['free']) > 0)

        self.assertEquals(True, 'shared' in instances)
        self.assertEquals(True, len(instances['shared']) > 0)

        self.assertEquals(True, 'private' in instances)
        self.assertEquals(0,    len(instances['private']))

        free = instances['free'][0]
        self.assertEquals(True, 'id' in free)
        self.assertEquals(True, 'width' in free)
        self.assertEquals(True, 'height' in free)
        self.assertEquals(True, 'load' in free)
        self.assertEquals(True, 'browser' in free)
        self.assertEquals(True, 'id' in free['browser'])
        self.assertEquals(True, 'name' in free['browser'])
        self.assertEquals(True, 'javascript' in free['browser'])
        self.assertEquals(True, 'flash' in free['browser'])
        self.assertEquals(True, 'mobile' in free['browser'])
        self.assertEquals(True, 'type' in free)
        self.assertEquals(True, 'active' in free)
        self.assertEquals(1,    int(free['active']))
        self.assertEquals(True, 'screenshot_cost' in free)
        self.assertEquals(0,    int(free['screenshot_cost']))


    def test_instance_info(self):
        instances = self.client.instance_list()
        free = instances['free'][0]
		
        instance = self.client.instance_info(free['id'])
        self.assertEquals(free['id'], instance['id'])
        self.assertEquals(free['width'], instance['width'])
        self.assertEquals(free['height'], instance['height'])
        self.assertEquals(free['load'], instance['load'])
        self.assertEquals(free['browser']['id'], instance['browser']['id'])
        self.assertEquals(free['browser']['name'], instance['browser']['name'])
        self.assertEquals(free['browser']['javascript'], instance['browser']['javascript'])
        self.assertEquals(free['browser']['flash'], instance['browser']['flash'])
        self.assertEquals(free['browser']['mobile'], instance['browser']['mobile'])
        self.assertEquals(free['type'], instance['type'])
        self.assertEquals(free['active'], instance['active'])
        self.assertEquals(free['screenshot_cost'], instance['screenshot_cost'])


    def test_instance_info_wrong(self):
        instance = self.client.instance_info(-1)

        self.assertEquals(True, 'error' in instance)
        self.assertEquals(True, 'status' in instance)


    def test_instance_create_wrong(self):
        instance = self.client.instance_create({'width': 3000})
        self.assertEquals(True, 'error' in instance)

        instance = self.client.instance_create({'height': 3000})
        self.assertEquals(True, 'error' in instance)

        instance = self.client.instance_create({'browser_id': -1})
        self.assertEquals(True, 'error' in instance)

	# Instances are not really crerated for test account, the reply may not match the request arguments
    def test_instance_create(self):
        instance = self.client.instance_create()
        self.assertEquals(True, 'id' in instance)
        self.assertEquals(True, 'width' in instance)
        self.assertEquals(True, 'height' in instance)
        self.assertEquals(True, 'active' in instance)
        self.assertEquals(1,    int(instance['active']))
        self.assertEquals(True, 'browser' in instance)
        self.assertEquals(True, 'id' in instance['browser'])


    def test_browser_list(self):
        browsers = self.client.browser_list()
        self.assertEquals(True, len(browsers.keys()) > 0)

        browser_id = browsers.keys()[0]
        self.assertEquals(True, browser_id > 0)

        browser = browsers[browser_id]
        self.assertEquals(True, 'name' in browser)
        self.assertEquals(True, 'user_agent' in browser)
        self.assertEquals(True, 'appname' in browser)
        self.assertEquals(True, 'vendorsub' in browser)
        self.assertEquals(True, 'appcodename' in browser)
        self.assertEquals(True, 'platform' in browser)
        self.assertEquals(True, 'vendor' in browser)
        self.assertEquals(True, 'appversion' in browser)
        self.assertEquals(True, 'javascript' in browser)
        self.assertEquals(True, 'mobile' in browser)
        self.assertEquals(True, 'flash' in browser)


    # browser is not actually created for test account, so the reply may not match our parameters
    def test_browser_create(self):
        browser = self.client.browser_create({'mobile': 1, 'flash': 1, 'user_agent': 'test'});
        self.assertEquals(True, 'name' in browser)
        self.assertEquals(True, 'user_agent' in browser)
        self.assertEquals(True, 'appname' in browser)
        self.assertEquals(True, 'vendorsub' in browser)
        self.assertEquals(True, 'appcodename' in browser)
        self.assertEquals(True, 'platform' in browser)
        self.assertEquals(True, 'vendor' in browser)
        self.assertEquals(True, 'appversion' in browser)
        self.assertEquals(True, 'javascript' in browser)
        self.assertEquals(True, 'mobile' in browser)
        self.assertEquals(True, 'flash' in browser)

    def test_screenshot_create_wrong(self):
        screenshot = self.client.screenshot_create()
        self.assertEquals(True, 'error' in screenshot)

        screenshot = self.client.screenshot_create('-')
        self.assertEquals(True, 'error' in screenshot)


    def test_screenshot_create(self):
        screenshot = self.client.screenshot_create('http://browshot.com/')

        self.assertEquals(True, 'id' in screenshot)
        self.assertEquals(True, 'status' in screenshot)
        self.assertEquals(True, 'priority' in screenshot)

        if screenshot['status'] == 'finished':
            self.assertEquals(True, 'screenshot_url' in screenshot)
            self.assertEquals(True, 'url' in screenshot)
            self.assertEquals(True, 'size' in screenshot)
            self.assertEquals(True, 'width' in screenshot)
            self.assertEquals(True, 'height' in screenshot)
            self.assertEquals(True, 'request_time' in screenshot)
            self.assertEquals(True, 'started' in screenshot)
            self.assertEquals(True, 'load' in screenshot)
            self.assertEquals(True, 'content' in screenshot)
            self.assertEquals(True, 'finished' in screenshot)
            self.assertEquals(True, 'instance_id' in screenshot)
            self.assertEquals(True, 'response_code' in screenshot)
            self.assertEquals(True, 'final_url' in screenshot)
            self.assertEquals(True, 'content_type' in screenshot)
            self.assertEquals(True, 'scale' in screenshot)
            self.assertEquals(True, 'cost' in screenshot)


    def test_screenshot_info_wrong(self):
        screenshot = self.client.screenshot_info()
        self.assertEquals(True, 'error' in screenshot)


    def test_screenshot_info(self):
        screenshot = self.client.screenshot_create('http://browshot.com/')
        info  = self.client.screenshot_info(screenshot['id'])
		
        self.assertEquals(True, 'id' in info)
        self.assertEquals(True, 'status' in info)
        self.assertEquals(True, 'priority' in info)

        if info['status'] == 'finished':
            self.assertEquals(True, 'screenshot_url' in info)
            self.assertEquals(True, 'url' in info)
            self.assertEquals(True, 'size' in info)
            self.assertEquals(True, 'width' in info)
            self.assertEquals(True, 'height' in info)
            self.assertEquals(True, 'request_time' in info)
            self.assertEquals(True, 'started' in info)
            self.assertEquals(True, 'load' in info)
            self.assertEquals(True, 'content' in info)
            self.assertEquals(True, 'finished' in info)
            self.assertEquals(True, 'instance_id' in info)
            self.assertEquals(True, 'response_code' in info)
            self.assertEquals(True, 'final_url' in info)
            self.assertEquals(True, 'content_type' in info)
            self.assertEquals(True, 'scale' in info)
            self.assertEquals(True, 'cost' in info)


    def test_screenshot_list(self):
        screenshots = self.client.screenshot_list()
        self.assertEquals(True, len(screenshots.keys()) > 0)

        screenshot_id = screenshots.keys()[0]
        self.assertEquals(True, screenshot_id > 0)

        screenshot = screenshots[screenshot_id]
		
        self.assertEquals(True, 'id' in screenshot)
        self.assertEquals(True, 'status' in screenshot)
        self.assertEquals(True, 'priority' in screenshot)

        if screenshot['status'] == 'finished':
            self.assertEquals(True, 'screenshot_url' in screenshot)
            self.assertEquals(True, 'url' in screenshot)
            self.assertEquals(True, 'size' in screenshot)
            self.assertEquals(True, 'width' in screenshot)
            self.assertEquals(True, 'height' in screenshot)
            self.assertEquals(True, 'request_time' in screenshot)
            self.assertEquals(True, 'started' in screenshot)
            self.assertEquals(True, 'load' in screenshot)
            self.assertEquals(True, 'content' in screenshot)
            self.assertEquals(True, 'finished' in screenshot)
            self.assertEquals(True, 'instance_id' in screenshot)
            self.assertEquals(True, 'response_code' in screenshot)
            self.assertEquals(True, 'final_url' in screenshot)
            self.assertEquals(True, 'content_type' in screenshot)
            self.assertEquals(True, 'scale' in screenshot)
            self.assertEquals(True, 'cost' in screenshot)

    def test_thumbnail(self):
        pass


    def test_account_info(self):
        account = self.client.account_info()

        self.assertEquals(True, 'balance' in account)
        self.assertEquals(0,  int(account['balance']))
        self.assertEquals(True, 'active' in account)
        self.assertEquals(1,  int(account['active']))
        self.assertEquals(True, 'instances' in account)

    def test_account_info_wrong(self):
        client = BrowshotClient()
        account = client.account_info()

        self.assertEquals(True, 'error' in account)


if __name__ == "__main__":
    unittest.main()