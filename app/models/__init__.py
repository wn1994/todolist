#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# 这里一定要把所有表都导入db所在的文件,或者是db.create_all()所在的文件里,不然drop_all()和create_all()都没有效果
from .tables import User, Item


def new_user_info(**kwargs):
    phone_id = kwargs.get('phone_id', '')
    password = kwargs.get('password', '')
    if User.query.filter_by(phone_id=phone_id).first():
        # phone_id is already exists.
        return -1
    if phone_id and password:
        user = User(phone_id, password)
        user.save()
        return 1
    else:
        # Invalid phone_id or password.
        return -2


# def update_user_info(user, **kwargs):
#     for key, value in kwargs.iteritems():
#         user.key = value
#     user.update()


def get_user(phone_id):
    user = User.query.filter_by(phone_id=phone_id).first()
    return user


def set_content(phone_id, content):
    user = User.query.filter_by(phone_id=phone_id).first()
    item = Item(content, user)
    result = item.save()

    return item.id if result else False

def get_content_by_user(phone_id):
    items = Item.query.filter_by(phone_id=phone_id).all()
    return items


def get_content_by_id(id):
    item = Item.query.filter_by(id=id).first()
    return item


def is_in(**kwargs):
    phone_id = kwargs.get('phone_id', '')
    password = kwargs.get('password', '')
    if User.query.filter_by(phone_id=phone_id, password=password).first():
        return True
    else:
        return False
