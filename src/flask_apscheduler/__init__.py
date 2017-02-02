#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: apscheduler.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-10 11:10:36 (CST)
# Last Update:星期四 2017-2-2 16:58:41 (CST)
#          By:
# Description:
# **************************************************************************
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerAlreadyRunningError

DEFAULT_CONFIG = {
    'scheduler': BackgroundScheduler(),
    'jobstores': None,
    'executors': None,
    'job_defaults': None,
    'timezone': 'UTC'
}


class APScheduler(object):
    def __init__(self, app=None, scheduler=None):
        self.scheduler = scheduler or BackgroundScheduler()
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        config = DEFAULT_CONFIG
        self.scheduler = app.config.setdefault('SCHEDULER',
                                               config['scheduler'])
        self.jobstores = app.config.setdefault('SCHEDULER_JOBSTORES',
                                               config['jobstores'])
        self.executors = app.config.setdefault('SCHEDULER_EXECUTORS',
                                               config['executors'])
        self.job_defaults = app.config.setdefault('SCHEDULER_JOB_DEFAULTS',
                                                  config['job_defaults'])
        self.timezone = app.config.setdefault('SCHEDULER_TIMEZONE',
                                              config['timezone'])
        self.api_func_rule = app.config.setdefault('SCHEDULER_API_RULE', False)
        api_enabled = app.config.setdefault('SCHEDULER_API_ENABLED', True)

        assert self.jobstores is not None
        assert self.executors is not None
        assert self.job_defaults is not None
        assert self.timezone is not None
        self.scheduler.configure(
            jobstores=self.jobstores,
            executors=self.executors,
            job_defaults=self.job_defaults,
            timezone=self.timezone)
        if api_enabled:
            self.register_api(app)

    def func_rule(self, func):
        rule = self.api_func_rule
        if isinstance(rule, list):
            return self.func_rule_list(rule, func)
        elif callable(rule):
            return rule(func)
        return rule

    def func_rule_list(self, rules, func):
        for rule in rules:
            self.api_func_rule = rule
            if not self.func_rule(func):
                return False
        return True

    def query(self, table='jobs_t', jobstore='default'):
        from sqlalchemy.orm import sessionmaker
        jobstore = self.jobstores.get(jobstore)
        if jobstore is None:
            raise ValueError('%s is not exist' % jobstore)
        table = getattr(jobstore, table)
        engine = jobstore.engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        return session.query(table)

    def start(self, paused=False):
        try:
            self.scheduler.start(paused)
        except SchedulerAlreadyRunningError as e:
            pass

    def shutdown(self, wait=True):
        self.scheduler.shutdown(wait)

    def run_job(self, id, jobstore=None):
        job = self.scheduler.get_job(id, jobstore)

        if not job:
            raise LookupError(id)

        job.func(*job.args, **job.kwargs)

    def register_api(self, app):
        from .urls import site
        app.register_blueprint(site)

    def __getattr__(self, name):
        return getattr(self.scheduler, name)


scheduler = APScheduler()
