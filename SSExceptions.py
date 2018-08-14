# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： Exceptions
Description:
Author: caimmy
date： 2018/8/13
-------------------------------------------------
Change Activity:
2018/8/13
-------------------------------------------------
"""
__author__ = 'caimmy'


class NotLoginException(Exception):
    def __repr__(self):
        return "current user not login"