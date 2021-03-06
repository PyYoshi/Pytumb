#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.
# Based tweepy. Thanks Joshua Roesslein.

from Pytumb.error import PytumbError
from urllib import urlencode, quote
from Pytumb.api import API
try:
    from urlparse import parse_qs
except ImportError:
    def parse_qs(url):
        param = {}
        for i in url.split('&'):
            _p = i.split('=')
            param.update({_p[0]: _p[1]})
        return param
try:
    import httplib2
except ImportError:
    PytumbError('Install httplib2. ex.) easy_install httplib2')
from Pytumb import oauth2

class OAuthHandler():
    """OAuth authentication handler"""
    # Request-token URL: POST http://www.tumblr.com/oauth/request_token
    # Authorize URL: http://www.tumblr.com/oauth/authorize
    # Access-token URL: POST http://www.tumblr.com/oauth/access_token
    
    OAUTH_HOST = 'www.tumblr.com'
    OAUTH_ROOT = '/oauth/'

    def __init__(self, consumer_key, consumer_secret, callback=None, secure=False):

        self._consumer = oauth2.Consumer(consumer_key, consumer_secret)
        self.request_token = None
        self.access_token = None
        self.callback = callback
        self.username = None
        self.secure = secure

    #
    def _gen_oauth_url(self, endpoint):
        if self.secure:
            # https has not been implemented on Tumblr.
            prefix = 'https://'
        else:
            prefix = 'http://'
        return prefix + self.OAUTH_HOST + self.OAUTH_ROOT + endpoint

    #
    def _get_request_token(self):
        try:
            url = self._gen_oauth_url('request_token')
            # Note: Only POST.
            client = oauth2.Client(self._consumer)
            resp, content = client.request(url, 'POST')
            tmp_token = parse_qs(content)
            key = tmp_token['oauth_token']
            secret = tmp_token['oauth_token_secret']
            return oauth2.Token(key[0], secret[0])

        except Exception, e:
            raise PytumbError(e)

    #
    def set_request_token(self, key, secret):
        self.request_token = oauth2.Token(key, secret)

    #
    def get_authorization_url(self):
        try:
            self.request_token = self._get_request_token()
            url = self._gen_oauth_url('authorize') + '?oauth_token=' + self.request_token.key
            return url
        except Exception, e:
            raise PytumbError(e)

    #
    def get_access_token(self, verifier=None):
        try:
            url = self._gen_oauth_url('access_token')
            client = oauth2.Client(self._consumer, self.request_token)
            resp, content = client.request(url, 'POST', body='oauth_verifier=%s' % str(verifier))

            tmp_token = parse_qs(content)
            key = tmp_token['oauth_token']
            secret = tmp_token['oauth_token_secret']
            self.access_token = oauth2.Token(key[0], secret[0])
        except Exception, e:
            raise PytumbError(e)

    #
    def set_access_token(self, key, secret):
        self.access_token = oauth2.Token(key, secret)

    #
    def apply_oauth_request(self, url, method, params=None):

        try:
            client = oauth2.Client(consumer=self._consumer, token=self.access_token)
            params = urlencode(params)
            resp, content = client.request(url, method, params)
            return resp, content
        except Exception, e:
            raise PytumbError('Failed to aplly OAuth. Error message: %s' % e)

        # multipart/form-data
        """
        if file_path:
            client = oauth2.Client(consumer=self._consumer, token=self.access_token)
            content_type, data = API._encode_multipart_formdata(params, file_path, max_size)
            headers={'Content-Type':content_type}
            resp, content = client.request(url, method, headers=headers, body=data)
            return resp, content
        else:
            client = oauth2.Client(consumer=self._consumer, token=self.access_token)
            params = urlencode(params)
            resp, content = client.request(uri=url, method=method, body=params, headers=headers)
            return resp, content"""
