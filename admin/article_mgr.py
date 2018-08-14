# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： article_mgr
Description: 产品文章管理
Author: caimmy
date： 2018/8/14
-------------------------------------------------
Change Activity:
2018/8/14
-------------------------------------------------
"""
__author__ = 'caimmy'

from sqlalchemy import and_

from admin import AdminWebRequestHandler
from models.mysql.enterprise_tbls import MProduct


class ArticleIndex(AdminWebRequestHandler):
    def get(self, *args, **kwargs):
        pid, = self.getArgument_list("pid")
        return self.render("products_mgr/zhishiku_index.html", breadcrumb=[],
                           pid=pid)

class ArticleCreate(AdminWebRequestHandler):
    def get(self, *args, **kwargs):
        pid, = self.getArgument_list("pid")
        product = self.db.query(MProduct).filter(and_(MProduct.id==pid), (MProduct.ep_id==self.user.get("ep"))).one()
        return self.render("products_mgr/article_create.html", breadcrumb=[], product=product)

    def post(self, *args, **kwargs):
        pass