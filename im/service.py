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

import tornado.log

from lib import SSWebRequestHandler
import bp

from im.mimc_api import FetchMIMCToken, ProxyPushP2PMessage

async def bbb(s):
    tornado.log.gen_log.error(s)
    return 1

class IndexHandler(SSWebRequestHandler):
    async def get(self):
        tornado.log.gen_log.error("asdfasdfasdf")
        self.write("<h3>welcome to IM service</h3>")


def CreateBlueprint():
    '''
    创建IM业务子应用
    :return:
    '''
    return bp.Blueprint("/im", [
        (r"/?", IndexHandler),
        (r"/fetchmimctoken/?", FetchMIMCToken),
        (r"/p2p/?", ProxyPushP2PMessage)
    ])