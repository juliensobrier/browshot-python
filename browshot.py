# Copyright 2011 Julien Sobrier
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

""" Version 1.2.1

Python module for Browshot (http://www.browshot.com/), a web service to create website screenshots.

Browshot (http://www.browshot.com/) is a web service to easily make screenshots of web pages in any screen size, as any device: iPhone, iPad, Android, Nook, PC, etc. Browshot has full Flash, JavaScript, CSS, & HTML5 support.

The latest API version is detailed at http://browshot.com/api/documentation. browshot.py follows the API documentation very closely: the function names are similar to the URLs used (screenshot/create becomes screenshot_create(), instance/list becomes instance_list(), etc.), the request arguments are exactly the same, etc.

The library version matches closely the API version it handles: browshot.py 1.0.0 is the first release for the API 1.0, browshot.py 1.1.1 is the second release for the API 1.1, etc.

browshot.py can handle most the API updates within the same major version, e.g. browshot.py 1.0.0 should be compatible with the API 1.1 or 1.2. """


import urllib
import urllib2
import simplejson


class BrowshotClient(object):
	def __init__(self, key='', base='https://api.browshot.com/api/v1/', debug=0):
		""" Create a new WebService::Browshot object. You must pass your API key (go to you Dashboard to find your API key, https://browshot.com/dashboard).
		
		Arguments:
			key:  API key.
			base: Base URL for all API requests. You should use the default base provided by the library. Be careful if you decide to use HTTP instead of HTTPS as your API key could be sniffed and your account could be used without your consent.
			debug: Set to 1 to print debug output to the standard output. 0 (disabled) by default.
		"""
		self.key = key
		self.base = base
		self.debug = debug
		
	def api_version(self):
		""" Return the API version handled by the library. Note that this library can usually handle new arguments in requests without requiring an update. """
		return '1.2'

	def instance_list(self):
		""" Return the list of instances as a dictionary. See http://browshot.com/api/documentation#instance_list for the response format. """
		return self.return_reply('instance/list')

	
	def instance_info(self, id=0):
		""" Return the details of an instance. See http://browshot.com/api/documentation#instance_info for the response format.

			Arguments:
				id (Required): Instance ID
 		"""
		return self.return_reply('instance/info', { 'id': id })
	
	def instance_create(self,parameters={}):
		""" Create a private instance. See http://browshot.com/api/documentation#instance_create for the response format.

			Arguments:
				See http://browshot.com/api/documentation#instance_create for the full list of possible arguments.
 		"""
		return self.return_reply('instance/create', parameters)


	def browser_list(self):
		""" Return the list of browsers as a hash reference. See http://browshot.com/api/documentation#browser_list for the response format. """
		return self.return_reply('browser/list')
	
	def browser_info(self, id=0):
		""" Return the details of a browser. See L<http://browshot.com/api/documentation#browser_info> for the response format.

			Arguments:
				id (Required: Browser ID
		"""
		return self.return_reply('browser/info', { 'id': id })
	
	def browser_create(self,parameters={}):
		""" Create a custom browser. See http://browshot.com/api/documentation#browser_create for the response format.

			Arguments:
				See http://browshot.com/api/documentation#browser_create for the full list of possible arguments.
 		"""
		return self.return_reply('browser/create', parameters)

	def screenshot_create(self, url='', parameters={}):
		""" Request a screenshot. See http://browshot.com/api/documentation#screenshot_create for the response format.

			Arguments:
			See http://browshot.com/api/documentation#screenshot_create for the full list of possible arguments.
				url(Required): URL of the website to create a screenshot of.
		"""
		parameters.update({'url': url})
		return self.return_reply('screenshot/create', parameters)

	def screenshot_info(self, id=0):
		""" Get information about a screenshot requested previously. See http://browshot.com/api/documentation#screenshot_info for the response format.

			Arguments:
				id (Required): Screenshot ID.
		"""
		return self.return_reply('screenshot/info', { 'id': id })

	def screenshot_list(self, parameters={}):
		""" Get details about screenshot requested. See http://browshot.com/api/documentation#screenshot_list for the response format. """
		return self.return_reply('screenshot/list', parameters)

	def screenshot_thumbnail(self, url='', parameters={}):
		""" Retrieve the screenshot, or a thumbnail. See L<http://browshot.com/api/documentation#thumbnails> for the response format.
		
			Arguments:
			See http://browshot.com/api/documentation#thumbnails for the full list of possible arguments.
				url (Required): URL of the screenshot (screenshot_url value retrieved from screenshot_create() or screenshot_info()). You will get the full image if no other argument is specified.
		"""
		try:
			for key, value in parameters.items():
				url += '&' + urllib.quote_plus(key) + '=' + urllib.quote_plus(str(value))
			
			response = urllib.urlopen(url)
			
			return response.read()
		except Exception, e:
			raise e
		
	def screenshot_thumbnail_file(self, url='', file='', parameters={}):
		""" Retrieve the screenshot, or a thumbnail, and save it to a file. See http://browshot.com/api/documentation#thumbnails for the response format.

		Returns the file name if successful.

		Arguments:
		See http://browshot.com/api/documentation#thumbnails for the full list of possible arguments.
			url (Required): URL of the screenshot (screenshot_url value retrieved from screenshot_create() or screenshot_info()). You will get the full image if no other argument is specified.
 		"""
		content = self.screenshot_thumbnail(url, parameters);

		image = open(file, mode='wb')
		image.write(content)
		image.close();
		
		return file

	def account_info(self, parameters={}):
		""" Get details about the user account. See http://browshot.com/api/documentation#account_info for the response format. """
		return self.return_reply('account/info', parameters)

	
	def make_url(self, action='', parameters={}):
		url = self.base + action + '?key=' + urllib.quote_plus(self.key)
		
		for key, value in parameters.items():
			url += '&' + urllib.quote_plus(key) + '=' + urllib.quote_plus(str(value))

		if self.debug:
			print url

		return url
		
	def return_reply(self, action='', parameters={}):
		try:
			url	= self.make_url(action, parameters)
			
			response = urllib.urlopen(url)
			json = response.read()
			
			json_decode = simplejson.loads(json)
			return json_decode
		except Exception, e:
			raise e