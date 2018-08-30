# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： service
Description:
Author: caimmy
date： 2018/8/29
-------------------------------------------------
Change Activity:
2018/8/29
-------------------------------------------------
"""
__author__ = 'caimmy'

from tornado.web import url
import bp
from userinterface.ui_index import TextserviceRequestHandler

def CreateBlueprint():
    return bp.Blueprint(r"ui", [
        url(r"/ts/?", TextserviceRequestHandler, name="text_service_proxy_url"),
    ])