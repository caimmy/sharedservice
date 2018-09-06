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
from ssmain.workbench.linestatus import CustomerStatus
from utils.ids import unhash_ids

class KeepliveWsHandler(SSWebRequestHandler):
    def open(self, *args, **kwargs):
        CustomerStatus.CustomerOnlineStatus(self.db).setCustomerOnline(self.user)

    def on_message(self, message):
        # 更新心跳时间戳
        user_id = unhash_ids(self.user["hashid"])
        CustomerStatus.CustomerOnlineStatus(self.db).beatCustomerOnline(user_id)

    def on_close(self):
        print("on close")
        user_id = unhash_ids(self.user["hashid"])
        CustomerStatus.CustomerOnlineStatus(self.db).removeCustomerOnline(user_id)

    def on_connection_close(self):
        print("connection close")
        user_id = unhash_ids(self.user["hashid"])
        CustomerStatus.CustomerOnlineStatus(self.db).removeCustomerOnline(user_id)

    def on_ping(self, data):
        print("ping : " + str(data))

    def on_pong(self, data):
        print("pong : " + str(data))
        print(datetime.now())
        self.ping()
