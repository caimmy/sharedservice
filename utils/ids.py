# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： ids
Description:
Author: caimmy
date： 2018/8/13
-------------------------------------------------
Change Activity:
2018/8/13
-------------------------------------------------
"""
__author__ = 'caimmy'

from uuid import uuid1
from hashids import Hashids

from const_defines import HASHIDS_SALT

def generateUUID():
    return str(uuid1())

def hash_ids(id):
    """
    对编号做编码计算
    @param id int
    @return string
    """
    h = Hashids(HASHIDS_SALT)
    return h.encode(id)

def unhash_ids(code):
    """
    对编码做解码
    @param code string
    @return int
    """
    h = Hashids(HASHIDS_SALT)
    return h.decode(code)[0]


if "__main__" == __name__:

    m = hash_ids(1314)
    print(m)

    n = unhash_ids(m)
    print(n)

