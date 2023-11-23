# -*- coding: utf-8 -*-
# Copyright 2012 Julien Sobrier
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

""" Version 1.29.0

Python module for Browshot (http://www.browshot.com/), a web service to create website screenshots.

Browshot (http://www.browshot.com/) is a web service to easily make screenshots of web pages in any screen size, as any device: iPhone, iPad, Android, Nook, PC, etc. Browshot has full Flash, JavaScript, CSS, & HTML5 support.

The latest API version is detailed at http://browshot.com/api/documentation. browshot.py follows the API documentation very closely: the function names are similar to the URLs used (screenshot/create becomes screenshot_create(), instance/list becomes instance_list(), etc.), the request arguments are exactly the same, etc.

The library version matches closely the API version it handles: browshot.py 1.0.0 is the first release for the API 1.0, browshot.py 1.1.1 is the second release for the API 1.1, etc.

browshot.py can handle most the API updates within the same major version, e.g. browshot.py 1.0.0 should be compatible with the API 1.1 or 1.2. """


import urllib
from urllib2 import Request, urlopen, URLError, HTTPError
import simplejson
import requests


class BrowshotClient(object):
    def __init__(self, key='', debug=0, base='https://api.browshot.com/api/v1/'):
        """ Create a new BrowshotClient object. You must pass your API key (go to you Dashboard to find your API key, https://browshot.com/dashboard).

        Arguments:
            key:  API key.
            debug: Set to 1 to print debug output to the standard output. 0 (disabled) by default.
            base: Base URL for all API requests. You should use the default base provided by the library. Be careful if you decide to use HTTP instead of HTTPS as your API key could be sniffed and your account could be used without your consent.
        """
        self.key = key
        self.base = base
        self.debug = debug

    def api_version(self):
        """ Return the API version handled by the library. Note that this library can usually handle new arguments in requests without requiring an update. """
        return '1.29'

    def simple(self, url='', parameters={}):
        """ Retrieve a screenshot in one function.

            Note: by default, screenshots are cached for 24 hours. You can tune this valu with the cache=X parameter.

            Arguments:
            See https://browshot.com/api/documentation#simple for the full list of possible arguments.
                url (Required): URL of the screenshot

            Returns {'code': <code>, 'png': <content>}
                <code>: 200 if successful
                <content>: PNG file
        """
        parameters.update({'url': url})
        uri = self.make_url('simple', parameters)
        if self.debug:
            print uri

        try:
            response = urlopen(uri)

            return {'code': 200, 'png': response.read()}
        except HTTPError, e:
            return {'code': e.code, 'png': ''}
        except Exception, e:
            return {'code': 400, 'png': ''}



    def simple_file(self, url='', file='', parameters={}):
        """ Retrieve a screenshot, or a thumbnail, and save it to a fil in one functione.

        Note: by default, screenshots are cached for 24 hours. You can tune this valu with the cache=X parameter.

        Returns {'code': <code>, 'file': <file path}
                <code>: 200 if successful
                <file path>: local file where the screenshot was saved, empty string it if failed

        Arguments:
        See https://browshot.com/api/documentation#simple for the full list of possible arguments.
            url (Required): URL of the screenshot
            file (Required): local file to store the screenshot
         """
        data = self.simple(url, parameters);
        if len(data['png']) > 0:
            image = open(file, mode='wb')
            image.write(data['png'])
            image.close();
            return {'code': data['code'], 'file': file}

        return {'code': data['code'], 'file': ''}


    def instance_list(self):
        """ Return the list of instances as a dictionary. See https://browshot.com/api/documentation#instance_list for the response format. """
        return self.return_reply('instance/list')


    def instance_info(self, id=0):
        """ Return the details of an instance. See https://browshot.com/api/documentation#instance_info for the response format.

            Arguments:
                id (Required): Instance ID
         """
        return self.return_reply('instance/info', { 'id': id })


    def browser_list(self):
        """ Return the list of browsers as a hash reference. See https://browshot.com/api/documentation#browser_list for the response format. """
        return self.return_reply('browser/list')

    def browser_info(self, id=0):
        """ Return the details of a browser. See https://browshot.com/api/documentation#browser_info for the response format.

            Arguments:
                id (Required: Browser ID
        """
        return self.return_reply('browser/info', { 'id': id })


    def screenshot_create(self, url='', parameters={}):
        """ Request a screenshot. See https://browshot.com/api/documentation#screenshot_create for the response format.

            Note: by default, screenshots are cached for 24 hours. You can tune this valu with the cache=X parameter.

            Arguments:
            See https://browshot.com/api/documentation#screenshot_create for the full list of possible arguments.
                url(Required): URL of the website to create a screenshot of.
        """
        parameters.update({'url': url})
        return self.return_reply('screenshot/create', parameters)

    def screenshot_info(self, id=0, parameters={}):
        """ Get information about a screenshot requested previously. See https://browshot.com/api/documentation#screenshot_info for the response format.

            Arguments:
                id (Required): Screenshot ID.
        """
        parameters.update({'id': id})
        return self.return_reply('screenshot/info', parameters)

    def screenshot_list(self, parameters={}):
        """ Get details about screenshot requested. See https://browshot.com/api/documentation#screenshot_list for the response format. """
        return self.return_reply('screenshot/list', parameters)

    def screenshot_host(self, id=0, parameters={}):
        """ Host a screenshot or a thumbnail. See https://browshot.com/api/documentation#screenshot_host for the response format.

            Arguments:
            See https://browshot.com/api/documentation#screenshot_host for the full list of possible arguments.
                id (Required): screenshot ID
        """
        parameters.update({'id': id})
        return self.return_reply('screenshot/host', parameters)

    def screenshot_share(self, id=0, parameters={}):
        """ Share a screenshot. See L<http://browshot.com/api/documentation#screenshot_share> for the response format.

            Arguments:
            See https://browshot.com/api/documentation#screenshot_share for the full list of possible arguments.
                id (Required): screenshot ID
        """
        parameters.update({'id': id})
        return self.return_reply('screenshot/share', parameters)

    def screenshot_search(self, url='', parameters={}):
        """ Get details about screenshots requested. See L<http://browshot.com/api/documentation#screenshot_search> for the response format.

            Arguments:
            See https://browshot.com/api/documentation#screenshot_search for the full list of possible arguments.
                url (Required): URL string to match
        """
        parameters.update({'url': url})
        return self.return_reply('screenshot/search', parameters)

    def screenshot_delete(self, id=0, parameters={}):
        """ Delete details of a screenshot. See L<http://browshot.com/api/documentation#screenshot_delete> for the response format.

            Arguments:
            See https://browshot.com/api/documentation#screenshot_delete for the full list of possible arguments.
                id (Required): screenshot ID
        """
        parameters.update({'id': id})
        return self.return_reply('screenshot/delete', parameters)

    def screenshot_thumbnail(self, id=0, parameters={}):
        """ Retrieve the screenshot, or a thumbnail. See L<http://browshot.com/api/documentation#screenshot_thumbnail> for the response format.

            Arguments:
            See https://browshot.com/api/documentation#screenshot_thumbnail for the full list of possible arguments.
                id (Required): screenshot ID. You will get the full image if no other argument is specified.
        """
        parameters.update({'id': id})
        url = self.make_url('screenshot/thumbnail', parameters)
        response = urllib.urlopen(url)
        return response.read()

    def screenshot_thumbnail_file(self, id=0, file='', parameters={}):
        """ Retrieve the screenshot, or a thumbnail, and save it to a file. See http://browshot.com/api/documentation#screenshot_thumbnail for the response format.

        Returns the file name if successful.

        Arguments:
        See https://browshot.com/api/documentation#screenshot_thumbnail for the full list of possible arguments.
            id (Required): screenshot ID. You will get the full image if no other argument is specified.
            file (Required): local file to store the screenshot
         """
        content = self.screenshot_thumbnail(id, parameters);

        image = open(file, mode='wb')
        image.write(content)
        image.close();

        return file

    def screenshot_html(self, id=0, parameters={}):
        """ Get the HTML code of the rendered page. See L<http://browshot.com/api/documentation#screenshot_html> for the response format.

            Arguments:
            See https://browshot.com/api/documentation#screenshot_html for the full list of possible arguments.
                id (Required): screenshot ID
        """
        parameters.update({'id': id})
        return self.return_reply_string('screenshot/html', parameters)


    def screenshot_multiple(self, parameters={}):
        """ Request multiple screenshots. See https://browshot.com/api/documentation#screenshot_multiple for the response format.

            Arguments:
            See https://browshot.com/api/documentation#screenshot_multiple for the full list of possible arguments.
        """
        return self.return_reply('screenshot/multiple', parameters)


    def batch_create(self, file='', parameters={}):
        """ Request multiple screenshots from a file. See https://browshot.com/api/documentation#batch_create for the response format.

            Arguments:
            See https://browshot.com/api/documentation#batch_create for the full list of possible arguments.
                file (Required): file with hhe list of URLs to capture
        """
        return self.return_post_reply('batch/create', file, parameters)


    def batch_info(self, id=0, parameters={}):
        """ Check the status of a batch. See https://browshot.com/api/documentation#batch_info for the response format.

            Arguments:
            See https://browshot.com/api/documentation#batch_info for the full list of possible arguments.
                id (Required): batch ID
        """
        parameters.update({'id': id})
        return self.return_reply('batch/info', parameters)


    def crawl_create(self, domain='', url='', parameters={}):
        """ Crawl a domain. See https://browshot.com/api/documentation#crawl_create for the response format.

            Arguments:
            See https://browshot.com/api/documentation#crawl_create for the full list of possible arguments.
                domain (Required): domain to crawl
                url (Required): URL to start with
        """
        parameters.update({'url': url})
        parameters.update({'domain': domain})
        return self.return_reply('crawl/create', parameters)


    def crawl_info(self, id=0, parameters={}):
        """ Request multiple screenshots. See https://browshot.com/api/documentation#crawl_info for the response format.

            Arguments:
            See https://browshot.com/api/documentation#crawl_info for the full list of possible arguments.
                id (Required): crawl ID
        """
        parameters.update({'id': id})
        return self.return_reply('crawl/info', parameters)


    def account_info(self, parameters={}):
        """ Get details about the user account. See https://browshot.com/api/documentation#account_info for the response format. """
        return self.return_reply('account/info', parameters)


    def make_url(self, action='', parameters={}):
        url = self.base + action + '?key=' + urllib.quote_plus(self.key)

        for key, value in parameters.items():
            if key == 'urls':
              for uri in value:
                url += '&url=' + urllib.quote_plus(str(uri))
            elif key == 'instances':
              for instance_id in value:
                url += '&instance_id=' + urllib.quote_plus(str(instance_id))
            else:
              url += '&' + urllib.quote_plus(key) + '=' + urllib.quote_plus(str(value))

        if self.debug:
            print url

        return url


    def return_reply(self, action='', parameters={}):
        content = self.return_reply_string(action, parameters);

        try:
            json_decode = simplejson.loads(content)
            return json_decode
        except Exception, e:
            raise e


    def return_reply_string(self, action='', parameters={}):
        try:
            url    = self.make_url(action, parameters)

            response = urllib.urlopen(url)
            return response.read()
        except Exception, e:
            raise e



    def return_post_reply(self, action='', file='', parameters={}):
        content = self.return_reply_post_string(action, file, parameters);

        try:
            json_decode = simplejson.loads(content)
            return json_decode
        except Exception, e:
            raise e


    def return_reply_post_string(self, action='', file='', parameters={}):
        try:
            url = self.make_url(action, parameters)

            if file == '':
              response = urllib.urlopen(url)
              return response.read()

            else:
              response = requests.post(url, files={'file': open(file,'rb')})
              return response.content

        except Exception, e:
            raise e


if __name__ == "__main__":
    client = BrowshotClient()