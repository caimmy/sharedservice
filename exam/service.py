# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     service
   Description:
   Author:         caimmy
   date：          2018/5/28
-------------------------------------------------
   Change Activity:
                   2018/5/28
-------------------------------------------------
"""
__author__ = 'caimmy'

from tornado.web import url
from lib import SSWebRequestHandler
import bp

class IndexRequest(SSWebRequestHandler):
    def get(self):
        self.write("<h3>Welcome to Examination application</h3>")

def CreateBlueprint():
    return bp.Blueprint("exam", [
        url(r"/?", IndexRequest)
    ])