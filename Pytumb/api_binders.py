#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.
# Based tweepy. Thanks Joshua Roesslein.

from Pytumb.error import PytumbError
from Pytumb.paser import ModelPaser
try:
    import httplib2
except ImportError:
    raise PytumbError('Require httplib2.')
import httplib
import time
import urllib
try:
    import urlparse
except ImportError:
    raise PytumbError('Under Python2.6 is not supported!')
import urllib

class Bider4xml(object):

    def __init__(self,**config):
        self.api = config.get('api', None)
        self.json = config.get('json', False)
        self.host = self.fix_host(config['host'])
        self.path = config['path']
        self.method = config.get('method', 'GET')
        self.status_type = config.get('status_type', None)
        self.require_auth = config.get('require_auth', False)
        self.ptype = config.get('ptype', None)
        self.file_path = config.get('file_path', None)
        self.max_size = config.get('max_size', None)
        self.not_implemented = config.get('not_implemented', False)
        if self.api.secure:
            self.scheme = 'https://'
        else:
            self.scheme = 'http://'

        self.build_parameters(config.get('kargs', None))

    def build_parameters(self, kargs):
        self.parameters = {}
        if kargs is not None:
            for k, arg in kargs.items():
                if arg == None:
                    continue
                if k in self.parameters:
                    raise PytumbError('Multiple values for parameter %s supplied!' % k)

                if k == 'reblog_key':
                    self.parameters['reblog-key'] = convert_to_utf8_str(arg)
                elif k == 'post_id':
                    self.parameters['post-id'] = convert_to_utf8_str(arg)
                elif k == 'send_to_twitter':
                    self.parameters['send-to-twitter'] = convert_to_utf8_str(arg)
                elif k == 'click_through_url':
                    self.parameters['click-through-url'] = convert_to_utf8_str(arg)
                elif k == 'externally_hosted_url':
                    self.parameters['externally-hosted-url'] = convert_to_utf8_str(arg)
                else:
                    self.parameters[k] = convert_to_utf8_str(arg)

        if self.ptype:
            self.parameters['type'] = self.ptype

    def fix_host(self, host):
        # redirect check
        # FIXME: Waste processing
        try:
            conn = httplib.HTTPConnection(host)
            conn.request('GET', '/')
            r = conn.getresponse()
            conn.close()
            if r.status == 200:
                return host
            elif r.status == 301:
                fix_host = urlparse.urlparse(r.msg['Location']).netloc
                conn2 = httplib.HTTPConnection(fix_host)
                conn2.request('GET', '/')
                r2 = conn2.getresponse()
                conn2.close()
                if r2.status == 200:
                    return fix_host
            else:
                raise  PytumbError('Unknown Host: %s' % self.host)

        except httplib.HTTPException, e:
            raise PytumbError(e)


    def execute(self):
        if self.json:
            url = self.scheme + self.host + self.path + '/json'
        else:
            url = self.scheme + self.host + self.path

        if self.method == 'GET' and len(self.parameters):
            url = url + '?%s' % (urllib.urlencode(self.parameters))

        retries_performed = 0
        while retries_performed < self.api.retry_count + 1:

            #try:
            if self.api.auth and self.require_auth:
                resp, content = self.api.auth.apply_oauth_request(url, method=self.method,
                                             params=self.parameters, file_path=self.file_path,
                                             max_size=self.max_size)
            else:
                client = httplib2.Http()
                resp, content = client.request(url, self.method)
            #except Exception, e:
            #    raise PytumbError('Failed to send request: %s' % e)

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
        if resp.status != 200:
            if resp.status != 201:
                try:
                    error_msg = parser.parse_error(self, content)
                except Exception:
                    print content
                    error_msg = 'Tumblr error response: status code = %s ' % resp.status
                raise PytumbError(error_msg, resp)

        result = parser.chooseParser(self, content)

        return result

        



def convert_to_utf8_str(arg):
    # written by Michael Norton (http://docondev.blogspot.com/)
    if isinstance(arg, unicode):
        arg = arg.encode('utf-8')
    elif not isinstance(arg, str):
        arg = str(arg)
    return arg