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
from ssmain.messager.msg_factory import MakeMessagerInterface
from config import MESSAGER_LIVE_PROXY

class TextserviceRequestHandler(UserinterfaceWebRequestHandler):
    def get(self, *args, **kwargs):
        """
        @param GET eid 企业编号 hashids
        @param GET pid 产品编号 hashids
        @param GET uid 用户编号 hashids
        """
        eid, pid, uid = self.getArgument_list("eid", "pid", "uid")
        if all((eid, pid)):
            chat_proxy = MakeMessagerInterface(MESSAGER_LIVE_PROXY)

            return self.render("text_service.html",
                           visitor=chat_proxy.GetTempAccount(),
                           msg_proxy=MESSAGER_LIVE_PROXY)
        else:
            raise Exception("params invalid")