# !/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-02-02 09:27:13 (CST)
# Last Update:星期四 2017-2-2 17:20:39 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import SchedulerStatusView, SchedulerListView, SchedulerView
from .views import JobPauseView, JobResumeView, JobExecuteView

site = Blueprint('scheduler', __name__, url_prefix='/scheduler')

site.add_url_rule('', view_func=SchedulerListView.as_view('scheduler_list'))
site.add_url_rule('/<pk>', view_func=SchedulerView.as_view('scheduler'))
site.add_url_rule(
    '/status', view_func=SchedulerStatusView.as_view('scheduler_status'))
site.add_url_rule('/<pk>/pause', view_func=JobPauseView.as_view('pause'))
site.add_url_rule('/<pk>/resume', view_func=JobResumeView.as_view('resume'))
site.add_url_rule('/<pk>/execute', view_func=JobExecuteView.as_view('run'))
