# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     lib
   Description:
   Author:         caimmy
   date：          2018/5/28
-------------------------------------------------
   Change Activity:
                   2018/5/28
-------------------------------------------------
"""
__author__ = 'caimmy'

import json
import tornado.web
import SSExceptions
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.tools import LoadYAML2Object
from models.yaml import MimcConfig
from utils.tor_session import SessionData

from models.mysql.db import engine

def makeResponse(msg=''):
    return {'code': -1, 'msg': msg, 'success': False, 'data': None}

class SSApplication(tornado.web.Application):

    def __init__(self, handlers, **settings):
        super(SSApplication, self).__init__(handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=True, expire_on_commit=False))
        self.yaml = LoadYAML2Object('./config.yaml', MimcConfig())

    def RegisterBlueprint(self, blueprint):
        '''
        :param blueprint: bp.Blueprint
        :return:
        '''
        self.default_router.add_rules(blueprint.GetSubRouters())

class SSWebRequestHandler(tornado.web.RequestHandler):
    version = 1.0

    def __init__(self, application, request, **kwargs):
        super(SSWebRequestHandler, self).__init__(application, request, **kwargs)
        self.user_info = None

    @property
    def user(self):
        if self.user_info:
            return self.user_info
        else:
            ui = self.get_secure_cookie("user")
            if ui:
                self.user_info = json.loads(ui)
                return self.user_info
            else:
                raise SSExceptions.NotLoginException()

    def prepare(self):
        self.response = makeResponse()
        self.session = SessionData(self)

    def get_current_user(self):
        loginned_user = self.get_secure_cookie("user")
        if loginned_user is not None:
            return json.loads(loginned_user)
        else:
            return None

    def Login(self, user):
        '''
        用户登录
        :param user: dict
        :return:
        '''
        self.set_secure_cookie("user", json.dumps(user))
        self.session.set("user", user)

    def Loginout(self):
        '''
        注销用户会话
        :return:
        '''
        self.clear_cookie("user")
        self.clear_cookie("sess_id")
        self.session.clear()

    @property
    def db(self):
        return self.application.db

    @property
    def yaml(self):
        '''
        :return: im.MimcConfig
        '''
        return self.application.yaml

    def getArgument_list(self, *args):
        ret_arguments = []
        for a in args:
            ret_arguments.append(self.get_arguments(a) if a.endswith("[]") else self.get_argument(a, None))
        return ret_arguments


class SSWebDataRequestHandler(SSWebRequestHandler):

    def __init__(self, application, request, **kwargs):
        super(SSWebDataRequestHandler, self).__init__(application, request, **kwargs)
        self.response = {"code": -1, "success": False, "msg": "gen err"}

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST,GET')

    def changeResponse2Success(self, data=None):
        '''
        将数据响应改为成功状态
        :param data:
        :return:
        '''
        self.response["code"]       = 0
        self.response["success"]    = True
        self.response["msg"]        = "ok"
        self.response["data"]       = data

    def setResponseMsg(self, msg, code=-1):
        '''
        设置数据响应的文本信息
        :param msg:
        :return:
        '''
        self.response['code'] = code
        self.response['msg'] = msg

    def jsonResponse(self):
        '''
        已json格式输出响应
        :return:
        '''
        return json.dumps(self.response)