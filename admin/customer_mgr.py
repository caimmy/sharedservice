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
import json
from tornado.log import gen_log
from admin import AdminWebRequestHandler
from models.mysql.tables import Enterprise
from models.mysql.enterprise_tbls import MProduct, Customer, CustomerEnterpriseRel
from models import USER_CREATE_METHOD_ENTERPRISE
from tornado_ui.ui_methods import flash, full_url

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


class CustomerDetail(AdminWebRequestHandler):
    def get(self, *args, **kwargs):
        cid, = self.getArgument_list("cid")
        if cid:
            customer = self.db.query(Customer).filter(Customer.id==int(cid)).one()
            ep_rels_list = customer.ep_rel

            return self.render("customer_mgr/customer_detail.html", breadcrumb=[],
                               customer=customer, products=MProduct.allEnabledProducts(self.db, self.user.get("ep")),
                               ep_rels=json.dumps([str(p.product_id) for p in ep_rels_list if p.product_id != 0]))
        else:
            flash(self, "cid not provide")
        return self.redirect(self.reverse_url("customer_index"))

    def post(self, *args, **kwargs):
        cid, = self.getArgument_list("cid")
        uid, name, phone, pwd, status, products = \
            self.getArgument_list("uid", "name", "phone", "pwd", "status", "bind_products[]")
        ep_id = self.user.get("ep")
        cur_user_id = self.user.get("id")
        if all((uid, name, phone, status, products)):
            products = [int(p) for p in products]
            try:
                customer = self.db.query(Customer).filter(Customer.id==uid).one()
                customer.name = name
                customer.phone = phone
                if "" != pwd:
                    salt, password = customer.genPassword(pwd)
                    customer.salt = salt
                    customer.passwd = password
                for cur_rel in customer.ep_rel:
                    if cur_rel.product_id in products:
                        products.remove(cur_rel.product_id)
                    elif cur_rel.product_id != 0:
                        customer.ep_rel.remove(cur_rel)
                        self.db.delete(cur_rel)
                for p in products:
                    uer = CustomerEnterpriseRel()
                    uer.ep_id = ep_id
                    uer.cm_id = customer.id
                    uer.product_id = p
                    uer.create_tm = datetime.now()
                    uer.create_method = USER_CREATE_METHOD_ENTERPRISE
                    uer.uid = cur_user_id
                    customer.ep_rel.append(uer)
                self.db.commit()
                return self.redirect(self.reverse_url("customer_index"))
            except Exception as e:
                self.db.rollback()
                gen_log.error(e)
                flash(self, str(e))
        else:
            flash(self, "some parameters lost")
        return self.redirect(full_url(self, "customer_detail", {"cid": cid}))
