# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： service
Description:
Author: caimmy
date： 2018/8/31
-------------------------------------------------
Change Activity:
2018/8/31
-------------------------------------------------
"""
__author__ = 'caimmy'

from tornado.web import url
import bp

from papi.controllers.mimc_if import MimcTokenRefresh, MimcStatusChange
from papi.controllers.keep_live import KeepliveWsHandler

def CreateBlueprint():
    return bp.Blueprint(r"papi", [
        url(r"/mimc_token/?", MimcTokenRefresh, name="mimc_token_refresh"),
        url(r"/keepalive/?", KeepliveWsHandler, name="ws_keepalive"),                                # websocket reqeust handler

        url(r"/runtime/chat_mimc_status/?", MimcStatusChange, name="runtimelog_mimc_status_change")
    ])