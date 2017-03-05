#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2017年 陈超. All rights reserved by Chao.Chen.
# Create on 2017-03-05

__author__ = 'Albert'

import os
from jinja2 import Markup
from flask import url_for, redirect, render_template, abort, request
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin import form
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers

from app import app, db
from app.models import User, Role, Travel, Type

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
file_path = os.path.join(app.config['BASEDIR'], "files")


class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


# Flask views
class TravelView(MyModelView):

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.path)))

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }


@app.route('/')
def index():
    return render_template('index.html')

admin = flask_admin.Admin(
    app,
    u'后台',
    base_template='my_master.html',
    template_mode='bootstrap3'
)


admin.add_view(TravelView(Travel, db.session, name=u'行程'))
admin.add_view(MyModelView(Type, db.session, name=u"行程类型"))
admin.add_view(MyModelView(Role, db.session,  name=u"权限"))
admin.add_view(MyModelView(User, db.session,  name=u"用户"))


# define a context processor for merging flask-admin's template context into the
# flask-security views.

@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


