# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     authentication
   Description:
   Author:         caimmy
   date：          2018/6/14
-------------------------------------------------
   Change Activity:
                   2018/6/14
-------------------------------------------------
"""
__author__ = 'caimmy'

from lib import SSWebRequestHandler
from utils.wraps import request_authenticate

class LoginRequestHandler(SSWebRequestHandler):
    @request_authenticate
    def get(self):
        return self.write("success")