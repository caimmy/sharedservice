# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     service
   Description:
   Author:         caimmy
   date：          2018/6/14
-------------------------------------------------
   Change Activity:
                   2018/6/14
-------------------------------------------------
"""
__author__ = 'caimmy'

from tornado.web import url
import tornado
import bp

from admin.authentication import LoginRequestHandler, RegisterRequestHandler, IndexRequestHandler, AdminloginRequestHandler, \
    AdminlogoutRequestHandler


class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        self.write("error: " + str(status_code))

def CreateBlueprint():
    return bp.Blueprint(r'admin', [
        url(r'/?', IndexRequestHandler, name="admin_index"),
        url(r'/register/?', RegisterRequestHandler),
        (r'/login/?', LoginRequestHandler),
        url(r'/adminlogin/?', AdminloginRequestHandler, name="login"),
        url(r'/logout', AdminlogoutRequestHandler, name="logout"),
        url(r'.*', BaseHandler)
    ])