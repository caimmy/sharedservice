# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： productadmin
Description:
Author: caimmy
date： 2018/8/13
-------------------------------------------------
Change Activity:
2018/8/13
-------------------------------------------------
"""
__author__ = 'caimmy'

from datetime import datetime
from tornado.log import gen_log
from sqlalchemy import and_

from admin import AdminWebRequestHandler
from models.mysql.enterprise_tbls import MProduct
from tornado_ui.ui_methods import flash
from utils.ids import generateUUID

class ProductIndex(AdminWebRequestHandler):
    def get(self):
        breadcrumb = {
            "title": ["业务管理", "产品"],
            "nav": [
                {"name": "首页", "url": "/"},
                {"name": "产品管理", "url": ""},
                {"name": "索引"}
            ]
        }
        current_user = self.get_current_user()
        products_list = self.db.query(MProduct).filter(MProduct.ep_id == current_user.get("ep")).all()
        return self.render("products_mgr/index.html", breadcrumb=breadcrumb,
                           products=products_list)

class ProductCreate(AdminWebRequestHandler):
    def get(self):
        breadcrumb = {
            "title": ["业务管理", "产品"],
            "nav": [
                {"name": "首页", "url": "/"},
                {"name": "产品管理", "url": ""},
                {"name": "索引", "url": self.reverse_url("product_index")},
                {"name": "创建产品"}
            ]
        }
        return self.render("products_mgr/create_product.html", breadcrumb=breadcrumb)

    def post(self):
        name, desc = self.getArgument_list("pname", "pdesc")
        if all((name, desc)):
            try:
                product = MProduct()
                product.name = name
                product.desc = desc
                product.add_user = self.user.get("id")
                product.add_time = datetime.now()
                product.label = generateUUID()
                product.ep_id = self.user.get("ep")
                self.db.add(product)
                self.db.commit()
                return self.redirect(self.reverse_url("product_index"))
            except Exception as e:
                self.db.rollback()
                gen_log.error(e)
                flash(self, str(e))
        return self.redirect(self.reverse_url("product_create"))

class ProductConfig(AdminWebRequestHandler):
    def get(self, *args, **kwargs):
        pid, = self.getArgument_list("pid")
        product = self.db.query(MProduct).filter(and_(MProduct.id==pid), MProduct.ep_id==self.user.get("ep")).one()

        return self.render("products_mgr/product_configure.html", breadcrumb=[],
                           product=product)
