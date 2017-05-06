#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: config.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-05-06 18:48:44 (CST)
# Last Update:星期六 2017-5-6 21:33:37 (CST)
#          By:
# Description:
# **************************************************************************
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from pytz import timezone

DEBUG = True
JSON_AS_ASCII = False

SCHEDULER_JOBSTORES = {'default': SQLAlchemyJobStore(url='sqlite:///test.db')}

SCHEDULER_EXECUTORS = {'default': {'type': 'threadpool', 'max_workers': 20}}

SCHEDULER_JOB_DEFAULTS = {'coalesce': False, 'max_instances': 3}
SCHEDULER_TIMEZONE = timezone('Asia/Shanghai')

SCHEDULER_API_ENABLED = True
SCHEDULER_API_RULE = [lambda func: True, ]
