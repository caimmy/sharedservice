# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     service
   Description:
   Author:         caimmy
   date：          2018/6/14
-------------------------------------------------
   Change Activity:
                   2018/6/14
-------------------------------------------------
"""
__author__ = 'caimmy'

from tornado.web import url
import bp
import tornado

from admin.authentication import LoginRequestHandler, RegisterRequestHandler, IndexRequestHandler, AdminloginRequestHandler, \
    AdminlogoutRequestHandler, ResetPasswordRequestHandler
from admin.productadmin import ProductIndex, ProductCreate, ProductConfig
from admin.article_mgr import ArticleIndex, ArticleCreate
from admin.customer_mgr import CustomerIndex, CustomerCreate
from admin.question_mgr import QuestionIndex, QuestionCreate
from admin import AdminWebRequestHandler


class BaseHandler(AdminWebRequestHandler):
    def get(self, *args, **kwargs):
        raise tornado.web.HTTPError(404)


def CreateBlueprint():
    return bp.Blueprint(r'admin', [
        url(r'/?', IndexRequestHandler, name="admin_index"),
        url(r'/register/?', RegisterRequestHandler),
        (r'/login/?', LoginRequestHandler),
        url(r'/adminlogin/?', AdminloginRequestHandler, name="login"),
        url(r'/logout', AdminlogoutRequestHandler, name="logout"),
        url(r'/profilesetting', ResetPasswordRequestHandler, name="profilesetting"),

        # 产品管理相关
        url(r'/productindex', ProductIndex, name="product_index"),
        url(r'/productcreate', ProductCreate, name="product_create"),
        url(r'/productconfig', ProductConfig, name="product_config"),
        ## 产品知识库相关
        url(r'/product_article_index', ArticleIndex, name="product_article_index"),
        url(r'/product_article_create', ArticleCreate, name="product_article_create"),
        # 客服人员管理相关
        url(r'/customer_index', CustomerIndex, name="customer_index"),
        url(r'/customer_create', CustomerCreate, name="customer_create"),
        # 问答管理
        url(r'/question_index', QuestionIndex, name="question_index"),
        url(r'/question_create', QuestionCreate, name="question_create"),
        url(r'.*', BaseHandler)
    ])