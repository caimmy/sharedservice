# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： status_models
Description: 业务状态相关的模型
Author: caimmy
date： 2018/9/4
-------------------------------------------------
Change Activity:
2018/9/4
-------------------------------------------------
"""
__author__ = 'caimmy'

import json

class _MongoData():
    def extraData(self):
        """
        抽取mongodb的数据实例
        """
        mongo_data = {}
        for v in vars(self).items():
            if v[1] != None:
                mongo_data.setdefault(v[0], v[1])
        return mongo_data

    def fillData(self, data):
        """
        填充mongodb的数据实例
        """
        for _k in data:
            if hasattr(self, _k):
                setattr(self, _k, data[_k])

class CustomerOnLineData(_MongoData):
    user_id         = None         # 客服编号
    hashid          = None         # 客服hash编号
    online_time     = None         # 客服上线时间
    beat_time       = None         # 上次心跳检测时间
    workload        = None         # 客服工作负载
    service_prod    = None         # 客服服务的产品编号
    active          = None         # 是否处于活跃状态，可以接受服务分配

    def __init__(self, user_id, hashid):
        self.user_id = user_id
        self.hashid = hashid

    def __repr__(self):
        return json.dumps(self.extraData())