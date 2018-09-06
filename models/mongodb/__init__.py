# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： __init__.py
Description:
Author: caimmy
date： 2018/9/3
-------------------------------------------------
Change Activity:
2018/9/3
-------------------------------------------------
"""
__author__ = 'caimmy'

MONGO_DB_NAME = "ss"

COLLECTION_CUSTOMER_ONLINE  = "online_customers"
COLLECTION_LOGS             = "runtime_log_"

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

    def __repr__(self):
        return json.dumps(self.extraData())
