# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     __init__.py
   Description:
   Author:         caimmy
   date：          2018/6/14
-------------------------------------------------
   Change Activity:
                   2018/6/14
-------------------------------------------------
"""
__author__ = 'caimmy'

import os
from lib import SSWebRequestHandler

class AdminWebRequestHandler(SSWebRequestHandler):
    def get_template_path(self):
        return os.path.join(os.path.dirname(__file__), 'template')