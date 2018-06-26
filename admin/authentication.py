# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     authentication
   Description:
   Author:         caimmy
   date：          2018/6/14
-------------------------------------------------
   Change Activity:
                   2018/6/14
-------------------------------------------------
"""
__author__ = 'caimmy'

from lib import SSWebDataRequestHandler
from utils.wraps import web_authenticate, jsonp
from models.mysql.tables import User
from admin import AdminWebRequestHandler

class LoginRequestHandler(SSWebDataRequestHandler):
    @jsonp
    def get(self):
        phone   = self.get_argument('phone', '')
        pwd     = self.get_argument('pass', '')
        user = self.db.query(User).filter(User.phone == phone).first()
        if user:
            self.changeResponse2Success(str(user).encode('utf-8'))
        else:
            self.setResponseMsg('用户不存在')
        return self.jsonResponse()

    def optionsa(self):
        self.write(self.jsonResponse())

class AdminloginRequestHandler(AdminWebRequestHandler):
    def get(self):
        if self.current_user:
            return self.redirect(self.reverse_url("admin_index"))
        return self.render("login.html")

    def post(self):
        username, password = self.getArgument_list("username", "password")
        user = self.db.query(User).filter(User.email==username).first()
        if user is None:
            return self.redirect(self.reverse_url("login"))
        else:
            self.Login(user.getAttributes())
            return self.redirect(self.reverse_url("admin_index"))

class AdminlogoutRequestHandler(AdminWebRequestHandler):
    def get(self):
        self.Loginout()
        return self.redirect(self.reverse_url("login"))

class RegisterRequestHandler(SSWebDataRequestHandler):
    def get(self):
        user = User()
        user.name = '蔡淼'
        user.phone = '15902811426'
        user.salt = '123456'
        user.passwd = 'aabbccdd'
        self.db.add(user)
        self.db.commit()
        self.write("success")

class IndexRequestHandler(AdminWebRequestHandler):
    @web_authenticate
    def get(self):
        self.render('index.html')
