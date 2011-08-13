#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.
# Based tweepy. Thanks Joshua Roesslein.

from Pytumb.error import PytumbError
from Pytumb.model import ModelFactory
from Pytumb.utils import Utils

json_lib = Utils.import_simplejson()

class ModelPaser(object):
    def __init__(self):
        self.model_factory = ModelFactory

    def parse_error(self, method, resp):
        json = json_lib.loads(resp)
        status = json['meta']['status']
        msg = json['meta']['msg']
        print status, msg
        print method.__dict__

        if method.api_path == '/info':
            if status == 404:
                return 'Invalid blog hostname: %s ' % method.blog_hostname
            elif status == 401:
                return  'Invalid consumer key.'
            else:
                return "Sorry, this error is unknown. Check Tumblr's API DOC. Return message: %s" % msg
        else:
            return "Sorry, this error is unknown. Check Tumblr's API DOC. Return message: %s" % msg


    def parser(self, method, data):
        if method.status_type == 'binary':
            try:
                model = getattr(self.model_factory, method.status_type)
            except AttributeError:
                raise PytumbError('No model for this type: %s' % method.status_type)

            result = model.parse(method, data)
            return result

        else:
            try:
               data = json_lib.loads(data)['response']
            except Exception, e:
                raise PytumbError('Failed to parse JSON: %s' % e)
            try:
                if method.status_type is None:
                    return
                model = getattr(self.model_factory, method.status_type)
            except AttributeError:
                raise PytumbError('No model for this type: %s' % method.status_type)

            result = model.parse(method, data)
            return result







