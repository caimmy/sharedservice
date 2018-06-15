# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     db
   Description:
   Author:         caimmy
   date：          2018/6/15
-------------------------------------------------
   Change Activity:
                   2018/6/15
-------------------------------------------------
"""
__author__ = 'caimmy'

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_DBNAME, MYSQL_USER, MYSQL_PAWD, DEBUG_MODE

Base = declarative_base()
engine = create_engine('mysql+pymysql://%s:%s@%s:%d/%s?charset=utf8mb4' %
                       (MYSQL_USER, MYSQL_PAWD, MYSQL_HOST, MYSQL_PORT, MYSQL_DBNAME),
                       encoding='utf-8', echo=DEBUG_MODE, pool_size=100, pool_recycle=10)