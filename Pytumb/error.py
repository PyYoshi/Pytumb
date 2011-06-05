# Pytumb
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.
# Based tweepy. Thanks Joshua Roesslein.

class PytumbError(Exception):
    """Pytumb exception"""

    def __init__(self, reason, response=None):
        self.reason = str(reason)
        self.response = response
        #print self.response

    def __str__(self):
        return self.reason