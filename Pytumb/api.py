#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.

from Pytumb.error import PytumbError
from Pytumb.api_binders import Binder
from Pytumb.utils import Utils
import os
import mimetypes

class API(object):
    """Tumblr API v2"""
    # http://www.tumblr.com/docs/en/api/v2

    def __init__(self, auth_handler,
                 retry_count=0,
                 retry_delay=0,
                 retry_errors=None,
                 ):

        self.auth = auth_handler
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.api_version = 'v2'
        self.api_domain = 'api.tumblr.com'

    ###########################################################
    #####                    Blog Methods                 #####
    ###########################################################
    """ /info — Retrieve Blog Info """
    def get_bloginfo(self, blog_hostname):
        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = blog_hostname,
                    api_path = '/info',
                    status_type = 'bloginfo',
                    auth_type = 'api_key',
                    method = 'GET')
        return binder.execute()

    """ /avatar — Retrieve a Blog Avatar """
    def get_blogavatar(self, blog_hostname, size=64):
        sizes = [16, 24, 30, 40, 48, 64, 96, 128, 512]
        payload = {}
        if size:
            if not isinstance(size, int):
                raise PytumbError('size is not int type.')
            if size in sizes:
                payload['size'] = size
            else:
                raise PytumbError('Invalid size. Supported size: %s') % sizes

        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = blog_hostname,
                    api_path = '/avatar',
                    payload = payload,
                    status_type = 'binary',
                    method = 'GET')
        return binder.execute()

    """ /followers — Retrieve a Blog's Followers """
    #
    def get_blogfollowers(self, own_blog_hostname, limit=20, offset=0):
        payload = {}
        if limit:
            if not isinstance(limit, int):
                raise PytumbError('limit is invalid int type.')
            payload['limit'] = limit
        if offset:
            if not isinstance(offset, int):
                raise PytumbError('offset is invalid int type.')
            payload['offset'] = offset

        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/followers',
                    payload = payload,
                    status_type = 'blogfollowers',
                    auth_type = 'oauth',
                    method = 'GET')
        return binder.execute()

    """ /posts – Retrieve Published Posts """
    #
    def get_blogposts(self, blog_hostname,posts_type=None, post_id=None, posts_tag=None, limit=20, offset=0, reblog_info=False, notes_info=False,post_format=None):
        payload = {}
        if post_id:
            payload['id'] = post_id
        if posts_tag:
            if not isinstance(posts_tag, list):
                raise PytumbError('posts_tag is invalid list type.')
            payload['tag'] = posts_tag
        if limit:
            if not isinstance(limit, int):
                raise PytumbError('limit is invalid int type.')
            payload['limit'] = limit
        if offset:
            if not isinstance(offset, int):
                raise PytumbError('offset is invalid int type.')
            payload['offset'] = offset
        if reblog_info:
            if not isinstance(reblog_info, bool):
                raise PytumbError('reblog_info is invalid bool type.')
            payload['reblog_info'] = reblog_info
        if notes_info:
            if not isinstance(notes_info, bool):
                raise PytumbError('notes_info is invalid bool type.')
            payload['notes_info'] = notes_info
        if post_format == 'text' or post_format == 'raw':
            payload['format'] = post_format
        elif not post_format:
            pass
        else:
            raise PytumbError('post_format must be either "text" or "raw".')
        
        if posts_type:
            api_path = '/posts/' + posts_type
        else:
            api_path = '/posts'
        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = blog_hostname,
                    api_path = api_path,
                    payload = payload,
                    status_type = 'blogposts',
                    auth_type = 'api_key',
                    method = 'GET')
        return binder.execute()

    """ /posts/queue — Retrieve Queued Posts """
    #
    def get_queuedposts(self, own_blog_hostname):
        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/posts/queue',
                    status_type = 'blogposts',
                    auth_type = 'oauth',
                    method = 'GET')
        return binder.execute()

    """ /posts/draft — Retrieve Draft Posts """
    #
    def get_draftposts(self, own_blog_hostname):
        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/posts/draft',
                    status_type = 'blogposts',
                    auth_type = 'oauth',
                    method = 'GET')
        return binder.execute()

    """ /posts/submission — Retrieve Submission Posts """
    #
    def get_submissionposts(self, own_blog_hostname):
        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/posts/submission',
                    status_type = 'blogposts',
                    auth_type = 'oauth',
                    method = 'GET')
        return binder.execute()

    """ /post — Create a New Blog Post """
    # Returns 201: Created or an error code.
    def update_text(self, own_blog_hostname, body, title=None, state='published', tags=[], tweet=None, post_date=None, markdown=False, slug=None):
        # state = ['published', 'draft', 'queue']
        # tweet: add tweet message.
        # post_date: GMT date
        # markdown: True or False
        # title: string, html is escaped.
        # body: html allowed.
        payload = {}
        payload['body'] = body
        if title:
            payload['title'] = title

        payload['type'] = 'text'
        if state == 'published' or state == 'draft' or state == 'queue':
            payload['state'] = state
        elif not state:
            pass
        else:
            raise PytumbError('state must be either "published" or "draft" or "queue".')
        if tags:
            if not isinstance(tags, list):
                raise PytumbError('tags is invalid list type.')
            payload['tags'] = tags
        if tweet:
            payload['tweet'] = tweet
        if post_date:
            payload['date'] = post_date
        if markdown:
            if not isinstance(markdown, bool):
                raise PytumbError('markdown is invalid bool type.')
            payload['markdown'] = markdown
        if slug:
            payload['slug'] = slug

        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/post',
                    payload = payload,
                    status_type = 'raw',
                    auth_type = 'oauth',
                    method = 'POST')
        return binder.execute()

    def update_photo(self, own_blog_hostname, state='published', tags=[], tweet=None, post_date=None, markdown=False, slug=None, caption=None, link=None, source=None, file_path=None):
        # state: ['published', 'draft', 'queue']
        # tweet
        # post_date: GMT date
        # markdown: True or False
        # caption: html allowed
        # link: "click-through URL", photo's source-link.
        # source: source is link. tumblr fetch photo from link.
        # file_path:

        payload  = {}
        if caption:
            payload['caption'] = caption
        if link:
            payload['link'] = link
        if source and file_path:
            raise PytumbError('Must be either source or file_path, not both these.')
        elif source:
            payload['source'] = source
        elif file_path:
            data = Utils.chkFile(file_path, 5000)
            payload['data'] = data
        else:
            raise PytumbError('Must be either source or file_path, not both these.')

        payload['type'] = 'photo'
        if state == 'published' or state == 'draft' or state == 'queue':
            payload['state'] = state
        elif not state:
            pass
        else:
            raise PytumbError('state must be either "published" or "draft" or "queue".')
        if tags:
            if not isinstance(tags, list):
                raise PytumbError('tags is invalid list type.')
            payload['tags'] = tags
        if tweet:
            payload['tweet'] = tweet
        if post_date:
            payload['date'] = post_date
        if markdown:
            if not isinstance(markdown, bool):
                raise PytumbError('markdown is invalid bool type.')
            payload['markdown'] = markdown
        if slug:
            payload['slug'] = slug

        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/post',
                    payload = payload,
                    status_type = 'raw',
                    auth_type = 'oauth',
                    method = 'POST')
        return binder.execute()

    def update_quote(self, own_blog_hostname, quote, state='published', tags=[], tweet=None, post_date=None, markdown=False, slug=None, source=None):
        # state = ['published', 'draft', 'queue']
        # tweet
        # post_date: GMT date
        # markdown: True or False
        # quote: html is escaped.
        # source: html allowed.

        payload = {}
        payload['quote'] = quote
        if source:
            payload['source'] = source
        payload['type'] = 'quote'
        if state == 'published' or state == 'draft' or state == 'queue':
            payload['state'] = state
        elif not state:
            pass
        else:
            raise PytumbError('state must be either "published" or "draft" or "queue".')
        if tags:
            if not isinstance(tags, list):
                raise PytumbError('tags is invalid list type.')
            payload['tags'] = tags
        if tweet:
            payload['tweet'] = tweet
        if post_date:
            payload['date'] = post_date
        if markdown:
            if not isinstance(markdown, bool):
                raise PytumbError('markdown is invalid bool type.')
            payload['markdown'] = markdown
        if slug:
            payload['slug'] = slug

        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/post',
                    payload = payload,
                    status_type = 'raw',
                    auth_type = 'oauth',
                    method = 'POST')
        return binder.execute()

    def update_link(self, own_blog_hostname, url, state='published', tags=[], tweet=None, post_date=None, markdown=False, slug=None,description=None):
        # state = ['published', 'draft', 'queue']
        # tweet
        # post_date: GMT date
        # markdown: True or False
        # description: html allowed.

        payload = {}
        payload['link'] = link
        if description:
            payload['description'] = description
        payload['type'] = 'link'
        if state == 'published' or state == 'draft' or state == 'queue':
            payload['state'] = state
        elif not state:
            pass
        else:
            raise PytumbError('state must be either "published" or "draft" or "queue".')
        if tags:
            if not isinstance(tags, list):
                raise PytumbError('tags is invalid list type.')
            payload['tags'] = tags
        if tweet:
            payload['tweet'] = tweet
        if post_date:
            payload['date'] = post_date
        if markdown:
            if not isinstance(markdown, bool):
                raise PytumbError('markdown is invalid bool type.')
            payload['markdown'] = markdown
        if slug:
            payload['slug'] = slug

        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/post',
                    payload = payload,
                    status_type = 'raw',
                    auth_type = 'oauth',
                    method = 'POST')
        return binder.execute()

    def update_chat(self, own_blog_hostname,conversation,state='published', tags=[], tweet=None, post_date=None, markdown=False, slug=None,title=None):
        # state = ['published', 'draft', 'queue']
        # tweet
        # post_date: GMT date
        # markdown: True or False
        # title
        # conversation: conversation/chat with dialogue labels. no html.

        payload = {}
        payload['conversation'] = conversation
        if title:
            payload['title'] = title
        payload['type'] = 'chat'
        if state == 'published' or state == 'draft' or state == 'queue':
            payload['state'] = state
        elif not state:
            pass
        else:
            raise PytumbError('state must be either "published" or "draft" or "queue".')
        if tags:
            if not isinstance(tags, list):
                raise PytumbError('tags is invalid list type.')
            payload['tags'] = tags
        if tweet:
            payload['tweet'] = tweet
        if post_date:
            payload['date'] = post_date
        if markdown:
            if not isinstance(markdown, bool):
                raise PytumbError('markdown is invalid bool type.')
            payload['markdown'] = markdown
        if slug:
            payload['slug'] = slug

        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/post',
                    payload = payload,
                    status_type = 'raw',
                    auth_type = 'oauth',
                    method = 'POST')
        return binder.execute()

    def update_audio(self, own_blog_hostname,state='published', tags=[], tweet=None, post_date=None, markdown=False, slug=None,caption=None,external_url=None, file_path=None):
        # state = ['published', 'draft', 'queue']
        # tweet
        # post_date: GMT date
        # markdown: True or False
        # caption
        # external_url
        # file_path

        payload = {}
        if caption:
            payload['caption'] = caption

        if external_url and file_path:
            raise PytumbError('Must be either external_url or file_path, not both these.')
        elif external_url:
            payload['external_url'] = external_url
        elif file_path:
            data = Utils.chkFile(file_path, 5000)
            payload['data'] = data
        else:
            raise PytumbError('Must be either external_url or file_path, not both these.')

        payload['type'] = 'audio'
        if state == 'published' or state == 'draft' or state == 'queue':
            payload['state'] = state
        elif not state:
            pass
        else:
            raise PytumbError('state must be either "published" or "draft" or "queue".')
        if tags:
            if not isinstance(tags, list):
                raise PytumbError('tags is invalid list type.')
            payload['tags'] = tags
        if tweet:
            payload['tweet'] = tweet
        if post_date:
            payload['date'] = post_date
        if markdown:
            if not isinstance(markdown, bool):
                raise PytumbError('markdown is invalid bool type.')
            payload['markdown'] = markdown
        if slug:
            payload['slug'] = slug

        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/post',
                    payload = payload,
                    status_type = 'raw',
                    auth_type = 'oauth',
                    method = 'POST')
        return binder.execute()

    def update_video(self, own_blog_hostname,state='published', tags=[], tweet=None, post_date=None, markdown=False, slug=None,caption=None, embed=None, file_path=None):
        # state = ['published', 'draft', 'queue']
        # tweet
        # post_date: GMT date
        # markdown: True or False
        # caption
        # embed: html embed code. <embed></embed>
        # file_path

        payload = {}
        if caption:
            payload['caption'] = caption

        if external_url and file_path:
            raise PytumbError('Must be either external_url or file_path, not both these.')
        elif embed:
            payload['embed'] = embed
        elif file_path:
            data = Utils.chkFile(file_path, 5000)
            payload['data'] = data
        else:
            raise PytumbError('Must be either external_url or file_path, not both these.')

        payload['type'] = 'video'
        if state == 'published' or state == 'draft' or state == 'queue':
            payload['state'] = state
        elif not state:
            pass
        else:
            raise PytumbError('state must be either "published" or "draft" or "queue".')
        if tags:
            if not isinstance(tags, list):
                raise PytumbError('tags is invalid list type.')
            payload['tags'] = tags
        if tweet:
            payload['tweet'] = tweet
        if post_date:
            payload['date'] = post_date
        if markdown:
            if not isinstance(markdown, bool):
                raise PytumbError('markdown is invalid bool type.')
            payload['markdown'] = markdown
        if slug:
            payload['slug'] = slug

        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/post',
                    payload = payload,
                    status_type = 'raw',
                    auth_type = 'oauth',
                    method = 'POST')
        return binder.execute()

    """ /post/edit – Edit a Blog Post """
    #　Returns 200: OK (successfully edited) or an error code.
    def edit_post(self, blog_hostname, post_id, post_type):
        # post_typeによって必要なパラメを条件にして処理
        payload = {
            'id':post_id
        }

        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/post/edit',
                    payload = payload,
                    status_type = 'raw',
                    auth_type = 'oauth',
                    method = 'POST')
        return binder.execute()

    """ /post/reblog – Reblog a Post """
    #
    def update_reblog(self, own_blog_hostname,reblog_key, post_id, comment=None):
        # Returns 201: Created or an error code.
        # reblog_key
        # post_id
        # comment
        payload = {}
        payload['reblog_key'] = reblog_key
        payload['id'] = post_id
        if comment:
            payload['comment'] = comment
        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/post/reblog',
                    payload = payload,
                    status_type = 'raw',
                    auth_type = 'oauth',
                    method = 'POST')
        return binder.execute()

    """ /post/delete – Delete a Post """
    # Returns 200: OK (successfully deleted) or an error code.
    def delete_post(self, own_blog_hostname, post_id):
        payload = {}
        payload['id'] = post_id
        binder = Binder(api = self,
                    api_method_path = '/blog',
                    blog_hostname = own_blog_hostname,
                    api_path = '/post/delete',
                    payload = payload,
                    status_type = 'raw',
                    auth_type = 'oauth',
                    method = 'POST')
        return binder.execute()

    ###########################################################
    #####                    User Methods                 #####
    ###########################################################

    """ /user/info – Get a User's Information """
    #
    def get_userinfo(self):
        binder = Binder(api = self,
                    api_method_path = '/user',
                    api_path = '/info',
                    status_type = 'userinfo',
                    auth_type = 'oauth',
                    method = 'POST')
        return binder.execute()

    """ /user/dashboard – Retrieve a User's Dashboard """
    #
    def get_dashboard(self,limit=20, offset=0, post_type=None, since_id=0, reblog_info=False, notes_info=False):
        payload = {}
        if post_type:
            payload['post_type'] = post_type

        if limit:
            if not isinstance(limit, int):
                raise PytumbError('limit is invalid int type.')
            payload['limit'] = limit
        if offset:
            if not isinstance(offset, int):
                raise PytumbError('offset is invalid int type.')
            payload['offset'] = offset
        if since_id:
            if not isinstance(since_id, int):
                raise PytumbError('since_id is invalid int type.')
            payload['since_id'] = since_id
        if reblog_info:
            if not isinstance(reblog_info, bool):
                raise PytumbError('reblog_info is invalid bool type.')
            payload['reblog_info'] = reblog_info
        if notes_info:
            if not isinstance(notes_info, bool):
                raise PytumbError('notes_info is invalid bool type.')
            payload['notes_info'] = notes_info

        binder = Binder(api = self,
                    api_method_path = '/user',
                    api_path = '/dashboard',
                    payload = payload,
                    status_type = 'dashboard',
                    auth_type = 'oauth',
                    method = 'GET')
        return binder.execute()

    """ /user/likes — Retrieve a User's Likes """
    #
    def get_userlikes(self,limit=20, offset=0):
        payload = {}
        if limit:
            if not isinstance(limit, int):
                raise PytumbError('limit is invalid int type.')
            payload['limit'] = limit
        if offset:
            if not isinstance(offset, int):
                raise PytumbError('offset is invalid int type.')
            payload['offset'] = offset
        binder = Binder(api = self,
                    api_method_path = '/user',
                    api_path = '/likes',
                    payload = payload,
                    status_type = 'userlikes',
                    auth_type = 'oauth',
                    method = 'GET')
        return binder.execute()

    """ /user/following – Retrieve the Blogs a User Is Following """
    #
    def get_userfollowing(self, limit=20, offset=0):
        payload = {}
        if limit:
            if not isinstance(limit, int):
                raise PytumbError('limit is invalid int type.')
            payload['limit'] = limit
        if offset:
            if not isinstance(offset, int):
                raise PytumbError('offset is invalid int type.')
            payload['offset'] = offset
        binder = Binder(api = self,
                    api_method_path = '/user',
                    api_path = '/following',
                    payload = payload,
                    status_type = 'userfollowing',
                    auth_type = 'oauth',
                    method = 'GET')
        return binder.execute()

    """ /user/follow – Follow a blog """
    # Returns 200: OK (blog successfully followed) or a 404 (blog was not found)
    def update_follow(self, blog_url):
        payload = {}
        payload['url'] = blog_url
        binder = Binder(api = self,
                    api_method_path = '/user',
                    api_path = '/follow',
                    payload = payload,
                    status_type = 'followunfollow',
                    auth_type = 'oauth',
                    method = 'POST')
        return binder.execute()

    """ /user/unfollow – Unfollow a blog """
    # Returns 200: OK (blog successfully unfollowed) or a 404 (blog was not found)
    def update_unfollow(self, blog_url):
        payload = {}
        payload['url'] = blog_url
        binder = Binder(api = self,
                    api_method_path = '/user',
                    api_path = '/unfollow',
                    payload = payload,
                    status_type = 'followunfollow',
                    auth_type = 'oauth',
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
        
"""
class OldAPI(object):

    # ** Deprecated: Function **
    # Not only required authentication.

    def __init__(self):
        pass

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
"""