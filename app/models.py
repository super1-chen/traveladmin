#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2017年 陈超. All rights reserved by Chao.Chen.
# Create on 2017-03-05

__author__ = 'Albert'

import os
from flask_security import UserMixin, RoleMixin
from sqlalchemy.event import listens_for
from flask_admin import form
from . import app, db

file_path = os.path.join(app.config.get('BASEDIR'), "files")

try:
    os.mkdir(file_path)
except OSError:
    pass

# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

travel_types = db.Table(
    'travel_types',
    db.Column('travel_id', db.Integer(), db.ForeignKey('travel.id')),
    db.Column('type_id', db.Integer(), db.ForeignKey('type.id'))
)

# travel_tables = db.Table(
#     ""
# )

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    @staticmethod
    def insert_roles():
        roles = ('user', 'superuser')
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.name = r
            db.session.add(role)
        db.session.commit()

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

# type of travel
class Type(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

# type
class Travel(db.Model):

    __tablename__ = 'travel'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)  # 标题
    departure = db.Column(db.String(255))  #出发地
    destination = db.Column(db.String(255))  # 目的地
    agency = db.Column(db.String(100))   # 供应商
    days = db.Column(db.Integer())  # 旅游的天数
    price = db.Column(db.Float())  # 价格
    publish_at = db.Column(db.DateTime())  # 发表时间

    path = db.Column(db.Unicode(256))
    active = db.Column(db.Boolean())
    types = db.relationship('Type', secondary=travel_types,
                            backref=db.backref('travels', lazy='dynamic'))
    # fixme this item no work
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 发表用户的id

@listens_for(Travel, 'after_delete')
def del_image(mapper, connection, target):

    if target.path:
        # Delete image
        try:
            os.remove(os.path.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(os.path.join(file_path, form.thumbgen_filename(target.path)))
        except OSError:
            pass
