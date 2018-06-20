# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     __init__.py
   Description:
   Author:         caimmy
   date：          2018/6/14
-------------------------------------------------
   Change Activity:
                   2018/6/14
-------------------------------------------------
"""
__author__ = 'caimmy'

def ensureBytes(s):
    '''
    确保字符串以bytes形式返回
    :param s:
    :return: bytes
    '''
    if isinstance(s, bytes):
        return s
    elif isinstance(s, str):
        return s.encode()


def ensureString(b):
    '''
    确保字符串以string形式返回
    :param b:
    :return: str
    '''
    if isinstance(b, str):
        return b
    elif isinstance(b, bytes):
        return b.decode()