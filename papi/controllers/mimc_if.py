# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： mimc
Description:
Author: caimmy
date： 2018/8/31
-------------------------------------------------
Change Activity:
2018/8/31
-------------------------------------------------
"""
__author__ = 'caimmy'

import requests
from tornado.log import gen_log
from papi import PrivateApiRequestHandler
from papi import mimc_services_urls
from models.mongodb.signalling_models import MIMCStatusChangeLog, RuntimeLogs
from config import MIMC_APP_ID, MIMC_APP_KEY, MIMC_APP_SECRET
from const_defines import RUNTIME_LOG_MIMC_STATUS_CHANGE

class MimcTokenRefresh(PrivateApiRequestHandler):
    """
    代理获取消息云服务的授权token
    """
    def get(self, *args, **kwargs):
        account, = self.getArgument_list("account")
        if account:
            req = requests.post(mimc_services_urls.MIMC_FETCH_TOKEN, None, json=
            {"appId": MIMC_APP_ID, "appKey": MIMC_APP_KEY, "appSecret": MIMC_APP_SECRET, "appAccount": account})
            if req.ok:
                self.changeResponse2Success(req.text)
            else:
                self.setResponseMsg(req.text)
                gen_log.error(req.content)
        else:
            self.setResponseMsg("parameter invalid")
        return self.write(self.jsonResponse())

class MimcStatusChange(PrivateApiRequestHandler):
    """
    消息云状态变化日志
    """
    def get(self, *args, **kwargs):
        account, br, et, er, ed = self.getArgument_list("account", "br", "et", "er", "ed")
        if (all((account, br))):
            data_mimc_status_change = MIMCStatusChangeLog(account, br, et, er, ed)
            data_log                = RuntimeLogs(RUNTIME_LOG_MIMC_STATUS_CHANGE, data_mimc_status_change.extraData())
            self.runtime_logger_mongo.insert(data_log.extraData())
            self.changeResponse2Success()
        else:
            gen_log.error("params invalid")
        return self.write(self.jsonResponse())