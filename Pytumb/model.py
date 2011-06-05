#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.
# Based tweepy. Thanks Joshua Roesslein.

from Pytumb.error import PytumbError


class Model(object):

    def __init__(self, api=None):
        self._api = api

        def __getstate__(self):
            pickle = dict(self.__dict__)
            try:
                del pickle['_api']
            except KeyError:
                pass
            return pickle

        @classmethod
        def parse(cls, api, json):
            raise NotImplementedError


class template(Model):
    @classmethod
    def parse(cls, method, json):
        api = method.api
        status = cls(api)

class Posts(Model):
    @classmethod
    def parse(cls, method, json):
        api = method.api
        post = cls(api)
        for k, v in json.items():
            setattr(post, k, v)
        return post

    @classmethod
    def parse_lists(cls, method, json_lists):
        api = method.api
        results = []
        for json in json_lists:
            results.append(cls.parse(method, json))
        return results

class Tumblelog(Model):
    @classmethod
    def parse(cls, method, json):
        api = method.api
        tumblelog = cls(api)
        for k, v in json.items():
            setattr(tumblelog, k, v)
        return tumblelog

class Update(Model):
    @classmethod
    def parse(cls, method, elem):
        api = method.api
        status = cls(api)
        print elem

class Pages(Model):
    @classmethod
    def parse(cls, method, elem):
        api = method.api
        status = cls(api)
        pages = []
        for n in elem.findall('pages'):
            for m in n:
                page = dict()
                for k, v in m.items():
                    page[k] = v
                pages.append(page)
        setattr(status, 'pages', pages)
        return status


class User(Model):
    @classmethod
    def parse(cls, method, json):
        api = method.api
        status = cls(api)
        for k, v in json.items():
            if k == 'posts':
                posts = Posts.parse_lists(method, v)
                setattr(status, 'posts', posts)
            elif k == 'tumblelog':
                tumblelog = Tumblelog.parse(method, v)
                setattr(status, 'tumblelog', tumblelog)
            else:
                setattr(status, k, v)
        return status
                

class Dashboard(Model):
    # Parse JSON
    @classmethod
    def parse(cls, method, json):
        api = method.api
        status = cls(api)
        for k, v in json.items():
            if k == 'posts':
                posts = Posts.parse_lists(method, v)
                setattr(status, 'posts', posts)
            else:
                setattr(status, k, v)
        return status

class MyLikes(Model):
    # Parse XML
    @classmethod
    def parse(cls, method, elem):
        api = method.api
        status = cls(api)
        if method.json:
            raise PytumbError('%s Model is not Implemented JsonPaser' % method.status_type)
        posts = []
        for n in elem.findall('posts'):
            for m in n:
                post = dict()
                for k, v in m.items():
                    post[k] = v
                posts.append(post)
        setattr(status, 'posts', posts)
        return status

class AccountInfo(Model):
    # Parse XML
    @classmethod
    def parse(cls, method, elem):
        api = method.api
        status = cls(api)
        if method.json:
            raise PytumbError('%s Model is not Implemented JsonPaser' % method.status_type)
        userlimits = []
        tumblelog = []

        for n in elem.findall('user'):
            obj = dict()
            obj['default-post-format'] = n.get('default-post-format')
            obj['can-upload-aiff'] = n.get('can-upload-aiff')
            obj['can-upload-video'] = n.get('can-upload-video')
            obj['can-upload-audio'] = n.get('can-upload-audio')
            obj['max-video-bytes-uploaded'] = n.get('max-video-bytes-uploaded')
            userlimits.append(obj)
        for n in elem.findall('tumblelog'):
            obj = dict()
            obj['title'] = n.get('title')
            obj['type'] = n.get('type')
            obj['private-id'] = n.get('private-id')
            obj['name'] = n.get('name')
            obj['url'] = n.get('url')
            obj['avatar-url'] = n.get('avatar-url')
            obj['is-primary'] = n.get('is-primary')
            tumblelog.append(obj)
        setattr(status, 'userlimits', userlimits)
        setattr(status, 'tumblelog', tumblelog)
        return status


class ModelFactory(object):
    dashboard = Dashboard
    accountinfo = AccountInfo
    user = User
    my_likes = MyLikes
    update = Update
    pages = Pages