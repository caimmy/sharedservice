# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： enterprise_tbls
Description:
Author: caimmy
date： 2018/7/5
-------------------------------------------------
Change Activity:
2018/7/5
-------------------------------------------------
"""
__author__ = 'caimmy'

from models.mysql.db import Base
from datetime import datetime
from sqlalchemy import Column, Integer, VARCHAR, DateTime, Enum, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from models import ENUM_VALID, ENUM_INVALID, ENUM_DELETE
from models.mysql.tables import Enterprise

class MProduct(Base):
    """
    企业产品表
    """
    __tablename__ = 'em_product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(128), nullable=False, comment='产品名称')
    label = Column(VARCHAR(64), unique=True, nullable=False, index=True, comment='产品标识，唯一属性')
    desc = Column(TEXT, nullable=False, comment='产品描述')
    add_user = Column(Integer, nullable=False, comment="添加产品的用户")
    add_time = Column(DateTime, default=datetime.now())
    ep_id = Column(Integer, ForeignKey("enterprise.id"), nullable=False, index=True, comment='产品归属的企业的编号')

    enterprise = relationship("Enterprise", backref="products")

    def __repr__(self):
        return "<<m_product> id: {id}, name: {name}, label: {label} >".format(id=self.id, name=self.name, label=self.label)


class ServiceRequirements(Base):
    """
    企业服务需求
    """

    __tablename__ = "em_servicerequire"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(VARCHAR(128), nullable=False, comment="服务需求名称")
    label       = Column(VARCHAR(64), unique=True, nullable=False, index=True, comment="服务需求标识，唯一属性")
    start_tm    = Column(DateTime, comment="服务时段（起始时间）")
    end_tm      = Column(DateTime, comment="服务时段（结束时间）")
    memo        = Column(TEXT, comment="服务介绍")
    ep_id       = Column(Integer, ForeignKey("enterprise.id"), nullable=False, index=True, comment="服务需求归属的企业")
    p_id        = Column(Integer, ForeignKey("em_product.id"), nullable=False, index=True, comment="服务需求归属的产品")

    def __repr__(self):
        return "<<em_servicerequire> id: {id}, name: {name}, label: {label}, start_tm: {stm}, end_tm: {etm}".format(
            id=self.id, name=self.name, label=self.label, stm=self.start_tm, etm=self.end_tm
        )