# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： CustomerStatus
Description: 客服在线状态管理
Author: caimmy
date： 2018/9/4
-------------------------------------------------
Change Activity:
2018/9/4
-------------------------------------------------
"""
__author__ = 'caimmy'

import time
import pymongo
from tornado.log import gen_log
from utils.wraps import singleton
from models.mongodb.status_models import CustomerOnLineData
from models.mysql.enterprise_tbls import CustomerEnterpriseRel
from models.mongodb import MONGO_DB_NAME, COLLECTION_CUSTOMER_ONLINE
from config import MONGODB_HOST, MONGODB_PORT
from const_defines import SIDE_ROLE_CUSTOMER

@singleton
class CustomerOnlineStatus():
    def __init__(self, mysqldb):
        self.db = mysqldb
        self.mongodb = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)[MONGO_DB_NAME]

    def __del__(self):
        self.mongodb.close()
        self.mongodb = None

    def getCustomerOnline(self, user_id):
        return self.mongodb[COLLECTION_CUSTOMER_ONLINE].find_one(CustomerOnLineData(user_id, None).extraData())

    def setCustomerOnline(self, user_info):
        """
        设置客服上线
        """
        if "side" in user_info and user_info["side"] == SIDE_ROLE_CUSTOMER:
            if not self.getCustomerOnline(user_info["id"]):
                # 提取客服和服务产品之间的关系，为建立客服服务路由做准备
                customer_enterprise_query = self.db.query(CustomerEnterpriseRel).filter(CustomerEnterpriseRel.cm_id==user_info["id"]).all()
                customer_bind_products = [rel.product_id for rel in customer_enterprise_query]
                c_online_data = CustomerOnLineData(user_info["id"], user_info["hashid"])
                c_online_data.workload = 0
                c_online_data.online_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                c_online_data.beat_time = time.time()
                c_online_data.service_prod = customer_bind_products
                c_online_data.active = 1
                customer_online_collection = self.mongodb[COLLECTION_CUSTOMER_ONLINE]
                res = customer_online_collection.insert(c_online_data.extraData())
                print(res)
            else:
                self.beatCustomerOnline(user_info["id"])
            gen_log.debug(self.getCustomerOnline(user_info["id"]))

    def beatCustomerOnline(self, user_id):
        """
        延长客服在线的心跳时间戳
        """
        res = self.mongodb[COLLECTION_CUSTOMER_ONLINE].update({"user_id": user_id}, {"$set": {"beat_time": time.time()}})
        if 0 == res["nModified"]:
            gen_log.error("beatCustomerOnline", str(res))



