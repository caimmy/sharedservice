# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： build_tables
Description:
Author: caimmy
date： 2018/7/5
-------------------------------------------------
Change Activity:
2018/7/5
-------------------------------------------------
"""
__author__ = 'caimmy'

from models.mysql.db import engine, Base

from models.mysql.tables import *
from models.mysql.enterprise_tbls import *

if "__main__" == __name__:
    res = Base.metadata.create_all(engine)
    print(res)
    print("completed")