#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.
# Based tweepy. Thanks Joshua Roesslein.

from Pytumb.error import PytumbError
from Pytumb.paser import ModelPaser
from Pytumb.utils import Utils

import time
import urllib

try:
    import httplib2
except ImportError:
    raise PytumbError('Require httplib2.')

try:
    import urlparse
except ImportError:
    raise PytumbError('Under Python2.6 is not supported!')

convert_to_utf8_str = Utils.convert_to_utf8_str

class Binder(object):

    def __init__(self, **config):
        self.api = config.get('api', None)
        self.api_method_path = config.get('api_method_path', None)
        self.blog_hostname = config.get('blog_hostname', None)
        self.api_path = config.get('api_path', None)
        self.payload = config.get('payload', {})
        self.status_type = config.get('status_type', 'raw')
        self.auth_type = config.get('auth_type', None)
        self.method = config.get('method', 'GET')
        self.file_path = config.get('file_path', None)
        self.max_size = config.get('max_size', None)

    def execute(self):
        if self.auth_type == 'api_key':
            self.payload['api_key'] = self.api.auth._consumer.key

        if self.api_method_path == '/blog':
            url = 'http://' + self.api.api_domain + '/' +self.api.api_version + self.api_method_path  + '/' + self.blog_hostname + self.api_path
        elif self.api_method_path == '/user':
            url = 'http://' + self.api.api_domain + '/' +self.api.api_version + self.api_method_path +  self.api_path

        retries_performed = 0
        while retries_performed < self.api.retry_count + 1:

            try:
                if self.auth_type == 'oauth':
                    resp, content = self.api.auth.apply_oauth_request(url, method=self.method,
                                                 params=self.payload)
                else:
                    if self.method == 'GET' and len(self.payload):
                        url = url + '?' + urllib.urlencode(self.payload)
                    client = httplib2.Http()
                    resp, content = client.request(url, self.method)
            except Exception, e:
                raise PytumbError('Failed to send request: %s' % e)

            if self.api.retry_errors:
                if resp.status not in self.api.retry_errors:
                    break
                else:
                    if resp.status == 200:
                        break
            time.sleep(self.api.retry_delay)
            retries_performed += 1

        parser = ModelPaser()
        self.api.last_response = resp, content
        ####################################################
        print self.api.last_response
        print url
        ####################################################
        if resp.status != 200:
            if resp.status != 201:
                error_msg = parser.parse_error(self, content)
                raise PytumbError(error_msg, resp)
                """
                try:
                    error_msg = parser.parse_error(self, content)
                except Exception:
                    error_msg = 'Tumblr error response: status code = %s ' % resp.status
                raise PytumbError(error_msg, resp)
                """

        result = parser.parser(self, content)

        return result
