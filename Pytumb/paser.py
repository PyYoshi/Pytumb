#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.
# Based tweepy. Thanks Joshua Roesslein.

from Pytumb.error import PytumbError
from Pytumb.model import ModelFactory

import re

try:
    from xml.etree import cElementTree as etree
except ImportError:
    raise PytumbError('Under Python2.6 is not supported!')

class ModelPaser(object):
    def __init__(self):
        self.model_factory = ModelFactory

    def parse_error(self, method, resp):
        if method.path == '/api/dashboard':
            if resp.status == 503:
                return 'You have exceeded the rate limit or the service is under heavy load. Return message: %s' % resp.read()
            else:
                return "Sorry, this error is unknown. Check Tumblr's API DOC. Return message: %s" % resp.read()
        elif method.path == '/api/like' or '/api/unlike':
            if resp.status == 400:
                return 'Invalid input data. Return message: %s' % resp.read()
            elif resp.status == 403:
                return 'Authentication or permissions failures. Return message: %s' % resp.read()
            elif resp.status == 404:
                return 'Not found post or an incorrect reblog-key value. Return message: %s' % resp.read()
            else:
                return "Sorry, this error is unknown. Check Tumblr's API DOC. Return message: %s" % resp.read()
        elif method.path == '/api/write':
            if resp.status == 400:
                return 'There was at least one error while trying to save your post. Errors are sent in plain text, one per line. Return message: %s' % resp.read()
            
            elif resp.status == 403:
                return 'Authentication failure. Return message: %s' % resp.read()
            else:
                return "Sorry, this error is unknown. Check Tumblr's API DOC. Return message: %s" % resp.read()
        else:
            return "Sorry, this error is unknown. Check Tumblr's API DOC. Return message: %s" % resp.read()

    def chooseParser(self, method, data):
        self.method = method
        self.data = data

        if self.method.json:
            return self.jsonPaser()
        else:
            return self.xmlParser()

    def jsonPaser(self):
        json_lib = import_simplejson()
        r = re.compile('var tumblr_api_read =')
        try:
            json = json_lib.loads(re.sub(r, '', self.data)[:-2])
        except Exception, e:
            raise PytumbError('Failed to parse JSON: %s' % e)
        try:
            if self.method.status_type is None:
                return
            model = getattr(self.model_factory, self.method.status_type)
        except AttributeError:
            raise PytumbError('No model for this type: %s' % self.method.status_type)

        result = model.parse(self.method, json)
        return result

    def xmlParser(self):
        try:
            elem = etree.fromstring(self.data)
            try:
                if self.method.status_type is None:
                    return
                model = getattr(self.model_factory, self.method.status_type)
            except AttributeError:
                raise PytumbError('No model for this type: %s' % self.method.status_type)

            result = model.parse(self.method, elem)
            return result
        except etree.ParseError, e:
            #print 'Parse Error: %s' % e
            return self.data



def import_simplejson():
    try:
        import simplejson as json
    except ImportError:
        try:
            import json  # Python 2.6+
        except ImportError:
            try:
                from django.utils import simplejson as json  # Google App Engine
            except ImportError:
                raise ImportError, "Can't load a json library"

    return json


