# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： customer_index
Description:
Author: caimmy
date： 2018/8/23
-------------------------------------------------
Change Activity:
2018/8/23
-------------------------------------------------
"""
__author__ = 'caimmy'

from sqlalchemy.sql import exists
from tornado.log import gen_log

from customer import CustomerWebRequestHandler
from tornado_ui.ui_methods import flash

from models.mysql.enterprise_tbls import Customer
from utils.wraps import web_customer_login

class CustomerIndex(CustomerWebRequestHandler):
    def get(self, *args, **kwargs):
        return self.render("frontpage/customer_index.html")

class CustomerDashboard(CustomerWebRequestHandler):
    @web_customer_login
    def get(self, *args, **kwargs):
        return self.render("frontpage/customer_dashboard.html")

class CustomerRegister(CustomerWebRequestHandler):
    def get(self, *args, **kwargs):
        return self.render("frontpage/customer_register.html")

    def post(self, *args, **kwargs):
        username, gender, phone, code = self.getArgument_list("username", "gender", "phone", "code")
        if all((username, gender, phone, code)):
            try:
                if self.db.query(~exists().where(Customer.phone==phone)).scalar():
                    customer = Customer()
                    s, p = customer.genPassword(code)
                    customer.name = username
                    customer.phone = phone
                    customer.passwd = p
                    customer.salt = s
                    customer.gender = gender
                    self.db.add(customer)
                    self.db.commit()
                    return self.redirect(self.reverse_url("customer_frontpage_index"))
                else:
                    flash(self, "手机号码已经被注册")
            except Exception as e:
                self.db.rollback()
                gen_log.error(str(e))
                flash(self, str(e))
        else:
            flash(self, "parameters invalid")
        return self.redirect(self.reverse_url("customer_frontpage_register"))

class CustomerLogin(CustomerWebRequestHandler):
    def get(self, *args, **kwargs):
        return self.render("frontpage/customer_login.html")

    def post(self, *args, **kwargs):
        phone, pwd = self.getArgument_list("phone", "pwd")
        if all((phone, pwd)):
            customer_user = self.db.query(Customer).filter(Customer.phone==phone).first()
            if customer_user and customer_user.checkPassword(pwd):
                self.Login(customer_user.getAttributes())
                return self.redirect(self.reverse_url("customer_frontpage_dashboard"))
            else:
                flash(self, "phone number not exists or invalid password.")
        else:
            flash(self, "parameter invalid")
        return self.redirect(self.reverse_url("customer_frontpage_login"))

class CustomerLogout(CustomerWebRequestHandler):
    def get(self, *args, **kwargs):
        if self.current_user:
            self.Loginout()
        return self.redirect(self.reverse_url("customer_frontpage_index"))