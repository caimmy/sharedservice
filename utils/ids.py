# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： ids
Description:
Author: caimmy
date： 2018/8/13
-------------------------------------------------
Change Activity:
2018/8/13
-------------------------------------------------
"""
__author__ = 'caimmy'

from uuid import uuid1

def generateUUID():
    return str(uuid1())