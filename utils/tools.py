# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     tools
   Description:
   Author:         caimmy
   date：          2018/6/20
-------------------------------------------------
   Change Activity:
                   2018/6/20
-------------------------------------------------
"""
__author__ = 'caimmy'

import codecs
import yaml
import random
try:
    from yaml import CLoader as Loader
except:
    from yaml import Loader

SALT_SEED = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
             'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
             'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '@', '#', '$',
             '%', '&', '*']

def LoadYAML(yamlfile):
    with codecs.open(yamlfile, 'r', 'utf-8') as yf:
        return yaml.load(yf, Loader=Loader)

def LoadYAML2Object(yamlfile, obj):
    '''
    从yaml加载python对象
    :param yamlfile: 配置文件的路径
    :param tag: 需要加载的配置项标签
    :param obj: 承载配置文件项的对象
    :return:
    '''
    yaml_config = LoadYAML(yamlfile)
    if (obj.yaml_tag in yaml_config):
        yaml_node = yaml_config.get(obj.yaml_tag)
        for _k in yaml_node:
            if hasattr(obj, _k):
                setattr(obj, _k, yaml_node.get(_k))
    return obj

def existsNone(*args):
    '''
    检查参数（list）中是否存在空值
    :param alist: list
    :return: bool
    '''
    ret_chk = False
    for item in args:
        if item is None:
            ret_chk = True
        elif isinstance(item, str) and item == '':
            ret_chk = True
        elif isinstance(item, bytes) and item == b'':
            ret_chk = True
        if ret_chk:
            break

    return ret_chk

def genSalt(length=6):
    """
    生成密码盐
    @return string
    """
    _s = []
    salt_size = len(SALT_SEED) - 1
    for i in range(length):
        _s.append(random.randint(0, salt_size))

    return "".join(_s)

def ensureBytes(s):
    """
    @return bytes
    """
    return s.encode("utf-8") if not isinstance(s, bytes) else s

def ensureString(b):
    """
    """
    return b.decode("utf-8") if not isinstance(b, str) else b
