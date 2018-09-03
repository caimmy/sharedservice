# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： article_mgr
Description: 产品文章管理
Author: caimmy
date： 2018/8/14
-------------------------------------------------
Change Activity:
2018/8/14
-------------------------------------------------
"""
__author__ = 'caimmy'

from datetime import datetime
from sqlalchemy import and_
from tornado.log import gen_log
from admin import AdminWebRequestHandler
from models.mysql.enterprise_tbls import MProduct, ProductArticle, ProductArticleTag
from tornado_ui.ui_methods import flash, full_url

class ArticleIndex(AdminWebRequestHandler):
    def get(self, *args, **kwargs):
        pid, = self.getArgument_list("pid")
        articles = self.db.query(ProductArticle).filter(ProductArticle.p_id==pid).all()
        return self.render("products_mgr/zhishiku_index.html", breadcrumb=[],
                           pid=pid, articles=articles)

class ArticleCreate(AdminWebRequestHandler):
    """
    创建产品知识库记录（文章）
    """
    def get(self, *args, **kwargs):
        pid, = self.getArgument_list("pid")
        product = self.db.query(MProduct).filter(and_(MProduct.id==pid), (MProduct.ep_id==self.user.get("ep"))).one()
        return self.render("products_mgr/article_create.html", breadcrumb=[], product=product)

    def post(self, *args, **kwargs):
        atitle, atag, adesc, pid = self.getArgument_list("atitle", "atag", "adesc", "pid")
        if all((atitle, adesc, pid)):
            try:
                article = ProductArticle()
                article.title = atitle
                article.content = adesc
                article.create_tm = datetime.now()
                article.uid = self.user.get("id")
                article.p_id = pid
                article.ep_id = self.user.get("ep")

                self.db.add(article)
                self.db.flush()
                # 添加文章标签
                tag_list = atag.split(" ")
                for tag in tag_list:
                    tag = tag.strip()
                    if tag != "":
                        tag_item = ProductArticleTag()
                        tag_item.tagname = tag
                        tag_item.article_id = article.id
                        tag_item.create_tm = datetime.now()
                        tag_item.uid = self.user.get("id")
                        self.db.add(tag_item)

                self.db.commit()
                return self.redirect(full_url(self, "product_article_index", {"pid": pid}))
            except Exception as e:
                self.db.rollback()
                gen_log.error(e)
                flash(self, str(e))
        else:
            flash(self, "parameters invalid")
        return self.redirect(full_url(self, "product_article_create", {"pid": pid}))

