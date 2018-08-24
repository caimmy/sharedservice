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

from customer import CustomerWebRequestHandler

class CustomerIndex(CustomerWebRequestHandler):
    def get(self, *args, **kwargs):
        return self.render("frontpage/customer_index.html")

class CustomerDashboard(CustomerWebRequestHandler):
    def get(self, *args, **kwargs):
        return self.render("frontpage/customer_dashboard.html")