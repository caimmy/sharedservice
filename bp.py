# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     blueprint
   Description:
   Author:         caimmy
   date：          2018/5/28
-------------------------------------------------
   Change Activity:
                   2018/5/28
-------------------------------------------------
"""
__author__ = 'caimmy'

class Blueprint:
    def __init__(self, name, rules):
        self.bpname     = name if name.startswith("/") else "/" + name
        self.rules      = rules

    def GetSubRouters(self):
        return [(self.bpname + rule_prefix[0], rule_prefix[1]) for rule_prefix in self.rules]