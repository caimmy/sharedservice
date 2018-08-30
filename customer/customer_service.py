# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： customer_service
Description:
Author: caimmy
date： 2018/8/30
-------------------------------------------------
Change Activity:
2018/8/30
-------------------------------------------------
"""
__author__ = 'caimmy'

from customer import CustomerWebRequestHandler

class TxtliveServiceIndex(CustomerWebRequestHandler):
    def get(self, *args, **kwargs):

        return self.render("service/txtlive_service.html")