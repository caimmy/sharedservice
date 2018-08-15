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
from sqlalchemy import Column, Integer, VARCHAR, DateTime, TEXT, ForeignKey
from sqlalchemy.orm import relationship
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


class ProductArticle(Base):
    """
    产品知识库（文章）
    """
    __tablename__ = "em_product_article"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    title       = Column(VARCHAR(128), nullable=False, comment="文章标题")
    content     = Column(TEXT, nullable=False, comment="文章内容")
    create_tm   = Column(DateTime, default=datetime.now(), comment="创建时间")
    uid         = Column(Integer, ForeignKey("plat_user.id"), comment="创建者编号")

    ep_id       = Column(Integer, ForeignKey("enterprise.id"), nullable=False, index=True, comment="文章归属的企业编号")
    p_id        = Column(Integer, ForeignKey("em_product.id"), nullable=False, index=True, comment="文章归属的产品编号")

    creator     = relationship("PlatUser", backref="articles")

    def __repr__(self):
        return "<<em_product_article> title: {title}, create_tm: {ctm}>".format(title=self.title, ctm=self.create_tm)

class ProductArticleTag(Base):
    """
    产品知识库摘要（标签）
    """
    __tablename__ = "em_product_article_tag"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    tagname       = Column(VARCHAR(32), nullable=False, comment="摘要名称")
    article_id    = Column(Integer, ForeignKey("em_product_article.id"), nullable=False, index=True, comment="标签归属的文章编号")
    create_tm     = Column(DateTime, default=datetime.now(), comment="标签创建时间")
    uid           = Column(Integer, comment="创建者编号")

    article       = relationship("ProductArticle", backref="tags")

    def __repr__(self):
        return "<<em_product_article_tag> name: {name}, create_tm: {ctm}>".format(name=self.tagname, ctm=self.create_tm)