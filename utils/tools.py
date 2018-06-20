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
try:
    from yaml import CLoader as Loader
except:
    from yaml import Loader

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