# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     wraps
   Description:
   Author:         caimmy
   date：          2018/6/14
-------------------------------------------------
   Change Activity:
                   2018/6/14
-------------------------------------------------
"""
__author__ = 'caimmy'
import json
import functools
from lib import makeResponse

def request_authenticate(method):
    @functools.wraps(method)
    def check_authentication(self, *args, **kwargs):
        if not self.current_user:
            self.write(json.dumps(makeResponse('login first please')))
        else:
            return method(self, *args, **kwargs)
    return check_authentication