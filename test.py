#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.

from Pytumb.auth import OAuthHandler
from Pytumb.error import PytumbError
from Pytumb.api import API
from urlparse import parse_qs
from wsgiref.simple_server import make_server
import threading
import webbrowser
import sys

try:
    import keys
    CONSUMER_KEY = keys.CONSUMER_KEY
    CONSUMER_SECRET = keys.CONSUMER_SECRET
    ACCESS_TOKEN = keys.ACCESS_TOKEN
    ACCESS_SECRET_TOKEN = keys.ACCESS_SECRET_TOKEN
except ImportError:
    CONSUMER_KEY = None
    CONSUMER_SECRET = None
    ACCESS_TOKEN = None
    ACCESS_SECRET_TOKEN = None

# Callback URL: http://127.0.0.1:8956/login/

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

def test_get_atoken(env, res):
    if env['PATH_INFO']=='/login/':
        if env['REQUEST_METHOD']=='GET':
            QUERY_STRING = env['QUERY_STRING']
            if QUERY_STRING:
                QUERY_STRING = parse_qs(QUERY_STRING)
                oauth_token = QUERY_STRING['oauth_token'][0]
                oauth_verifier = QUERY_STRING['oauth_verifier'][0]

                threading.Thread(target=httpd.shutdown).start()
                auth.set_request_token(auth.request_token.key, auth.request_token.secret)
                try:
                    auth.get_access_token(oauth_verifier)

                    print 'access_token.key:', auth.access_token.key
                    print 'access_token.secret:', auth.access_token.secret

                    print 'Authenticated Successfully!'
                    res('200 OK',[('Content-type','text/html')])
                    html = """
                    <html>
                    <head>
                    <title>Authenticated Successfully!</title>
                    </head>
                    <body>
                    Authenticated Successfully!
                    </body>
                    </html>
                    """
                    return html
                except PytumbError, e:
                    print 'Error! Failed to get access token. Error message: %s' % e
                    res('401 Unauthorized',[('Content-type','text/html')])
                    html = """
                    <html>
                    <head>
                    <title>Unauthorized!</title>
                    </head>
                    <body>
                    Unauthorized!
                    </body>
                    </html>
                    """
                    return html

if ACCESS_TOKEN and ACCESS_SECRET_TOKEN:
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
    api = API(auth_handler=auth)
    try:
        post_id = 4208659758
        delete_post_id = 8876011609
        reblog_key = 'UpE5higT'
        title = 'test'
        body = """
        I'm tumblr bot. Hello everyone!!
        """
        photo_link = 'http://assets.tumblr.com/images/logo.png'
        link = 'http://www.tumblr.com/'
        blog_hostname = 'axi1.tumblr.com'
        blog_hostname2 = 'renapsfhy.tumblr.com'
        blog_hostname3 = 'renaphy.tumblr.com'
        follow_blog_url = 'http://staff.tumblr.com/'
        file_path = 'test_img.jpg'

        ##print api.get_bloginfo(blog_hostname).__dict__
        ##print api.get_blogavatar(blog_hostname).__dict__
        ##print api.get_blogfollowers(blog_hostname3).__dict__
        ##print api.get_blogposts(blog_hostname3).__dict__
        ##print api.get_blogposts(blog_hostname3, posts_type='photo').__dict__
        ##print api.get_queuedposts(blog_hostname3).__dict__
        ##print api.get_draftposts(blog_hostname3).__dict__
        ##print api.get_submissionposts(blog_hostname3).__dict__
        ##print api.update_text(blog_hostname3,body,title).__dict__
        ##print api.update_photo(blog_hostname3, source=photo_link, link=link, caption=body).__dict__
        ##print api.update_photo(blog_hostname3, file_path=file_path, link=link, caption=body).__dict__
        ##print api.update_quote(blog_hostname3).__dict__
        ##print api.update_link(blog_hostname3).__dict__
        ##print api.update_chat(blog_hostname3).__dict__
        ##print api.update_audio(blog_hostname3).__dict__
        ##print api.update_video(blog_hostname3).__dict__
        #print api.edit_post(blog_hostname3).__dict__
        ##print api.update_reblog(blog_hostname3,reblog_key=reblog_key,post_id=post_id).__dict__
        ##print api.delete_post(blog_hostname3,post_id=delete_post_id).__dict__

        ##print api.get_userinfo().__dict__
        ##print api.get_dashboard().__dict__
        ##print api.get_userlikes().__dict__
        ##print api.get_userfollowing().__dict__

        ##print api.update_follow(follow_blog_url).__dict__
        ##print api.update_unfollow(follow_blog_url).__dict__

    except PytumbError, e:
        print e

else:
    try:
        redirect_url = auth.get_authorization_url()
        try:
            if webbrowser.open(redirect_url) == False:
                raise webbrowser.Error
        except webbrowser.Error:
            print 'webbrowser.Error'
            sys.exit(1)
        httpd = make_server('',8956,test_get_atoken)
        httpd.serve_forever()
    except PytumbError, e:
        print 'PytumbError! Error: %s' % e


