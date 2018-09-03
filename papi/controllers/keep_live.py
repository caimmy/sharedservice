# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： keep_live
Description: 用户连接保活，用以判断用户是否已经断开连接
Author: caimmy
date： 2018/9/3
-------------------------------------------------
Change Activity:
2018/9/3
-------------------------------------------------
"""
__author__ = 'caimmy'

from datetime import datetime
from lib import SSWebRequestHandler

class KeepliveWsHandler(SSWebRequestHandler):
    def open(self, *args, **kwargs):
        print("on open")

    def on_message(self, message):
        print("on message")
        print(message)
        print("_________________________")
        self.write_message("echo : " + message)

    def on_close(self):
        print("on close")

    def on_connection_close(self):
        print("connection close")

    def on_ping(self, data):
        print("ping : " + str(data))

    def on_pong(self, data):
        print("pong : " + str(data))
        print(datetime.now())
        self.ping()
