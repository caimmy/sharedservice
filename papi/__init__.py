# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： __init__.py
Description:
Author: caimmy
date： 2018/8/31
-------------------------------------------------
Change Activity:
2018/8/31
-------------------------------------------------
"""
__author__ = 'caimmy'

from lib import SSWebDataRequestHandler

class PrivateApiRequestHandler(SSWebDataRequestHandler):
    def prepare(self):
        super(PrivateApiRequestHandler, self).prepare()