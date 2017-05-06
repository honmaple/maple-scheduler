#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: runserver.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-02-02 09:18:53 (CST)
# Last Update:星期六 2017-5-6 21:47:24 (CST)
#          By:
# Description:
# **************************************************************************
from scheduler import scheduler
from scheduler.utils import HTTPResponse
from flask import Flask
from flask_cors import CORS
from importlib import import_module
from inspect import getmembers, isfunction, getargspec


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


app = create_app('config')


@app.route('/jobs')
def job():
    data = [{
        'name': 'jobs:{}'.format(f[1].__name__),
        'doc': f[1].__doc__
    } for f in getmembers(import_module('jobs'), isfunction)]
    return HTTPResponse(HTTPResponse.NORMAL_STATUS, data=data).to_response()


def hello():
    '''
    输出时间
    '''
    from time import time
    print(time())


from apscheduler.jobstores.base import ConflictingIdError
try:
    a = scheduler.add_job(hello, trigger='interval', seconds=10, id='3')
except ConflictingIdError as e:
    print(e)

if __name__ == '__main__':
    app.run()
