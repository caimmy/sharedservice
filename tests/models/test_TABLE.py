# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： test_MYSQL
Description:
Author: caimmy
date： 2018/7/5
-------------------------------------------------
Change Activity:
2018/7/5
-------------------------------------------------
"""
__author__ = 'caimmy'

import unittest
from sqlalchemy.orm import sessionmaker, scoped_session

from models.mysql.enterprise_tbls import MProduct
from models.mysql.tables import Enterprise,PlatUser

from sqlalchemy import create_engine
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_DBNAME, MYSQL_USER, MYSQL_PAWD, DEBUG_MODE

engine = create_engine('mysql+pymysql://%s:%s@%s:%d/%s?charset=utf8mb4' %
                       (MYSQL_USER, MYSQL_PAWD, MYSQL_HOST, MYSQL_PORT, MYSQL_DBNAME),
                       encoding='utf-8', echo=False, pool_size=100, pool_recycle=10)

class MysqlTest(unittest.TestCase):

    def setUp(self):
        self.db = sessionmaker(bind=engine, autocommit=False, autoflush=True, expire_on_commit=False)()

    def tearDown(self):
        self.db.close()

    def atest_CREATEENTERPRISE(self):
        ep = Enterprise()
        ep.name = '客服'
        ep.email = 'wokao@abc.com'
        ep.salt = 'adsf'
        ep.passwd = 'asdf'
        ep.validaion = '1'
        self.db.add(ep)
        self.db.commit()

    def atest_CREATEPRODUCTS(self):
        p = MProduct()
        p.name = '客服'
        p.label = 'abcd1234'
        p.add_user = 1
        p.ep_id = 1
        p.desc = 'asdfasdf'
        self.db.add(p)
        self.db.commit()

    def atest_QUERYPRODUCT(self):
        m = self.db.query(MProduct).filter(MProduct.label=='abcd1234').first()
        n = m.enterprise
        print(n)

    def test_CREATEUSER(self):
        plat_u = PlatUser()
        plat_u.phone = '13328281234'
        plat_u.passwd = '1234'
        plat_u.salt = '1'
        plat_u.name = 'abc'
        plat_u.email = 'zbc@qq.com'
        plat_u.ep = 1
        self.db.add(plat_u)
        self.db.commit()


if "__main__" == __name__:
    unittest.main()