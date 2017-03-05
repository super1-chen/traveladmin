#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2017年 陈超. All rights reserved by Chao.Chen.
# Create on 2017-03-05

__author__ = 'Albert'

import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Create dummy secrey key so we can use sessions
    SECRET_KEY = 'dsfdgknaklndhlfsncdihsfldknvkfldkvniodhiofjrpongonroihfioehroihjgoirebviuhdeg'

    # Flask-Security config
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Project BaseDIR
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):

    # Create in-memory database
    DEBUG = True
    DATABASE_FILE = 'develop_db.sqlite'
    DATABASE_PATH = os.path.join(base_dir, DATABASE_FILE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, DATABASE_FILE)
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):

    DEBUG = False
    DATABASE_FILE = 'db.sqlite'
    DATABASE_PATH = os.path.join(base_dir, DATABASE_FILE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, DATABASE_FILE)
    SQLALCHEMY_ECHO = True


class TestConfig(Config):

    TESTING = True
    DATABASE_FILE = 'test_db.sqlite'
    DATABASE_PATH = os.path.join(base_dir, DATABASE_FILE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, DATABASE_FILE)
    SQLALCHEMY_ECHO = True

config = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig,
    "test": TestConfig,
    "default": DevelopmentConfig
}