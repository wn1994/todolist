from flask import render_template
from . import api
from flask import request, make_response, redirect, url_for, jsonify


@api.route('/')
def index():
    return render_template('index.html')


@api.route('user/<int:phone_id>',methods=['POST','GET','PUT','DELETE'])
def user(phone_id):
    if request.method == 'GET':
        pass