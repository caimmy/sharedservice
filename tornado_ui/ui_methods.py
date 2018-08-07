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
    flashes = self.session.get("_flashes", [])
    flashes.append((category, message))
    self.session.set("_flashes", flashes)

def get_flashed_messages(self):
    """
    提取缓存的消息闪现内容
    :param self:
    :return:
    """
    flashes = self.session.get("_flashes", [])
    self.clear_cookie("_flashes")
    return flashes