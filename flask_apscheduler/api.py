#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: api.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-11 16:05:44 (CST)
# Last Update:星期四 2016-12-15 17:23:23 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request
from flask.views import MethodView
from flask_apscheduler import scheduler


class DateListView(MethodView):
    def get(self):
        pass

    def post(self):
        post_data = request.get_json()
        id = post_data.pop('id', None)
        date = post_data.pop('date', None)
        task = post_data.pop('task', None)
        kwargs = dict(func='s', trigger='date', run_date=date, kwargs=task)
        if id is not None:
            id = str(id)
            kwargs.update(id=id)
            if scheduler.get_job(id) is not None:
                msg = u'任务ID:%s 已存在' % id
                return msg
        scheduler.add_job(**kwargs)
        return 'success'


class DateView(MethodView):
    def get(self):
        pass
