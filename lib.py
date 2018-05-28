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

class SSApplication(tornado.web.Application):

    def RegisterBlueprint(self, blueprint):
        '''
        :param blueprint: bp.Blueprint
        :return:
        '''
        self.default_router.add_rules(blueprint.GetSubRouters())