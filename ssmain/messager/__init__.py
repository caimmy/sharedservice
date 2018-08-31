# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： __init__.py
Description: 消息抽象层，隔离MIMC及其他可能的消息中间件
Author: caimmy
date： 2018/8/31
-------------------------------------------------
Change Activity:
2018/8/31
-------------------------------------------------
"""
__author__ = 'caimmy'

class MessagerAbstract:
    def __init__(self):
        self.__version__ = "0.1"

    def GetAccount(self, account):
        """
        获取永久账号的封装信息
        @param account string
        @return string
        """
        raise NotImplementedError("need to be implement")

    def GetTempAccount(self):
        """
        获取临时账号
        @return string
        """
        raise NotImplementedError("need to be implement")