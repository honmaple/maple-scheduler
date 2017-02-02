#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: test.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-02-02 09:36:16 (CST)
# Last Update:星期四 2017-2-2 9:45:15 (CST)
#          By:
# Description:
# **************************************************************************
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask
from flask_apscheduler import APScheduler


class Config(object):
    JOBS = [
        {
            'id': 'vvvv',
            'func': 'test:job1',
            'args': (55, 66),
            'trigger': 'interval',
            'seconds': 2
        }
    ]

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///test.db')
    }

    SCHEDULER_EXECUTORS = {
        'default': {
            'type': 'threadpool',
            'max_workers': 20
        }
    }

    SCHEDULER_JOB_DEFAULTS = {'coalesce': False, 'max_instances': 3}

    SCHEDULER_API_ENABLED = True


def job1(a, b):
    print(str(a) + ' ' + str(b))


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run()
