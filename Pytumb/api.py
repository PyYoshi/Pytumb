#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.

from Pytumb.error import PytumbError
from Pytumb.api_binders import Bider4xml

import os
import mimetypes

class API(object):
    """Tumblr API"""
    # http://www.tumblr.com/docs/en/api

    def __init__(self, auth_handler=None,
                 username=None,
                 auth=None,
                 secure=False,
                 retry_count=0,
                 retry_delay=0,
                 retry_errors=None,
                 ):
        self.auth = auth_handler

        if self.auth:
            if username:
                self.username = username
            else:
                # Use Login-username
                ## FIXME: 'hoge'
                #self.username = self.auth._get_username()
                self.username = 'hoge'
        else:
            if username:
                self.username = username
            else:
                self.username = 'staff'

        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors

        self.secure = secure


    """ /api/read """
    # http://(user_id).tumblr.com/api/read
    # start - The post offset to start from. The default is 0.
    # num - The number of posts to return. The default is 20, and the maximum is 50.
    # type - The type of posts to return. If unspecified or empty, all types of posts are returned. Must be one of text, quote, photo, link, chat, video, or audio.
    # id - A specific post ID to return. Use instead of start, num, or type.
    # filter - Alternate filter to run on the text content. Allowed values:
        # text - Plain text only. No HTML.
        # none - No post-processing. Output exactly what the author entered. (Note: Some authors write in Markdown, which will not be converted to HTML when this option is used.)
    # tagged - Return posts with this tag in reverse-chronological order (newest first).
        # Optionally specify chrono=1 to sort in chronological order (oldest first).
    # search - Search for posts with this query.
    # state (Authenticated read required) - Specify one of the values draft, queue, or submission to list posts in the respective state. (this param is not implemented)
    def user_timeline(self, **kargs):
        # params: start, num, type, id, filter, tagged, search,
        binder = Bider4xml(api = self,
                    host = self.username + '.tumblr.com',
                    path = '/api/read',
                    kargs = kargs,
                    status_type = 'user',
                    require_auth = False,
                    json = True,
                    method = 'GET')
        return binder.execute()
    
    def get_status(self, **kargs):
        # params: id
        binder = Bider4xml(api = self,
                    host = self.username + '.tumblr.com',
                    path = '/api/read',
                    kargs = kargs,
                    status_type = 'user',
                    require_auth = False,
                    json = True,
                    method = 'GET')
        return binder.execute()

    """ /api/dashboard """
    # http://www.tumblr.com/api/dashboard
    # Authenticated read required.
    # start, num, type, filter (optional) - Identical to /api/read above. The maximum value of start is 250.
    # likes (optional) - 1 or 0, default 0. If 1, liked posts will have the liked="true" attribute.
    def home_timeline(self, **kargs):
        # params: start, num, type, filter, likes
        binder =Bider4xml(api = self,
                    host = 'www.tumblr.com',
                    path = '/api/dashboard',
                    kargs = kargs,
                    status_type = 'dashboard',
                    require_auth = True,
                    json = True,
                    method = 'GET')
        return binder.execute()


    """ http://www.tumblr.com/api/likes """
    #start, num, filter (optional) - Identical to /api/read above. The maximum value of start is 1000.
    def my_likes(self, **kargs):
        # params: start, num, filter
         binder = Bider4xml(api = self,
                    host = 'www.tumblr.com',
                    path = '/api/likes',
                    kargs = kargs,
                    status_type = 'my_likes',
                    require_auth = True,
                    json = False,
                    method = 'GET')
         return binder.execute()

    """ http://www.tumblr.com/api/like """
    # post-id - The numeric post ID to like.
    # reblog-key - The reblog-key value for the specified post from its XML as returned by /api/read or /api/dashboard.
    # POST request
    def update_like(self, **kargs):
        # params: reblog_key, post_id
        binder = Bider4xml(api = self,
                    host = 'www.tumblr.com',
                    path = '/api/like',
                    kargs = kargs,
                    status_type = 'update',
                    require_auth = True,
                    json = False,
                    ptype='like',
                    method = 'POST')
        return binder.execute()

    """  http://www.tumblr.com/api/unlike """
    # post-id - The numeric post ID to like.
    # reblog-key - The reblog-key value for the specified post from its XML as returned by /api/read or /api/dashboard.
    # POST request
    def update_unlike(self, **kargs):
        # params: reblog-key, post-id
        binder = Bider4xml(api = self,
                    host = 'www.tumblr.com',
                    path = '/api/unlike',
                    allowed_param = ['post-id', 'reblog-key'],
                    kargs = kargs,
                    status_type = 'update',
                    require_auth = True,
                    json = False,
                    method = 'POST')
        return binder.execute()


    """ /api/pages """
    # Not understanded. XD
    def get_pages(self):
        # params: Nothing
        binder = Bider4xml(api = self,
                    host = self.username + '.tumblr.com',
                    path = '/api/pages',
                    require_auth = False,
                    status_type = 'pages',
                    json = False,
                    method = 'GET')
        return binder.execute()


    """ http://www.tumblr.com/api/write """
    # type - The post type.
    # (content parameters) - These vary by post type.
    # generator (optional) - A short description of the application making the request for tracking and statistics, such as "John's Widget 1.0". Must be 64 or fewer characters.
    # date (optional) - The post date, if different from now, in the blog's timezone. Most unambiguous formats are accepted, such as '2007-12-01 14:50:02'. Dates may not be in the future.
    # private (optional) - 1 or 0. Whether the post is private. Private posts only appear in the Dashboard or with authenticated links, and do not appear on the blog's main page.
    # tags (optional) - Comma-separated list of post tags. You may optionally enclose tags in double-quotes.
    # format (optional) - html or markdown.
    # group (optional) - Post this to a secondary blog on your account, e.g. mygroup.tumblr.com (for public groups only)
    # slug (optional) - A custom string to appear in the post's URL: myblog.tumblr.com/post/123456/this-string-right-here. URL-friendly formatting will be applied automatically. Maximum of 55 characters.
    # state (optional) - One of the following values:
        # published (default)
        # draft - Save in the tumblelog's Drafts folder for later publishing.
        # submission - Add to the tumblelog's Messages folder for consideration.
        # queue - Add to the tumblelog's queue for automatic publishing in a few minutes or hours. To publish at a specific time in the future instead, specify an additional publish-on parameter with the date expression in the tumblelog's local time (e.g. publish-on=2010-01-01T13:34:00). If the date format cannot be understood, a 401 error will be returned and the post will not be created.
      # To change the state of an existing post, such as to switch from draft to published, follow the editing process and pass the new value as the state parameter.
      # Note: If a post has previously been saved as a draft, queue, or submission post, it will be assigned a new post ID the first time it enters the published state.
    # send-to-twitter (optional, ignored on edits) - One of the following values, if the tumblelog has Twitter integration enabled:
        # no (default) - Do not send this post to Twitter.
        # auto - Send to Twitter with an automatically generated summary of the post.
        # (any other value) - A custom message to send to Twitter for this post.
      # If this parameter is unspecified, API-created posts will be sent to Twitter if the "Send my Tumblr posts to Twitter" checkbox in the Customize screen is checked.

    # multipart/form-data method, like a file upload box in a web form. Maximum size:
        # 50 MB for videos
        # 10 MB for photos
        # 10 MB for audio
      # This is recommended since there's much less overhead.
    # Normal POST method, in which the file's entire binary contents are URL-encoded like any other POST variable. Maximum size:
        # 5 MB for videos
        # 5 MB for photos
        # 5 MB for audio
    # Return values - We return standard HTTP status codes for each request, plus a plaintext response.
        # 201 Created - Success! The newly created post's ID is returned.
        # 403 Forbidden - Your email address or password were incorrect.
        # 400 Bad Request - There was at least one error while trying to save your post. Errors are sent in plain text, one per line.

    # regular - Requires at least one:
        # title
        # body (HTML allowed)
    def update_regular(self, **kargs):
        # params: title, body, generator, date, private, tags, format, group, slug, state, send-to-twitter
        binder = Bider4xml(api = self,
                        host = 'www.tumblr.com',
                        path = '/api/write',
                        kargs = kargs,
                        status_type = 'update',
                        require_auth = True,
                        json = False,
                        method = 'POST',
                        ptype = 'regular')
        return binder.execute()

    # photo - Requires either source or data, but not both. If both are specified,source is used.
        # source - The URL of the photo to copy. This must be a web-accessible URL, not a local file or intranet location.
        # data - An image file. See File uploads below.
        # caption (optional, HTML allowed)
        # click-through-url (optional)
    def update_photo(self, file_path, **kargs):
        # params: source, data, caption, click-through-url, generator, date, private, tags, format, group, slug, state, send-to-twitter
        binder = Bider4xml(api = self,
                        host = 'www.tumblr.com',
                        path = '/api/write',
                        kargs = kargs,
                        file_path = file_path,
                        max_size = 10000,
                        status_type = 'update_file',
                        require_auth = True,
                        json = False,
                        method = 'POST',
                        ptype = 'photo')
        return binder.execute()

    # quote
        # quote
        # source (optional, HTML allowed)
    def update_quote(self, **kargs):
        # params: quote, source, generator, date, private, tags, format, group, slug, state, send-to-twitter
        binder = Bider4xml(api = self,
                        host = 'www.tumblr.com',
                        path = '/api/write',
                        kargs = kargs,
                        status_type = 'update',
                        require_auth = True,
                        json = False,
                        method = 'POST',
                        ptype = 'quote')
        return binder.execute()

    # link
        # name (optional)
        # url
        # description (optional, HTML allowed)
    def update_link(self, **kargs):
        # params: name, url, description, generator, date, private, tags, format, group, slug, state, send-to-twitter
        binder = Bider4xml(api = self,
                        host = 'www.tumblr.com',
                        path = '/api/write',
                        allowed_param = ['type', 'name', 'url', 'description',
                                        'generator', 'date', 'private', 'tags',
                                        'format', 'group', 'slug', 'state',
                                        'send-to-twitter'
                                        ],
                        kargs = kargs,
                        status_type = 'update',
                        require_auth = True,
                        json = False,
                        method = 'POST',
                        ptype = 'link')
        return binder.execute()

    # conversation
        # title
        # conversation
    def update_conversation(self, **kargs):
        # params: title, conversation, generator, date, private, tags, format, group, slug, state, send-to-twitter
        binder = Bider4xml(api = self,
                        host = 'www.tumblr.com',
                        path = '/api/write',
                        kargs = kargs,
                        status_type = 'update',
                        require_auth = True,
                        json = False,
                        method = 'POST',
                        ptype = 'conversation')
        return binder.execute()

    # video - Requires either embed or data, but not both.
        # embed - Either the complete HTML code to embed the video, or the URL of a YouTube video page.
        # data - A video file for a Vimeo upload. See File uploads below.
        # title (optional) - Only applies to Vimeo uploads.
        # caption (optional, HTML allowed)
    def update_video(self, file_path, **kargs):
        # params: embed, data, title, caption, generator, date, private, tags, format, group, slug, state, send-to-twitter
        binder = Bider4xml(api = self,
                        host = 'www.tumblr.com',
                        path = '/api/write',
                        kargs = kargs,
                        file_path = file_path,
                        max_size = 50000,
                        status_type = 'update_file',
                        require_auth = True,
                        json = False,
                        method = 'POST',
                        ptype = 'video')
        return binder.execute()

    # audio
        # data - An audio file. Must be MP3 or AIFF format. See File uploads below.
        # externally-hosted-url (optional, replaces data) - Create a post that uses this externally hosted audio-file URL instead of having Tumblr copy and host an uploaded file. Must be MP3 format. No size or duration limits are imposed on externally hosted files.
        # caption (optional, HTML allowed)
    def update_audio(self, file_path, **kargs):
        # params: data, externally-hosted-url, caption, generator, date, private, tags, format, group, slug, state, send-to-twitter
        binder = Bider4xml(api = self,
                        host = 'www.tumblr.com',
                        path = '/api/write',
                        kargs = kargs,
                        file_path = file_path,
                        max_size = 10000,
                        status_type = 'update_file',
                        require_auth = True,
                        json = False,
                        method = 'POST',
                        ptype = 'audio')
        return binder.execute()

    # Editing posts
        # post-id - The integer ID of the post you wish to edit.
        # type, private, format - These are ignored and can be omitted. These values cannot be changed after post creation.
        # tags, generator, date - These are optional. If specified, the new values will override the previous values. If omitted, the values are not changed.
        # You must pass all content parameters for the post's type (e.g. title, body for text posts) even if you are not changing their values.
    def editing_post(self, **kargs):
        # params: post-id, generator, date, tags, group, slug, state, send-to-twitter
        binder = Bider4xml(api = self,
                        host = 'www.tumblr.com',
                        path = '/api/write',
                        kargs = kargs,
                        status_type = 'update',
                        require_auth = True,
                        json = False,
                        method = 'POST',
                        ptype = 'edit',
                        not_implemented = True)
        return binder.execute()


    """ http://www.tumblr.com/api/delete """
    # All content-related parameters will be ignored and can be omitted. Only the authentication parameters and post-id are required
    # pass an additional POST parameter:
        # post-id - The integer ID of the post you wish to delete.
    def delete_post(self, **kargs):
        # param: post-id
        binder = Bider4xml(api = self,
                        host = 'www.tumblr.com',
                        path = '/api/delete',
                        kargs = kargs,
                        status_type = 'delete',
                        require_auth = True,
                        json = False,
                        method = 'POST')
        return binder.execute()


    """ http://www.tumblr.com/api/reblog """
    # pass these POST parameters:
        # post-id - The integer ID of the post to reblog.
        # reblog-key - The corresponding reblog-key value from the post's /api/read XML data.
        # comment (optional) - Text, HTML, or Markdown string (see format) of the commentary added to the reblog. It will appear below the automatically generated reblogged-content structure. Up to 2000 characters allowed (as UTF-8 characters, not bytes). This field is not supported, and is ignored, for chat posts.
        # as (optional) - Reblog as a different format from the original post. text, link, and quote are supported.
      # The format and group parameters from /api/write are also supported.
    def update_reblog(self, **kargs):
        # params: post-id, reblog-key, comment, as
        binder = Bider4xml(api = self,
                        host = 'www.tumblr.com',
                        path = '/api/reblog',
                        require_auth = True,
                        json = False,
                        method = 'POST')
        return binder.execute()


    #
    def get_account_info(self):
        # param: Nothing
        binder = Bider4xml(api = self,
                    host = 'www.tumblr.com',
                    path = '/api/authenticate',
                    status_type = 'accountinfo',
                    require_auth = True,
                    json = False,
                    method = 'POST')
        return binder.execute()

    @staticmethod
    def _encode_multipart_formdata(params, file_path, max_size):
        # http://www.bekkoame.ne.jp/~poetlabo/WWW/rfc2388J.html
        try:
            if os.path.getsize(file_path) > (max_size * 1024):
                raise PytumbError('File is too big, must be less than %d' % (max_size * 1024) )
        except os.errno, e:
            raise PytumbError('Unable to access file, %s' % e)

        file_type = mimetypes.guess_type(file_path)
        if file_type is None:
            raise PytumbError('Could not datermine file type')
        file_type = file_type[0]
        if file_type not in ['image/bmp', 'image/x-bmp', 'image/x-MS-bmp', 'image/gif', 'image/jpeg', 'image/pjpeg' ,'image/png', 'image/x-png']:
            raise  PytumbError('Invalid file type for image: %s' % file_path)

        BOUNDARY = '---IlOvEpYtHoN'

        body = []
        # For params
        for k, v in params.items():
            body.append('--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="%s"' % k)
            body.append('')
            body.append(v)
        #For file
        body.append('--' + BOUNDARY)
        filename = os.path.basename(file_path)
        body.append('Content-Disposition: form-data; name="data"; filename="%s"' % filename)
        body.append('Content-Type: %s' % file_type)
        body.append('')
        fp = open(file_path, 'rb')
        body.append(fp.read())
        fp.close()
        # End
        body.append('--' + BOUNDARY + '--')
        body.append('')
        body = '\r\n'.join(body)

        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body
        

class exAPI(object):

    # **Experimental function **
    # Warning: Terms of is a violation
    # Scraiping tumblr pages

    """
    print 'exAPI is Experimental functions.\nTake full responsibility for your actions.'
    """
    def __init__(self):
        pass

