#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-02-02 12:49:07 (CST)
# Last Update:星期四 2017-2-16 11:42:52 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Flask
from flask_apscheduler import scheduler
from flask_cors import CORS


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register(app)
    CORS(app)
    return app


def register(app):
    register_extension(app)


def register_extension(app):
    scheduler.init_app(app)
    scheduler.start()
