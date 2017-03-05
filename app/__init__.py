#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2017年 陈超. All rights reserved by Chao.Chen.
# Create on 2017-03-05

__author__ = 'Albert'

"""
config = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig,
    "test": TestConfig,
    "develop": DevelopmentConfig
}
"""

import os
from six.moves import builtins
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers

from config import config


config_name = os.getenv('TRAVEL_CONFIG', "default")

app = Flask(__name__, static_folder='files')

app.config.from_object(config[config_name])
app.jinja_env.line_statement_prefix = '#'
app.jinja_env.globals.update(builtins.__dict__)

config[config_name].init_app(app)

db = SQLAlchemy(app)


# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)
#
# class MyModelView(sqla.ModelView):
#
#     def is_accessible(self):
#         if not current_user.is_active or not current_user.is_authenticated:
#             return False
#
#         if current_user.has_role('superuser'):
#             return True
#
#         return False
#
#     def _handle_view(self, name, **kwargs):
#         """
#         Override builtin _handle_view in order to redirect users when a view is not accessible.
#         """
#         if not self.is_accessible():
#             if current_user.is_authenticated:
#                 # permission denied
#                 abort(403)
#             else:
#                 # login
#                 return redirect(url_for('security.login', next=request.url))
#
#
# admin = flask_admin.Admin(
#     app,
#     '旅游后台系统',
#     base_template='my_master.html',
#     template_mode='bootstrap3',
# )
#
#
#
# # define a context processor for merging flask-admin's template context into the
# # flask-security views.
# @security.context_processor
# def security_context_processor():
#     return dict(
#         admin_base_template=admin.base_template,
#         admin_view=admin.index_view,
#         h=admin_helpers,
#         get_url=url_for
#     )
#
#
# def build_sample_db():
#     """
#     Populate a small db with some example entries.
#     """
#
#     db.drop_all()
#     db.create_all()
#
#     with app.app_context():
#         user_role = Role(name='user')
#         super_user_role = Role(name='superuser')
#         db.session.add(user_role)
#         db.session.add(super_user_role)
#         db.session.commit()
#
#         admin_user = user_datastore.create_user(
#             username='Admin',
#             password=encrypt_password('admin'),
#             roles=[user_role, super_user_role]
#         )
#         print admin_user
#
#         db.session.commit()
#     return

