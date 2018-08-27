# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： service.py
Description:
Author: caimmy
date： 2018/8/23
-------------------------------------------------
Change Activity:
2018/8/23
-------------------------------------------------
"""
__author__ = 'caimmy'

from tornado.web import url
import bp
from customer.customer_index import CustomerIndex, CustomerDashboard, CustomerRegister, CustomerLogin, CustomerLogout

def CreateBlueprint():
    return bp.Blueprint(r"customer", [
        url(r"/?", CustomerIndex, name="customer_frontpage_index"),
        url(r"/dashboard/?", CustomerDashboard, name="customer_frontpage_dashboard"),
        url(r"/register/?", CustomerRegister, name="customer_frontpage_register"),
        url(r"/login/?", CustomerLogin, name="customer_frontpage_login"),
        url(r"/logout/?", CustomerLogout, name="customer_frontpage_logout"),
    ])