#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2017年 陈超. All rights reserved by Chao.Chen.
# Create on 2017-03-05

__author__ = 'Albert'


import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from flask_script import Manager, Shell
from flask_babelex import Babel
from flask_security import SQLAlchemyUserDatastore, Security
from flask_migrate import Migrate, MigrateCommand
from flask_security.utils import encrypt_password

from app import app, db
from app.admin import views, user_datastore
from app.models import User, Role

manager = Manager(app)
migrate = Migrate(app, db)
babel = Babel(app)



def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def admin():
    from getpass import getpass
    first_name = raw_input("\_admin first name: ")
    last_name = raw_input("\_admin last name: ")
    email = raw_input("\_admin email: ")
    password = getpass("\_admin password: ")

    user_role = Role(name='user')
    super_user_role = Role(name='superuser')

    admin_user = user_datastore.create_user(
        first_name = first_name,
        last_name = last_name,
        email = email,
        password = encrypt_password(password),
        roles = [user_role, super_user_role]
    )

    db.session.commit()

    print '<admin user %s %s add in database>' %(first_name, last_name)

if __name__ == '__main__':
    manager.run()