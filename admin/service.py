# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     service
   Description:
   Author:         caimmy
   date：          2018/6/14
-------------------------------------------------
   Change Activity:
                   2018/6/14
-------------------------------------------------
"""
__author__ = 'caimmy'


import bp

from admin.authentication import LoginRequestHandler, RegisterRequestHandler, IndexRequestHandler

def CreateBlueprint():
    return bp.Blueprint(r'admin', [
        (r'/?', IndexRequestHandler),
        (r'/register/?', RegisterRequestHandler),
        (r'/login/?', LoginRequestHandler)
    ])