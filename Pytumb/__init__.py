#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.
# Based tweepy. Thanks Joshua Roesslein.

"""
Pytumb Tumblr API Library

Version:
ex) Version 1.2.3 Beta
1: Major version
2: Minor version
3: Revision(bug fix and more...)

History(Learn more https://github.com/PyYoshi/Pytumb/commits/master/ ):
0.1.0 Pre-Alpha(2011.05.17): Release library. Add oauth functions.
0.2.0 Pre-Alpha(2011.06.05): Support Tumblr APIs(Not done yet.)
0.2.1 Pre-Alpha(2011.06.06): Add Exception handling and bug fix.

TODO:
    auth.py: 画像・動画などのファイルのmultipart/form-dataサポート
    model.py: XML・Json以外のレスポンスへの配慮。 エラーパーサーの値を精確に。
    すべてのモジュールをPython2.5+への配慮
    

Support APIs:
Learn api.py
"""

__vesion__ = '0.2.1 Pre-Alpha'
__author__ = 'Yoshihiro Misawa'
__license__ = 'MIT License'

from Pytumb.auth import OAuthHandler
from Pytumb.error import PytumbError
from Pytumb.api import API
from Pytumb.model import Dashboard

# Global, unauthenticated instance of API
api = API()
