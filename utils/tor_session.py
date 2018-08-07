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
from hashlib import sha1
from utils.caches import RedisSession

create_sess_id = lambda: sha1(bytes("%s%s" % (os.urandom(16), time.time()), encoding="utf-8")).hexdigest()

class SessionData(dict):
    def __init__(self, sessid):
        self.sessid = sessid

    def __getitem__(self, item):
        return self.get(item) if item in self else None

    def __setitem__(self, key, value):
        self[key] = value


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
            session_data = SessionData(sess_id)
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