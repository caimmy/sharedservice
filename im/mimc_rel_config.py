# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     mimc_rel_config
   Description:    mimc 相关的地址、配置、设置信息
   Author:         caimmy
   date：          2018/6/20
-------------------------------------------------
   Change Activity:
                   2018/6/20
-------------------------------------------------
"""
__author__ = 'caimmy'

mimc_api_url = 'https://mimc.chat.xiaomi.net/'

def getMimcApiUrl(api):
    '''
    获取具体的mimc api地址
    :param api:
    :return:
    '''
    return mimc_api_url + (api[1:] if api.startswith('/') else api)