# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     mimc_api
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
from lib import SSWebDataRequestHandler
from utils.wraps import jsonp
from utils.tools import existsNone
from im.mimc_rel_config import getMimcApiUrl
from im import mimcRequest

class FetchMIMCToken(SSWebDataRequestHandler):
    @jsonp
    def get(self):
        account = self.get_argument('account', None)
        url = getMimcApiUrl('api/account/token')
        req_data = {'appId': self.yaml.appId, 'appKey': self.yaml.appKey,
                    'appSecret': self.yaml.appSecret, 'appAccount': account}
        req_response = requests.post(url, None, json=req_data, headers={'Content-Type': 'application/json'})
        if req_response.ok:
            return req_response.text.encode('utf-8')
        else:
            return self.jsonResponse()


class ProxyPushP2PMessage(SSWebDataRequestHandler):
    @jsonp
    def get(self):
        '''
        通过服务器接口发送P2P消息
        :return:
        '''
        fromAccount, toAccount, msg = self.getArgument_list('from', 'to', 'msg')
        if not existsNone(fromAccount, toAccount, msg):
            url = getMimcApiUrl('api/push/p2p')
            req_data = {
                'appId': self.yaml.appId,
                'appKey': self.yaml.appKey,
                'appSecret': self.yaml.appSecret,
                'fromAccount': fromAccount,
                'toAccount': toAccount,
                'msg': msg,
                'msgType': '',
                'fromResource': ''
            }
            code, result = mimcRequest(url, req_data)
            if 200 == code:
                self.changeResponse2Success({'packetId': result})
            else:
                self.setResponseMsg(result)
        return self.jsonResponse()

