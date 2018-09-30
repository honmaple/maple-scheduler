#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: config.py
# Author: jianglin
# Email: mail@honmaple.com
# Created: 2017-05-06 18:48:44 (CST)
# Last Update: Sunday 2018-09-30 17:50:05 (CST)
#          By:
# Description:
# **************************************************************************
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from pytz import timezone

DEBUG = True
JSON_AS_ASCII = False

APSCHEDULER = {
    'jobstores': {
        'default': SQLAlchemyJobStore(url='sqlite:///test_scheduler.db')
    },
    'executors': {
        'default': {
            'type': 'threadpool',
            'max_workers': 20
        }
    },
    'job_defaults': {
        'coalesce': False,
        'max_instances': 3
    },
    'timezone': timezone('Asia/Shanghai'),
    'funcs': "jobs"
}
