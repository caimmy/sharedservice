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

import os, sys
from datetime import datetime
p = os.getcwd()
root_path = os.path.dirname(os.path.dirname(p))
sys.path.append(root_path)
from models.mysql.db import engine, Base
from sqlalchemy.orm import sessionmaker, session

from models.mysql.tables import *
from models.mysql.enterprise_tbls import *

def init_Tables():
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=True, expire_on_commit=False)
    conn = Session()
    try:
        enterprise = Enterprise()
        enterprise.name = "瑞某科技"
        enterprise.email = "ruimou@qq.com"
        enterprise.validaion = '1'
        enterprise.expire_tm = enterprise.create_tm = datetime.now()
        enterprise.salt = '1'
        enterprise.passwd = "2"
        conn.add(enterprise)
        conn.flush()

        platuser = PlatUser()
        platuser.name = "caimmy"
        platuser.phone = "19981299007"
        platuser.email = "ruimou@qq.com"
        platuser.salt, platuser.passwd = platuser.genPassword("abcd1234")
        platuser.create_tm = datetime.now()
        platuser.ep = enterprise.id
        conn.add(platuser)
        conn.commit()
        print("init table success")
    except Exception as e:
        conn.rollback()
        print(e)



if "__main__" == __name__:
    drop_res = Base.metadata.drop_all(engine)
    print(drop_res)
    res = Base.metadata.create_all(engine)
    print(res)

    init_Tables()