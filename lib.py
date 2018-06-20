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
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.tools import LoadYAML2Object
from models.yaml import MimcConfig

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

    def prepare(self):
        self.response = makeResponse()

    def get_current_user(self):
        return self.get_secure_cookie('id')

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
            ret_arguments.append(self.get_argument(a, None))
        return ret_arguments


class SSWebDataRequestHandler(SSWebRequestHandler):

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
        self.response['code'] = 0
        self.response['success'] = True
        self.response['msg'] = 'success'
        self.data = data

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