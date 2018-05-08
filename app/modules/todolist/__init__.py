#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

todolist = Blueprint('todolist', __name__)

from . import routes
