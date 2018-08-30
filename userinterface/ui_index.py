# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： ui_index
Description:
Author: caimmy
date： 2018/8/29
-------------------------------------------------
Change Activity:
2018/8/29
-------------------------------------------------
"""
__author__ = 'caimmy'

from userinterface import UserinterfaceWebRequestHandler


class TextserviceRequestHandler(UserinterfaceWebRequestHandler):
    def get(self, *args, **kwargs):
        return self.render("text_service.html")