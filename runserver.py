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

import platform
import logging
from logging import handlers
import tornado.log

from lib import SSApplication
import im.service
import exam.service
import admin.service

from config import DEBUG_MODE

APP_SETTINGS = {
    "debug": True,
    "cookie_secret": 'caimmy_9527',
    "login_url": 'admin/login',
    "xsrf_cookies": False
}

class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write("<h1>hello, world.</h1>")


def MakeApplication():
    '''
    :return: tornado.web.Application
    '''
    app = SSApplication([], **APP_SETTINGS)
    app.RegisterBlueprint(im.service.CreateBlueprint())
    app.RegisterBlueprint(exam.service.CreateBlueprint())
    app.RegisterBlueprint(admin.service.CreateBlueprint())
    app.default_router.add_rules([(r"/?", DemoHandler)])
    return app

def init_logger():
    fmt = tornado.log.LogFormatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.WARNING)
    # TimeRotatingFile
    th = handlers.TimedRotatingFileHandler('logs/app.log', interval=1, backupCount=5, encoding="utf-8")
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
