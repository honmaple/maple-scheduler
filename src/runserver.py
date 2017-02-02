#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: runserver.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-02-02 09:18:53 (CST)
# Last Update:星期四 2017-2-2 13:2:51 (CST)
#          By:
# Description:
# **************************************************************************
from flask_apscheduler import scheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from scheduler import create_app


class Config(object):
    DEBUG = True
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
    SCHEDULER_TIMEZONE = 'UTC'

    SCHEDULER_API_ENABLED = True
    JSON_AS_ASCII = False


app = create_app(Config())


def hello():
    '''
    输出时间
    '''
    from time import time
    print(time())


a = scheduler.add_job(hello, trigger='interval', seconds=10, id='3')
print(a)

if __name__ == '__main__':
    app.run()
    print(app.url_map)
