# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： MIMCMessager
Description:
Author: caimmy
date： 2018/8/31
-------------------------------------------------
Change Activity:
2018/8/31
-------------------------------------------------
"""
__author__ = 'caimmy'

from uuid import uuid1
from ssmain.messager import MessagerAbstract
from config import APPNAME

class MIMCMessager(MessagerAbstract):
    def GetAccount(self, account):
        return APPNAME + ":" + account

    def GetTempAccount(self):
        return APPNAME + ":" + str(uuid1())