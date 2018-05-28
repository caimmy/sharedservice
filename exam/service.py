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

import tornado.web
import bp

class IndexRequest(tornado.web.RequestHandler):
    def get(self):
        self.write("<h3>Welcome to Examination application</h3>")

def CreateBlueprint():
    return bp.Blueprint("exam", [
        (r"/?", IndexRequest)
    ])