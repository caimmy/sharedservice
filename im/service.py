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
import tornado.log
import bp

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        tornado.log.app_log.debug("asdfadsasdfasd")
        tornado.log.access_log.error("access asdfasdf")
        tornado.log.gen_log.info("gen log asdfasdf")
        self.write("<h3>welcome to IM service</h3>")


def CreateBlueprint():
    '''
    创建IM业务子应用
    :return:
    '''
    return bp.Blueprint("/im", [(
        r"/?", IndexHandler
    )])