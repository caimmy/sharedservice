# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： msg_factory
Description: 消息中间件的工厂类，生成对应的消息中间件工具
Author: caimmy
date： 2018/8/31
-------------------------------------------------
Change Activity:
2018/8/31
-------------------------------------------------
"""
__author__ = 'caimmy'

from ssmain.messager.MIMC import MIMCMessager
from config import MESSAGER_LIVE_PROXY

def MakeMessagerInterface(via=MESSAGER_LIVE_PROXY):
    if MESSAGER_LIVE_PROXY == via:
        return MIMCMessager()
    else:
        raise RuntimeError("{t} not support in messager interfaces".format(t=via))