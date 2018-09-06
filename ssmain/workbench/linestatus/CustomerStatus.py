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
from models.mongodb.status_models import StaffOnLineData
from models.mysql.enterprise_tbls import StaffEnterpriseRel
from models.mongodb import MONGO_DB_NAME, COLLECTION_CUSTOMER_ONLINE
from utils.ids import unhash_ids
from config import MONGODB_HOST, MONGODB_PORT
from const_defines import SIDE_ROLE_STAFF

@singleton
class CustomerOnlineStatus():
    def __init__(self, mysqldb):
        self.db = mysqldb
        self.mongodb = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)[MONGO_DB_NAME]

    def __del__(self):
        self.mongodb.close()
        self.mongodb = None

    def getCustomerOnline(self, user_id):
        return self.mongodb[COLLECTION_CUSTOMER_ONLINE].find_one(StaffOnLineData(user_id, None).extraData())

    def setCustomerOnline(self, user_info):
        """
        设置客服上线
        @param user_info 会话记录的用户信息
        """
        if "side" in user_info and user_info["side"] == SIDE_ROLE_STAFF:
            user_id = unhash_ids(user_info["hashid"])
            if not self.getCustomerOnline(user_id):
                # 提取客服和服务产品之间的关系，为建立客服服务路由做准备
                customer_enterprise_query = self.db.query(StaffEnterpriseRel).filter(StaffEnterpriseRel.cm_id == user_id).all()
                customer_bind_products = [rel.product_id for rel in customer_enterprise_query]
                c_online_data = StaffOnLineData(user_id, user_info["hashid"])
                c_online_data.workload = 0
                c_online_data.online_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                c_online_data.beat_time = time.time()
                c_online_data.service_prod = customer_bind_products
                c_online_data.active = 1
                customer_online_collection = self.mongodb[COLLECTION_CUSTOMER_ONLINE]
                res = customer_online_collection.insert(c_online_data.extraData())
                print(res)
            else:
                self.beatCustomerOnline(user_id)
            gen_log.debug(self.getCustomerOnline(user_id))

    def beatCustomerOnline(self, user_id):
        """
        延长客服在线的心跳时间戳
        @param user_id 用户编号
        """
        res = self.mongodb[COLLECTION_CUSTOMER_ONLINE].update({"user_id": user_id}, {"$set": {"beat_time": time.time()}})
        if 0 == res["nModified"]:
            gen_log.error("beatCustomerOnline", str(res))

    def removeCustomerOnline(self, user_id):
        """
        删除客服在线记录
        @param user_id 用户编号
        """
        delres = self.mongodb[COLLECTION_CUSTOMER_ONLINE].find_one_and_delete({"user_id": user_id})
        if not delres:
            gen_log.error("remove online customer failure: user_id %d" % user_id)

