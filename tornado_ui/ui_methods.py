# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     ui_mehtods
   Description:
   Author:         caimmy
   date：          2018/8/7
-------------------------------------------------
   Change Activity:
                   2018/8/7
-------------------------------------------------
"""
__author__ = 'caimmy'

def flash(self, message, category="error"):
    """
    设置消息闪现的消息缓存
    :param self:
    :param message:
    :param category:
    :return:
    """
    self.session.set("_flashes", {'category': category, "message": message})

def get_flashed_messages(self):
    """
    提取缓存的消息闪现内容
    :param self:
    :return:
    """
    flashes = self.session.get("_flashes", None)
    if flashes:
        self.session.delete("_flashes")
        return [flashes]
    else:
        return []

def get_login_identify(self, prop):
    """
    获取当前登录用户的信息
    :param prop:
    :return:
    """
    cur_user = self.session.get("user")
    return cur_user[prop] if cur_user and prop in cur_user else ''

def full_url(self, url_name, parameters):
    """
    构造完整的url
    """
    url = self.reverse_url(url_name)
    _p = ""
    if str(url).rfind("?") < 0:
        url = url + "?"
    if isinstance(parameters, dict):
        _p = "&".join([t+"="+str(parameters[t]) for t in parameters])
    elif isinstance(parameters, str):
        _p = parameters[1:] if parameters.startswith("?") else parameters
    return url + _p

