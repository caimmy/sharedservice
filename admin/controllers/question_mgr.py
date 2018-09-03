# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： question_mgr
Description:
Author: caimmy
date： 2018/8/17
-------------------------------------------------
Change Activity:
2018/8/17
-------------------------------------------------
"""
__author__ = 'caimmy'

from datetime import datetime
from tornado.log import gen_log
from admin import AdminWebRequestHandler
from models.mysql.enterprise_tbls import Enterprise, MProduct, ProductQuestion, ProductQuestionRel
from tornado_ui.ui_methods import flash

class QuestionIndex(AdminWebRequestHandler):
    """
    问答管理索引页
    """
    def get(self, *args, **kwargs):
        ep_id = self.user.get("ep")
        questions = self.db.query(ProductQuestion).filter(ProductQuestion.id==ProductQuestionRel.question_id).\
            filter(ProductQuestionRel.ep_id==ep_id).all()
        return self.render("question_mgr/question_index.html", breadcrumb=[], questions=questions)

class QuestionCreate(AdminWebRequestHandler):
    """
    创建问答
    """
    def get(self, *args, **kwargs):
        ep_id = self.user.get("ep")
        enterprise = self.db.query(Enterprise).filter(Enterprise.id == ep_id).one()
        products = MProduct.allEnabledProducts(self.db, self.user.get("ep"))

        return self.render("question_mgr/question_create.html", breadcrumb=[],
                           enterprise=enterprise, products=products)

    def post(self, *args, **kwargs):
        question, answer, atype, products = self.getArgument_list("question", "answer", "atype", "bind_products[]")
        if all((question, answer, atype, products)):
            try:
                curtime = datetime.now()
                curuser = self.user.get("id")
                ep_id = self.user.get("ep")
                product_question = ProductQuestion()
                product_question.question = question
                product_question.answer = answer
                product_question.atype = atype
                product_question.create_tm = curtime
                product_question.uid = curuser
                self.db.add(product_question)
                self.db.flush()
                for p in products:
                    question_product_rel = ProductQuestionRel()
                    question_product_rel.product_id = p
                    question_product_rel.question_id = product_question.id
                    question_product_rel.create_tm = curtime
                    question_product_rel.uid = curuser
                    question_product_rel.ep_id = ep_id
                    self.db.add(question_product_rel)

                self.db.commit()
                return self.redirect(self.reverse_url("question_index"))
            except Exception as e:
                self.db.rollback()
                gen_log.error(e)
                flash(self, str(e))
        else:
            flash(self, "parameters invalid")
        return self.redirect(self.reverse_url("question_create"))