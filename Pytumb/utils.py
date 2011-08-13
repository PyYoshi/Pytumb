#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.

from Pytumb.error import PytumbError
import os

class Utils(object):

    @classmethod
    def convert_to_utf8_str(self, arg):
        # written by Michael Norton (http://docondev.blogspot.com/)
        if isinstance(arg, unicode):
            arg = arg.encode('utf-8')
        elif not isinstance(arg, str):
            arg = str(arg)
        return arg

    @classmethod
    def import_simplejson(self):
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

    @classmethod
    def chkFile(cls, file_path, max_size):
        try:
            if os.path.getsize(file_path) > (max_size * 1024):
                raise PytumbError('File is too big, must be less than %d' % (max_size * 1024) )
        except os.errno, e:
            raise PytumbError('Unable to access file, %s' % e)
        fp = open(file_path, 'rb')
        data = fp.read()
        fp.close()
        return data