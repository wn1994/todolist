#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from flask import request, jsonify, redirect, url_for, current_app, flash, render_template
from app.models import new_user_info, get_user, get_content_by_id, get_content_by_user, is_in, \
    set_content
from functools import wraps


def check_login(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            current_phone_id = int(request.cookies.get('phone_id', ''))
            is_login = request.cookies.get('is_login', '')
            # args第一个为phone_id,第二个为content_id
            phone_id = kwargs.get('phone_id', '') or args[0]
            phone_id = int(phone_id)
        except:
            print('==========================decorator error===============')
            return redirect(url_for('.signin'))
        else:
            if current_phone_id == phone_id and is_login == 'yes':
                return func(*args, **kwargs)
            else:
                return redirect(url_for('.signin'))

    return decorator


def signup_response():
    phone_id = request.form.get('phone_id', '')
    password = request.form.get('password', '')
    result = new_user_info(phone_id=int(phone_id), password=password)
    if result == -1:
        return jsonify(ask='false', error='phone_id is already exists')
    elif result == -2:
        return jsonify(ask='false', error='Invalid phone_id or password')
    else:
        return jsonify(res_code=201)


def signin_response():
    phone_id = request.form.get('phone_id', '')
    password = request.form.get('password', '')
    result = is_in(phone_id=phone_id, password=password)
    if result:
        response = current_app.make_response(get_all_contents(phone_id))
        expires = datetime.datetime.now() + datetime.timedelta(days=365)
        response.set_cookie('phone_id', phone_id, expires=expires)
        response.set_cookie('is_login', 'yes', expires=expires)
    else:
        response = jsonify(ask='false', error='Invalid phone_id or password')
    return response


def get_all_contents(phone_id):
    contents = []
    items = get_content_by_user(phone_id)
    for item in items:
        content = item.content
        done_tag = item.done_tag
        content_id = item.id
        phone_id = item.phone_id
        contents.append(dict(phone_id=phone_id, content_id=content_id, content=content, done_tag=done_tag))
    result = jsonify(res_code=201, items=contents)
    result = eval(result.data)
    return render_template('index.html', result=result)


@check_login
def get_all_contents_response(phone_id):
    return get_all_contents(phone_id)


@check_login
def update_info_response(phone_id):
    req = request.get_json()
    password = req.get('password', '')
    if not password:
        return jsonify('password can not be empty')
    user = get_user(phone_id)
    user.password = password
    user.name = req.get('name', '')
    user.age = req.get('age', '')
    user.email = req.get('email', '')
    result = user.update()
    if result:
        return jsonify(name=user.name, age=user.age, email=user.email, )
    # return jsonify('success') if result else jsonify('failure')


@check_login
def get_info_response(phone_id):
    user = get_user(phone_id)
    if not user:
        return render_template('404.html')
    else:
        result = jsonify(data=dict(name=user.name, age=user.age, email=user.email), res_code=201)
        result = eval(result.data)
        return render_template('user.html', result=result)


@check_login
def add_content_response(phone_id):
    content = request.form.get('content', '')
    result = set_content(phone_id, content)
    return jsonify(
        {
            "res_code": 201,
            "res_content_id": result
        }
    ) if result else jsonify('failure')


@check_login
def delete_content_response(phone_id, content_id):
    item = get_content_by_id(content_id)
    result = item.delete()
    return jsonify('success') if result else jsonify('failure')


@check_login
def update_content_response(phone_id, content_id):
    item = get_content_by_id(content_id)
    req = request.get_json()
    content = req.get('content', '')
    # 可能涉及到单独改内容
    if content:
        item.content = content
    done_tag = int(req.get('done_tag', -1))
    if done_tag == 0 or done_tag == 1:
        item.done_tag = done_tag
    result = item.update()
    if result:
        return jsonify(content=item.content, done_tag=item.done_tag)
    # return jsonify('success') if result else jsonify('failure')


@check_login
def get_content_response(phone_id, content_id):
    item = get_content_by_id(content_id)
    if not item:
        return render_template('404.html')
    result = jsonify(data=dict(content=item.content, done_tag=item.done_tag),
                     res_code=201) if item.phone_id == phone_id else 404
    if result == 404:
        return render_template('404.html')
    # 这里先jsonify再eval没有必要,现在这么写只是为了练习直接返回json和返回一个html
    result = eval(result.data)
    return render_template('content.html', result=result)
