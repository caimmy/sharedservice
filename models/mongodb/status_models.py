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

from models.mongodb import _MongoData

class StaffOnLineData(_MongoData):
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
