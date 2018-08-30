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

import hashlib

from datetime import datetime
from sqlalchemy import Column, Integer, VARCHAR, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from models.mysql.db import Base
from models import PasswordBase
from utils.tools import genSalt, ensureBytes
from const_defines import SIDE_ROLE_ENTERPRISE

class PlatUser(Base, PasswordBase):
    __tablename__   = 'plat_user'
    '''
    后台用户信息表
    '''
    id              = Column(Integer, primary_key=True, autoincrement=True)
    email           = Column(VARCHAR(128), unique=True, index=True, comment='用户账号，以邮箱为索引')
    phone           = Column(VARCHAR(20), unique=True, index=True, comment='用户电话号码')
    name            = Column(VARCHAR(10), nullable=False, comment='用户名称')
    salt            = Column(VARCHAR(6), nullable=False)
    passwd          = Column(VARCHAR(128), nullable=False)
    create_tm       = Column(DateTime, default=datetime.now(), comment='账号创建时间')
    ep              = Column(Integer, ForeignKey("enterprise.id"), nullable=False, index=True, comment="成员所属的企业编号")

    enterprise      = relationship("Enterprise", backref="users")

    def getAttributes(self):
        '''
        获取用户模型的属性
        :return: dict
        '''
        return {"id": self.id, "name": self.name, "email": self.email, "phone": self.phone, "ep": self.ep, "side": SIDE_ROLE_ENTERPRISE}

    def __repr__(self):
        return "<<Table> Plat_user> : id {_id}, phone: {_p}, name: {_name}, ep: {_ep}".format(_id=self.id,
                                                                              _p=self.phone,
                                                                              _name=self.name, _ep=self.ep)


class Enterprise(Base):
    '''
    企业账号表
    '''
    __tablename__   = 'enterprise'

    id              = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(VARCHAR(128), nullable=False, comment='企业名称')
    email           = Column(VARCHAR(128), nullable=False, unique=True, index=True, comment='企业账号的登陆邮箱')
    salt            = Column(VARCHAR(6), nullable=False)
    passwd          = Column(VARCHAR(128), nullable=False, comment='企业账号的密码')
    validaion       = Column(Enum('0', '1'), default='0', comment='企业是否经过认证')
    create_tm       = Column(DateTime, default=datetime.now(), comment='企业账号的创建时间')
    expire_tm       = Column(DateTime, default=datetime.now(), comment='企业账号的认证过期时间')

    def __repr__(self):
        return '<<Table> Enterprise_user> : id: {_id}, name: {_name}, email: {_email}, create_tm: {_create_tm}, expire_tm: {_expire_tm}'.format(
            _id=self.id,
            _name=self.name,
            _email=self.email,
            _create_tm=self.create_tm,
            _expire_tm=self.expire_tm
        )

class EnterpriseAuthentication(Base):
    """
    企业认证信息
    """
    __tablename__   = "enterprise_auth"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    catalog         = Column(Integer, nullable=False, comment="主体类型")
    name            = Column(VARCHAR(128), nullable=False, comment="企业主体名称")
    authid          = Column(VARCHAR(256), nullable=False, comment="证照号")
