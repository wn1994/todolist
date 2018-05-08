#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from werkzeug.utils import import_string
import default_config
from .models import db

blueprints = [
    'app.modules.api:api',
    'app.modules.todolist:todolist'
]


def create_app(config=None):
    app = Flask(__name__)
    configure_app(app, config)
    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    with app.app_context():
        # db.drop_all()
        # db.create_all()
        pass

    # load blueprints
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    return app


def configure_app(app, config):
    app.config.from_object(default_config.BaseConfig)

    # if not config:
    #     config = default_config.config_map['dev']
    # app.config.from_object(config)
    app.config.from_pyfile('config.py')
    # print(app.config)
