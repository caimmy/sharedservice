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

from papi.mimc_if import MimcTokenRefresh

def CreateBlueprint():
    return bp.Blueprint(r"papi", [
        url(r"/mimc_token?", MimcTokenRefresh, name="mimc_token_refresh"),
    ])