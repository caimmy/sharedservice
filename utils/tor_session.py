# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     tor_session
   Description:
   Author:         caimmy
   date：          2018/8/7
-------------------------------------------------
   Change Activity:
                   2018/8/7
-------------------------------------------------
"""
__author__ = 'caimmy'

import os, time
import functools
import pickle
from hashlib import sha1
from utils.caches import RedisSession

create_sess_id = lambda: sha1(bytes("%s%s" % (os.urandom(16), time.time()), encoding="utf-8")).hexdigest()

class SessionData:
    def __init__(self, request_handler):
        sessid = request_handler.get_secure_cookie("sess_id", None)
        if not sessid:
            sessid = create_sess_id()
        self.sessid = sessid
        self.cache = RedisSession(self.sessid)
        self.info = {}
        request_handler.set_secure_cookie("sess_id", sessid, 1, 1)

    def get(self, item, defaults=None):
        if item in self.info:
            value = self.info[item]
        else:
            value = self.cache.getItem(item)
            if value:
                self.info[item] = value
        return defaults if not value else pickle.loads(value)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.set(key, value)

    def set(self, key, value):
        cache_value = pickle.dumps(value)
        self.cache.setItem(key, cache_value)
        self.info[key] = cache_value

    def delete(self, key):
        if key in self.info:
            del(self.info[key])
        self.cache.delItem(key)

    def clear(self):
        self.cache.clear()
        self.info.clear()


def sessoin(method):
    """
    装饰web请求对象，在进入请求处理前提取准备session数据，离开请求处理前保存session数据
    :param method:
    :return:
    """
    @functools.wraps(method)
    def wrap_session_opers(self, *args, **kwargs):
        cache = RedisSession()
        sess_id = self.get_secure_cookie("sess_id", None)
        if not sess_id:
            sess_id = create_sess_id()
            self.set_secure_cookie("sess_id", sess_id, 1)
        session_data = cache.getItem(sess_id)
        if not session_data:
            session_data = SessionData(self)
        setattr(self, "session", session_data)
        data = method(self, *args, **kwargs)
        self.write(data)
        save_session = getattr(self, "session", None)
        if save_session:
            cache.setItem(sess_id, save_session, 7200)
        else:
            # 清理session数据
            cache.delItem(sess_id)

    return wrap_session_opers