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

import tornado.web

def makeResponse(msg=''):
    return {'code': -1, 'msg': msg, 'success': False, 'data': None}

class SSApplication(tornado.web.Application):

    def RegisterBlueprint(self, blueprint):
        '''
        :param blueprint: bp.Blueprint
        :return:
        '''
        self.default_router.add_rules(blueprint.GetSubRouters())

class SSWebRequestHandler(tornado.web.RequestHandler):
    version = 1.0
    response = makeResponse()

    def changeResponse2Success(self, data=None):
        '''
        将数据响应改为成功状态
        :param data:
        :return:
        '''
        self.response['code'] = 0
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


    def get_current_user(self):
        return self.get_secure_cookie('id')