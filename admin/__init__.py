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
import traceback
from lib import SSWebRequestHandler

class AdminWebRequestHandler(SSWebRequestHandler):
    def get_template_path(self):
        return os.path.join(os.path.dirname(__file__), 'template')

    def write_error(self, status_code, **kwargs):
        if self.application.settings.get("debug"):
            error_trace_list = traceback.format_exception(*kwargs.get("exc_info"))
            # from web.py
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in error_trace_list:
                self.write(line)
            self.finish()
        else:
            if 404 == status_code:
                return self.render("404.html")
            else:
                err_details = kwargs.get("exc_info")
                err_info = ""
                if (1 < len(err_details)):
                    err_info = str(err_details[1])
                return self.render("500.html", err=err_info)