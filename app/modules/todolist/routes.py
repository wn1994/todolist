#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from flask import (current_app, jsonify, redirect, render_template, request,
                   url_for)

from response import (add_content_response, delete_content_response,
                      get_all_contents_response, get_content_response,
                      get_info_response, signin_response, signup_response,
                      update_content_response, update_info_response)

from . import todolist


@todolist.route('/', methods=['GET'])
def index():
    """首页显示用户所有的todolist"""
    phone_id = request.cookies.get('phone_id', '')
    return get_all_contents_response(phone_id)


@todolist.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return signup_response()
    else:
        return render_template('signup.html')


@todolist.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        return signin_response()
    else:
        return render_template('signin.html')


@todolist.route('/user/<int:phone_id>/content', methods=['POST', 'GET'])
def user_content_1(phone_id):
    """todo条目添加,查询当前用户所有条目"""
    if request.method == 'POST':
        return add_content_response(phone_id)
    else:
        return get_all_contents_response(phone_id)


@todolist.route('/user/<int:phone_id>/content/<int:content_id>', methods=['GET', 'PUT', 'DELETE'])
def user_content_2(phone_id, content_id=None):
    """todo条目改查删"""
    if request.method == 'PUT':
        return update_content_response(phone_id, content_id)
    elif request.method == 'DELETE':
        return delete_content_response(phone_id, content_id)
    else:
        return get_content_response(phone_id, content_id)


@todolist.route('/user/<int:phone_id>/info', methods=['PUT', 'GET'])
def user_info(phone_id):
    """用户信息改查"""
    if request.method == 'PUT':
        return update_info_response(phone_id)
    else:
        return get_info_response(phone_id)
