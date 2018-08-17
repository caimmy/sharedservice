# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： customer_mgr
Description:
Author: caimmy
date： 2018/8/16
-------------------------------------------------
Change Activity:
2018/8/16
-------------------------------------------------
"""
__author__ = 'caimmy'

from datetime import datetime
from tornado.log import gen_log
from admin import AdminWebRequestHandler
from models.mysql.tables import Enterprise
from models.mysql.enterprise_tbls import MProduct, Customer, CustomerEnterpriseRel
from models import USER_CREATE_METHOD_ENTERPRISE
from tornado_ui.ui_methods import flash

class CustomerIndex(AdminWebRequestHandler):
    def get(self, *args, **kwargs):
        customers = self.db.query(Customer).filter(Customer.id==CustomerEnterpriseRel.cm_id)\
            .filter(CustomerEnterpriseRel.ep_id==self.user.get("ep")).all()
        return self.render("customer_mgr/customer_index.html", breadcrumb=[],
                           customers=customers)

class CustomerCreate(AdminWebRequestHandler):
    def get(self, *args, **kwargs):
        enterprise = self.db.query(Enterprise).filter(Enterprise.id==self.user.get("ep")).one()
        products_list = MProduct.allEnabledProducts(self.db, self.user.get("ep"))
        return self.render("customer_mgr/customer_create.html", breadcrumb=[],
                           enterprise=enterprise, products=products_list)

    def post(self, *args, **kwargs):
        ep, name, phone, pwd, status, products = \
            self.getArgument_list("ep", "name", "phone", "pwd", "status", "bind_products[]")
        if all((ep, name, phone, pwd, status)):
            try:
                user = Customer()
                salt, password = user.genPassword(pwd)
                user.name = name
                user.phone = phone
                user.passwd = password
                user.salt = salt
                user.status = status
                user.create_tm = datetime.now()
                user.create_platuid = self.user.get("id")
                self.db.add(user)
                self.db.flush()
                user_enterprise_rel = CustomerEnterpriseRel()
                user_enterprise_rel.ep_id = self.user.get("ep")
                user_enterprise_rel.cm_id = user.id
                user_enterprise_rel.product_id = 0
                user_enterprise_rel.create_tm = datetime.now()
                user_enterprise_rel.create_method = USER_CREATE_METHOD_ENTERPRISE
                user_enterprise_rel.uid = self.user.get("id")
                self.db.add(user_enterprise_rel)
                for p in products:
                    uer = CustomerEnterpriseRel()
                    uer.ep_id = user_enterprise_rel.ep_id
                    uer.cm_id = user.id
                    uer.product_id = p
                    uer.create_tm = datetime.now()
                    uer.create_method = user_enterprise_rel.create_method
                    uer.uid = user_enterprise_rel.uid
                    self.db.add(uer)
                self.db.commit()
                return self.redirect(self.reverse_url("customer_index"))
            except Exception as e:
                self.db.rollback()
                gen_log.error(e)
                flash(self, str(e))
        else:
            flash(self, "parameter invalid")
        return self.redirect(self.reverse_url("customer_create"))