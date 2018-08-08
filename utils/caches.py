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
    def __init__(self, sessid):
        self.conn = redis.StrictRedis(REDIS_HOST, REDIS_PORT, REDIS_DB)
        self.sessid = sessid

    def getItem(self, key):
        return self.conn.hget(self.sessid, key)

    def setItem(self, key, data, duration=3600):
        self.conn.hset(self.sessid, key, data)
        self.conn.expire(self.sessid, duration)

    def delItem(self, item):
        self.conn.hdel(self.sessid, item)

    def clear(self):
        self.conn.delete(self.sessid)
