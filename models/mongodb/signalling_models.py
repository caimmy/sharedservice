# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： signalling_models
Description:
Author: caimmy
date： 2018/9/6
-------------------------------------------------
Change Activity:
2018/9/6
-------------------------------------------------
"""
__author__ = 'caimmy'

import time
from models.mongodb import _MongoData


class RuntimeLogs(_MongoData):
    """
    运行时日志
    """
    logType             = None
    timestamp           = None
    timelabel           = None
    content             = None

    def __init__(self, logtype, logcontent):
        self.logType    = logtype
        self.content    = logcontent
        self.timestamp  = time.time()
        self.timelabel  = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

class MIMCStatusChangeLog(_MongoData):
    """
    MIMC 状态改变事件日志
    @param account: mimc账号
    @param mimc 状态改变事件参数 bindResult, errType, errReason, errDesc
    """
    account             = None
    bindResult          = None
    errType             = None
    errReason           = None
    errDesc             = None

    def __init__(self, account, bindResult, errType="", errReason="", errDesc=""):
        self.account        = account
        self.bindResult     = bindResult
        self.errType        = errType
        self.errReason      = errReason
        self.errDesc        = errDesc
