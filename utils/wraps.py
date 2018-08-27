# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     wraps
   Description:
   Author:         caimmy
   date：          2018/6/14
-------------------------------------------------
   Change Activity:
                   2018/6/14
-------------------------------------------------
"""
__author__ = 'caimmy'
import json
import functools
from lib import makeResponse
from utils import ensureBytes, ensureString

def request_authenticate(method):
    '''
    数据请求方式中判断用户是否登录
    :param method:
    :return:
    '''
    @functools.wraps(method)
    def check_authentication(self, *args, **kwargs):
        if self.current_user:
            user_info = self.session.get("user")
            if user_info and user_info["side"] == "enterprise":
                return method(self, *args, **kwargs)
        self.write(json.dumps(makeResponse('login first please')))
    return check_authentication

def web_authenticate(method):
    '''
    web请求方式中判定用户是否登录，如未登陆则自动跳转默认登录地址
    :param method:
    :return:
    '''
    @functools.wraps(method)
    def check_authentication(self, *args, **kwargs):
        if self.current_user:
            user_info = self.session.get("user")
            if user_info and user_info["side"] == "enterprise":
                return method(self, *args, **kwargs)
        return self.redirect(self.reverse_url('login'))
    return check_authentication

def web_customer_login(method):
    """
    客服使用服务侧业务时，判断账号是否登陆，如果是限制登陆的页面，需要强制用户进行登录
    """
    @functools.wraps(method)
    def check_authentication(self, *args, **kwargs):
        if self.current_user:
            user_info = self.session.get("user")
            if user_info and user_info["side"] == "customer":
                return method(self, *args, **kwargs)
        return self.redirect(self.reverse_url('customer_frontpage_login'))

    return check_authentication

def jsonp(method):
    '''
    jsonp输出
    :param method:
    :return:
    '''
    @functools.wraps(method)
    def jsonp_func(self, *args, **kwargs):
        requestHandler = self
        callback = requestHandler.get_argument('callback', False)
        data = method(self, *args, **kwargs)
        content = str(callback) + '(' + ensureString(data) + ')' if callback else data
        requestHandler.write(ensureBytes(content))
        requestHandler.finish()
    return jsonp_func