# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     __init__.py
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
import requests
import tornado.log

def mimcRequest(url, data):
    '''
    向mimc接口提交数据请求
    :param url:
    :param data:
    :return:
    '''
    ret_code, result = 0, ''
    response_json = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    if response_json.ok:
        resp_obj = json.loads(response_json.text)
        ret_code = resp_obj.get("code", 0)
        if 200 == ret_code:
            result = resp_obj.get("data").get("packetId")
        else:
            tornado.log.gen_log.error(resp_obj.get("message", ""))
    return ret_code, result