#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.
# Based tweepy. Thanks Joshua Roesslein.

"""
Pytumb Tumblr API Library

Version:
ex) Version 1.2.3
1: Major version
2: Minor version
3: Revision(bug fix and more...)

History(Learn more https://github.com/PyYoshi/Pytumb/commits/master/ ):
0.1.0 Pre-Alpha(2011.05.17): Release library. Add oauth functions.
0.2.0 Pre-Alpha(2011.06.05): Support Tumblr APIs(Not done yet.)
0.2.1 Pre-Alpha(2011.06.06): Add Exception handling and bug fix.
0.3.0 Change API v2.
0.4.0


TODO:
    api.py: v2ではlike,unlikeが実装されていないのでv1を使用する。またconsumer登録しなくても取れるv1の/api/readをclass OldAPIに実装
            edit_postの実装。
    すべてのモジュールをPython2.5+への配慮
    無駄な処理を見つけ最適化
    parser.pyからmodel.pyへ変更後: 各API用のエラー処理追加
    xAuthの対応


Support APIs:
Learn api.py
"""

__vesion__ = '0.4.0'
__author__ = 'Yoshihiro Misawa'
__license__ = 'MIT License'
__url__ = 'https://github.com/PyYoshi/Pytumb'

from Pytumb.auth import OAuthHandler
from Pytumb.error import PytumbError
from Pytumb.api import API

