# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： __init__.py
Description:  客服后台界面
Author: caimmy
date： 2018/8/21
-------------------------------------------------
Change Activity:
2018/8/21
-------------------------------------------------
"""
__author__ = 'caimmy'

import os

from lib import SSWebRequestHandler

class CustomerWebRequestHandler(SSWebRequestHandler):
    def get_template_path(self):
        return os.path.join(os.path.dirname(__file__), 'template')

    def write_error(self, status_code, **kwargs):
        return self.write(str(status_code) + __file__)