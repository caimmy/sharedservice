# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
   File Name：     tables
   Description:
   Author:         caimmy
   date：          2018/6/15
-------------------------------------------------
   Change Activity:
                   2018/6/15
-------------------------------------------------
"""
__author__ = 'caimmy'

from datetime import datetime
from sqlalchemy import Column, Integer, VARCHAR, DateTime
from models.mysql.db import engine, Base

class User(Base):
    __tablename__   = 'user'

    id              = Column(Integer, primary_key=True, autoincrement=True)
    phone           = Column(VARCHAR(20), unique=True, index=True)
    name            = Column(VARCHAR(10), nullable=False)
    salt            = Column(VARCHAR(6), nullable=False)
    passwd          = Column(VARCHAR(128), nullable=False)
    create_tm       = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return "<<Table> User> : id {_id}, phone: {_p}, name: {_name}".format(_id=self.id,
                                                                              _p=self.phone,
                                                                              _name=self.name)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print("ok")