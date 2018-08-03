# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     admin_ui
   Description:
   Author:         caimmy
   date：          2018/6/26
-------------------------------------------------
   Change Activity:
                   2018/6/26
-------------------------------------------------
"""
__author__ = 'caimmy'

import tornado.web

class SideMenu(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        return self.render_string('uimodules/sidemenu.html')


class MainHeaderBar(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        return self.render_string("uimodules/mainheaderbar.html")


class Breadcrumb(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        return self.render_string("uimodules/breadcrumb.html", info=args)