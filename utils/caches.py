# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     caches
   Description:
   Author:         caimmy
   date：          2018/8/7
-------------------------------------------------
   Change Activity:
                   2018/8/7
-------------------------------------------------
"""
__author__ = 'caimmy'

import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

class RedisSession:
    def __init__(self):
        self.conn = redis.StrictRedis(REDIS_HOST, REDIS_PORT, REDIS_DB)

    def getItem(self, key):
        return self.conn.get(key)

    def setItem(self, key, data, duration):
        self.conn.set(key, data)
        self.conn.expire(key, duration)

    def delItem(self, key):
        self.conn.delete(key)
