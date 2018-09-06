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
from sqlalchemy import Column, Integer, VARCHAR, DateTime, TEXT, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models import ENUM_VALID, ENUM_INVALID, ENUM_DELETE, USER_CREATE_METHOD_AUTO, USER_CREATE_METHOD_ENTERPRISE, \
    USER_CREATE_METHOD_SYSTEM, ENUM_GENDER_FEMALE, ENUM_GENDER_MALE
from models.mysql.tables import Enterprise
from models import PasswordBase
from const_defines import SIDE_ROLE_STAFF, SIDE_ROLE_ENTERPRISE

class MProduct(Base):
    """
    企业产品表
    """
    __tablename__   = 'em_product'

    id              = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(VARCHAR(128), nullable=False, comment='产品名称')
    label           = Column(VARCHAR(64), unique=True, nullable=False, index=True, comment='产品标识，唯一属性')
    desc            = Column(TEXT, nullable=False, comment='产品描述')
    add_user        = Column(Integer, nullable=False, comment="添加产品的用户")
    add_time        = Column(DateTime, default=datetime.now())
    ep_id           = Column(Integer, ForeignKey("enterprise.id"), nullable=False, index=True, comment='产品归属的企业的编号')
    status          = Column(Enum(ENUM_VALID, ENUM_INVALID, ENUM_DELETE), comment="产品的状态")

    enterprise = relationship("Enterprise", backref="products")

    @staticmethod
    def allEnabledProducts(db, ep_id):
        return db.query(MProduct).filter(MProduct.ep_id==ep_id).all()

    def __repr__(self):
        return "<<m_product> id: {id}, name: {name}, label: {label} >".format(id=self.id, name=self.name, label=self.label)

class Staff(Base, PasswordBase):
    '''
    客服账号表
    '''
    __tablename__   = 'staff_user'

    id              = Column(Integer, primary_key=True, autoincrement=True)
    hashid          = Column(VARCHAR(128), nullable=False, unique=True, index=True, comment="哈希后的数据编号")
    name            = Column(VARCHAR(128), nullable=False, comment='客服名称')
    phone           = Column(VARCHAR(20), nullable=False, unique=True, index=True, comment='客服联系电话')
    salt            = Column(VARCHAR(6), nullable=False, comment='密码salt')
    passwd          = Column(VARCHAR(128), nullable=False, comment='客服账号密码')
    gender          = Column(Enum(ENUM_GENDER_FEMALE, ENUM_GENDER_MALE), default=ENUM_GENDER_FEMALE, comment='客服账号性别')
    status          = Column(Enum(ENUM_VALID, ENUM_INVALID, ENUM_DELETE), default=ENUM_VALID, comment='客服账号状态')
    create_tm       = Column(DateTime, default=datetime.now(), comment='客服账号的创建时间')
    create_platuid  = Column(Integer, default=0, comment="创建客服账号的平台用户编号， 0标识玩家自助注册账号")

    def getAttributes(self):
        '''
        获取用户模型的属性
        :return: dict
        '''
        return {"hashid": self.hashid, "name": self.name, "gender": self.gender, "side": SIDE_ROLE_STAFF}

    def __repr__(self):
        return '<<Table> Custom_user> : id: {id}, name: {name}, phone: {phone}, create_tm: {create_tm}'.format(
            id=self.id,
            name=self.name,
            phone=self.phone,
            create_tm=self.create_tm
        )

class StaffEnterpriseRel(Base):
    """
    客服和企业的关系表
    """
    __tablename__       = "staff_enterprise_rel"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    ep_id               = Column(Integer, ForeignKey("enterprise.id"), comment="企业编号")
    cm_id               = Column(Integer, ForeignKey("staff_user.id"), comment="客服编号")
    product_id          = Column(Integer, index=True, default=0, comment="关联的产品编号")
    create_tm           = Column(DateTime, default=datetime.now(), comment="客服企业关系建立时间")
    create_method       = Column(Enum(USER_CREATE_METHOD_AUTO, USER_CREATE_METHOD_ENTERPRISE, USER_CREATE_METHOD_SYSTEM),
                                 default="auto", comment="创建本条关系的方式， auto客服自动申请创建， enterprise企业创建， system平台设置")
    uid                 = Column(Integer, comment="创建者")

    staff               = relationship("Staff", foreign_keys=[cm_id], backref="ep_rel")

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

class ProductQuestion(Base):
    """
    产品或企业问答知识，供机器人客服理解
    """
    __tablename__   = "em_product_question"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    question        = Column(VARCHAR(256), nullable=False, comment="问题内容")
    answer          = Column(TEXT, nullable=False, comment="回答内容")
    atype           = Column(Integer, default=1, comment="答案类型，1：文本，2：富文本，3：图片，4：声音；5：连接")
    create_tm       = Column(DateTime, default=datetime.now(), comment="问题创建时间")
    uid             = Column(Integer, comment="创建者编号")

    def __repr__(self):
        return "<<ProductQuestion> question: {ques}>".format(ques=self.question)

class ProductQuestionSamerel(Base):
    """
    问答知识的相同问题
    """
    __tablename__   = "em_product_question_same_rel"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    question        = Column(VARCHAR(255), nullable=False, comment="问题内容")
    qid             = Column(Integer, ForeignKey("em_product_question.id"), comment="相同问答的记录编号")
    create_tm       = Column(DateTime, default=datetime.now(), comment="相似问题创建时间")
    uid             = Column(Integer, comment="创建者编号")

    question_item   = relationship("ProductQuestion", backref="samequestions")

    def __repr__(self):
        return "<<ProductQuestionSamerel>: {_q}".format(_q=self.question)

class ProductQuestionRel(Base):
    """
    问题和产品的关联关系
    """
    __tablename__   = "em_product_question_rel"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    product_id      = Column(Integer, ForeignKey("em_product.id"), nullable=False, comment="产品编号")
    question_id     = Column(Integer, ForeignKey("em_product_question.id"), nullable=False, comment="问题编号")
    ep_id           = Column(Integer, ForeignKey("enterprise.id"), nullable=False, comment="关联企业的编号")
    create_tm       = Column(DateTime, default=datetime.now(), comment="创建关联关系的时间")
    uid             = Column(Integer, comment="创建者编号")

    product         = relationship("MProduct", backref="questions")

    def __repr__(self):
        return "<<ProductQuestionRel>: product_id_{_p} - question_id_{_q}".format(_p=self.product_id, _q=self.question_id)
