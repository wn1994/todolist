#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from datetime import datetime
from functools import wraps


def exception_wrap(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            return False
        else:
            return True

    return decorator


class User(db.Model):
    __table__args = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    phone_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    password = db.Column(db.String(32), nullable=False)
    age = db.Column(db.Integer)
    reg_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    email = db.Column(db.String(128))

    def __init__(self, phone_id, password, name='', age=0, email=''):
        self.phone_id = phone_id
        self.password = password
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name

    @exception_wrap
    def save(self):
        db.session.add(self)
        db.session.commit()

    @exception_wrap
    def update(self):
        db.session.commit()


class Item(db.Model):
    __table__args = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    phone_id = db.Column(db.Integer, db.ForeignKey('user.phone_id'))
    done_tag = db.Column(db.Integer, default=0)
    user = db.relationship('User', backref='content')

    def __init__(self, content, user, done_tag=0):
        self.content = content
        self.done_tag = done_tag
        self.user = user

    def __repr__(self):
        return '<User %r>' % self.id

    @exception_wrap
    def save(self):
        db.session.add(self)
        db.session.commit()

    @exception_wrap
    def update(self):
        db.session.commit()

    @exception_wrap
    def delete(self):
        db.session.delete(self)
        db.session.commit()
