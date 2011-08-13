#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.
# Based tweepy. Thanks Joshua Roesslein.

from Pytumb.error import PytumbError
import datetime

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

class Raw(Model):
    @classmethod
    def parse(cls, method, data):
        api = method.api
        raw = cls(api)
        try:
            for k, v in data.items():
                setattr(raw, k, v)
        except AttributeError:
            setattr(raw, 'data', data)
        return raw

class BlogInfo(Model):
    @classmethod
    def parse(cls, method, data):
        api = method.api
        info =cls(api)
        blog = data.get('blog', data)
        for k, v in blog.items():
            setattr(info, k, v)
        return info

    @classmethod
    def parse_lists(cls,method,data_lists):
        results = []
        for data in data_lists:
            results.append(cls.parse(method, data))
        return results

class Binary(Model):
    @classmethod
    def parse(cls, method, data):
        api = method.api
        binary = cls(api)
        resp = api.last_response[0]
        setattr(binary,'content-type', resp['content-type'])
        setattr(binary, 'content-location', resp['content-location'])
        setattr(binary, 'content', data)
        return binary

class User(Model):
    @classmethod
    def parse(cls, method, data):
        api = method.api
        user = cls(api)
        for k, v in data.items():
            if k == 'blogs':
                v = BlogInfo.parse_lists(method, v)
            setattr(user, k, v)
        return user

    @classmethod
    def parse_lists(cls, method, data_list):
        results = []
        for data in data_list:
            results.append(cls.parse(method, data))
        return results
    

class BlogFollowers(Model):
    @classmethod
    def parse(cls, method, data):
        api = method.api
        followers = cls(api)
        for k, v in data.items():
            if k == 'total_users':
                v = int(v)
            if k == 'users':
                v = User.parse_lists(method, v)
            setattr(followers, k, v)
        return followers

class Post(Model):
    @classmethod
    def parse(cls, method, data):
        api = method.api
        post = cls(api)
        for k, v in data.items():
            #if data['type'] == 'photo':
            #    pass
            setattr(post, k, v)
        #print post.__dict__
        return post

    @classmethod
    def parse_lists(cls, method, data_lists):
        results = []
        for data in data_lists:
            results.append(cls.parse(method, data))
        return results

class Photo(Model):
    @classmethod
    def parse(cls, method, data):
        api = method.api
        photo = cls(api)
        for k, v in data.items():
            setattr(photo, k, v)
        return photo

    @classmethod
    def parse_lists(cls, method, data_lists):
        results = []
        for data in data_lists:
            results.append(cls.parse(method, data))
        return results

class BlogPosts(Model):
    @classmethod
    def parse(cls, method, data):
        api = method.api
        posts = cls(api)
        for k, v in data.items():
            if k == 'blogs':
                v = BlogInfo.parse(method, v)
            if k == 'posts':
                v = Post.parse_lists(method, v)
            if k == 'total_posts':
                v = int(v)
            setattr(posts, k, v)
        return posts

class Update(Model):
    @classmethod
    def parse(cls, method, data):
        api = method.api
        raw = cls(api)
        for k, v in data.items():
            setattr(raw, k, v)
        return raw

class UserInfo(Model):
    @classmethod
    def parse(cls,method, data):
        api = method.api
        userinfo = cls(api)
        for k, v in data['user'].items():
            if k == 'blogs':
                v = BlogInfo.parse_lists(method, v)
            setattr(userinfo, k, v)
        return userinfo

class Dashboard(Model):
    @classmethod
    def parse(cls,method, data):
        api = method.api
        dashboard = cls(api)
        for k, v in data.items():
            if k == 'posts':
                v = Post.parse_lists(method, v)
            setattr(dashboard,k,v)
        return dashboard

class UserLikes(Model):
    @classmethod
    def parse(cls,method,data):
        api = method.api
        likes = cls(api)
        for k, v in data.items():
            if k == 'liked_posts':
                v = Post.parse_lists(method,v)
            setattr(likes,k,v)
        return likes

class UserFollowing(Model):
    @classmethod
    def parse(cls,method,data):
        api = method.api
        userfollowing = cls(api)
        for k,v in data.items():
            if k == 'blogs':
                v = BlogInfo.parse_lists(method,v)
            setattr(userfollowing,k,v)
        return userfollowing

class FollowUnfollow(Model):
    @classmethod
    def parse(cls,method,data):
        api = method.api
        follow = cls(api)
        resp = api.last_response[0]
        if resp['status'] == '200':
            setattr(follow, 'msg', 'OK')
        else:
            setattr(follow, 'msg', 'FAILED')
        return follow

class ModelFactory(object):
    raw = Raw
    bloginfo = BlogInfo
    binary = Binary
    blogfollowers = BlogFollowers
    blogposts = BlogPosts
    userinfo = UserInfo
    dashboard = Dashboard
    userlikes = UserLikes
    userfollowing = UserFollowing
    followunfollow = FollowUnfollow