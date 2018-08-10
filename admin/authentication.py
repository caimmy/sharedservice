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

import tornado.log
from lib import SSWebDataRequestHandler
from utils.wraps import web_authenticate, jsonp
from models.mysql.tables import PlatUser
from admin import AdminWebRequestHandler
from tornado_ui.ui_methods import flash

class LoginRequestHandler(AdminWebRequestHandler):
    @jsonp
    def get(self):
        phone   = self.get_argument('phone', '')
        pwd     = self.get_argument('pass', '')
        user = self.db.query(PlatUser).filter(PlatUser.phone == phone).first()
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
        user = self.db.query(PlatUser).filter(PlatUser.email==username).first()
        if user is None:
            return self.redirect(self.reverse_url("login"))
        else:
            if user.checkPassword(password):
                self.Login(user.getAttributes())
            else:
                flash(self, "密码错误")
            return self.redirect(self.reverse_url("login"))

class AdminlogoutRequestHandler(AdminWebRequestHandler):
    def get(self):
        if self.current_user:
            self.Loginout()
        return self.redirect(self.reverse_url("login"))

class RegisterRequestHandler(SSWebDataRequestHandler):
    def get(self):
        user = PlatUser()
        user.name = '蔡淼'
        user.phone = '15902811426'
        user.salt = '123456'
        user.passwd = 'aabbccdd'
        self.db.add(user)
        self.db.commit()
        self.write("success")

class ResetPasswordRequestHandler(AdminWebRequestHandler):
    def get(self):
        return self.render('profile/personsetting.html')

    def post(self):
        cur_pass, set_pass = self.getArgument_list("cur_password", "set_password")
        me = self.get_current_user()
        self_obj = self.db.query(PlatUser).filter(PlatUser.id==me.get('id')).one()
        if self_obj and self_obj.checkPassword(cur_pass):
            try:
                salt, new_pass = self_obj.genPassword(set_pass)
                self_obj.salt = salt
                self_obj.passwd = new_pass
                self.db.commit()
                flash(self, "修改密码成功", "info")
                return self.redirect(self.reverse_url("admin_index"))
            except Exception as e:
                tornado.log.gen_log.error(e)
                flash(self, "出现异常 " + str(e))
        else:
            flash(self, "原密码错误")
        return self.render("profile/personsetting.html")

class IndexRequestHandler(AdminWebRequestHandler):
    @web_authenticate
    def get(self):
        breadcrumb = [
            {"name": "首页", "url": "/", "class": "ace-icon fa fa-home home-icon"},
            {"name": "控制面板"}
        ]
        self.render('index.html', breadcrumb=breadcrumb)
