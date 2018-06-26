# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     test
   Description:
   Author:         caimmy
   date：          2018/6/16
-------------------------------------------------
   Change Activity:
                   2018/6/16
-------------------------------------------------
"""
__author__ = 'caimmy'

import requests
from utils.tools import LoadYAML2Object
import yaml

from tornado.web import url
from tornado.web import RequestHandler

class T(RequestHandler):
    def get(self):
        return self.write("sadfasdf")

def sendP2PMsg(fromAccount, toAccount, content):
    url = 'https://mimc.chat.xiaomi.net/api/push/p2p/'
    data = {
        'appId': '2882303761517785685',
        'appKey': '5541778587685',
        'appSecret': 'MAa+9Zn+hznwXS8Eto2Hog==',
        'fromAccount': fromAccount,
        'fromResource': 'mi5',
        'toAccount': toAccount,
        'msg': content,
        'msgType': ''
        }
    req = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    print(req.text)

class MimcConfig():
    yaml_tag = 'mimc'
    def __init__(self):
        self.appId = ''
        self.appKey = ''
        self.appSecret = ''

    def __repr__(self):
        return "%s - %s - %s - %s" % (self.yaml_tag, self.appId, self.appKey, self.appSecret)

class MysqlCfg():
    yaml_tag = ''
    host = ''
    port = 0
    db = ''
    user = ''
    pwd = ''

def test(*args):
    for a in args:
        print(a)

if "__main__" == __name__:
    m = url(r"/t/?", T, name="asdfasdf")
    print(m)