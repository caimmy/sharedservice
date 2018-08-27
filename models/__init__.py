# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     __init__.py
   Description:
   Author:         caimmy
   date：          2018/6/15
-------------------------------------------------
   Change Activity:
                   2018/6/15
-------------------------------------------------
"""
__author__ = 'caimmy'

import hashlib
from utils.tools import ensureBytes, genSalt

'''
模型枚举值，有效、无效、已删除
'''
ENUM_VALID        = '1'
ENUM_INVALID      = '0'
ENUM_DELETE       = '2'

'''
性别
'''
ENUM_GENDER_MALE    = '1'
ENUM_GENDER_FEMALE  = '0'

'''
创建用户的三种途径
'''
USER_CREATE_METHOD_AUTO         = "auto"
USER_CREATE_METHOD_ENTERPRISE   = "enterprise"
USER_CREATE_METHOD_SYSTEM       = "system"


class PasswordBase:
    @staticmethod
    def sigPassword(salt, pwd):
        """
        用salt和pwd生成最终存表密码
        @return string
        """
        return hashlib.sha1(ensureBytes(salt + pwd)).hexdigest()

    def genPassword(self, password, salt=""):
        """
        对原始密码进行加盐计算，并生成sha1摘要作为存放的最终密码
        """
        salt = genSalt(6) if "" == salt else salt
        sig_pass = PasswordBase.sigPassword(salt, password)
        return salt, sig_pass

    def checkPassword(self, password):
        """
        校验密码是否正确
        """
        return PasswordBase.sigPassword(self.salt, password) == self.passwd