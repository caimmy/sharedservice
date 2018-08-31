# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： customer_service
Description:
Author: caimmy
date： 2018/8/30
-------------------------------------------------
Change Activity:
2018/8/30
-------------------------------------------------
"""
__author__ = 'caimmy'

from customer import CustomerWebRequestHandler
from ssmain.messager.msg_factory import MakeMessagerInterface
from config import MESSAGER_LIVE_PROXY


class TxtliveServiceIndex(CustomerWebRequestHandler):
    def get(self, *args, **kwargs):
        messager_live = MakeMessagerInterface(MESSAGER_LIVE_PROXY)
        live_account = messager_live.GetAccount(self.user.get("hashid"))
        return self.render("service/txtlive_service.html",
                           live_account=live_account,
                           msg_proxy=MESSAGER_LIVE_PROXY)