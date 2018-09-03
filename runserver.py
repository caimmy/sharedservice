# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     runserver
   Description:
   Author:        caimmy
   date：          2018/5/28
-------------------------------------------------
   Change Activity:
                   2018/5/28
-------------------------------------------------
"""
__author__ = 'caimmy'

import os
import platform
import logging
from logging import handlers
import tornado.log

from lib import SSApplication
import im.service
import exam.service
import admin.service
import customer.service
import userinterface.service
import papi.service

from admin.uimodules import admin_ui
from tornado_ui import ui_methods

from config import DEBUG_MODE

APP_SETTINGS = {
    "debug": DEBUG_MODE,
    "cookie_secret": 'caimmy_9527',
    "xsrf_cookies": True,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "ui_modules": admin_ui,
    "ui_methods": ui_methods,
    #"websocket_ping_interval": 3,
    #"websocket_ping_timeout": 30
}

class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write("<h1>hello, world.</h1>")


def MakeApplication():
    '''
    :return: tornado.web.Application
    '''
    prehander_urls = mergeBlueprintUrls(im.service.CreateBlueprint(),
                                        exam.service.CreateBlueprint(),
                                        admin.service.CreateBlueprint(),
                                        customer.service.CreateBlueprint(),
                                        userinterface.service.CreateBlueprint(),
                                        papi.service.CreateBlueprint())
    app = SSApplication([], **APP_SETTINGS)
    app.default_router.add_rules(prehander_urls)
    app.default_router.add_rules([(r"/?", DemoHandler)])
    return app

def mergeBlueprintUrls(*args):
    url_lists = []
    for service in args:
        url_lists.extend(service.GetSubRouters())
    return url_lists

def init_logger():
    fmt = tornado.log.LogFormatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.WARNING)
    # TimeRotatingFile
    th = handlers.TimedRotatingFileHandler('logs/app.log', when='h' if DEBUG_MODE else 'd', interval=1, backupCount= 5 if DEBUG_MODE else 1024, encoding="utf-8")
    th.setFormatter(fmt)
    # Console
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)

    logger.addHandler(sh)
    logger.addHandler(th)

    tornado.log.enable_pretty_logging(logger=tornado.log.gen_log)

if "__main__" == __name__:
    init_logger()
    application = MakeApplication()

    if ("Linux" == platform.system()):
        web_server = tornado.httpserver.HTTPServer(application)
        web_server.bind(8888)
        web_server.start(1 if DEBUG_MODE else 0)
    else:
        application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
