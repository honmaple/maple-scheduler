#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: mail@honmaple.com
# Created: 2016-11-10 11:10:36 (CST)
# Last Update: Sunday 2018-09-30 17:50:05 (CST)
#          By:
# Description:
# **************************************************************************
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerAlreadyRunningError
from inspect import getmembers, isfunction
from importlib import import_module

DEFAULT_CONFIG = {
    'scheduler': BackgroundScheduler(),
    'jobstores': None,
    'executors': None,
    'job_defaults': None,
    'timezone': 'UTC',
    "funcs": []
}


class APScheduler(object):
    def __init__(self, app=None, scheduler=None):
        self.scheduler = scheduler or BackgroundScheduler()
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('APSCHEDULER', DEFAULT_CONFIG)
        config = app.config['APSCHEDULER']
        config.setdefault('scheduler', DEFAULT_CONFIG['scheduler'])
        config.setdefault('jobstores', DEFAULT_CONFIG['jobstores'])
        config.setdefault('executors', DEFAULT_CONFIG['executors'])
        config.setdefault('job_defaults', DEFAULT_CONFIG['job_defaults'])
        config.setdefault('timezone', DEFAULT_CONFIG['timezone'])
        config.setdefault('funcs', DEFAULT_CONFIG['funcs'])

        self.scheduler = config['scheduler']
        self.jobstores = config['jobstores']
        self.executors = config['executors']
        self.job_defaults = config['job_defaults']
        self.timezone = config['timezone']
        self.funcs = config['funcs']

        assert self.jobstores is not None
        assert self.executors is not None
        assert self.job_defaults is not None
        assert self.timezone is not None

        self.scheduler.configure(
            jobstores=self.jobstores,
            executors=self.executors,
            job_defaults=self.job_defaults,
            timezone=self.timezone)

        if isinstance(self.funcs, str):
            self.funcs = [{
                'name': '{0}:{1}'.format(self.funcs, f[1].__name__),
                'doc': f[1].__doc__,
            } for f in getmembers(import_module(self.funcs), isfunction)]

    def start(self, paused=False):
        try:
            self.scheduler.start(paused)
        except SchedulerAlreadyRunningError as e:
            print(e)

    def run_job(self, id, jobstore=None):
        job = self.scheduler.get_job(id, jobstore)

        if not job:
            raise LookupError(id)

        job.func(*job.args, **job.kwargs)

    def status(self):
        return {
            'running': self.running,
            'executors': self.executors,
            'job_defaults': self.job_defaults,
            'funcs': self.funcs
        }

    def __getattr__(self, name):
        return getattr(self.scheduler, name)


sche = APScheduler()


def init_app(app, start=True):
    sche.init_app(app)
    if start:
        sche.start()


def add_job(*args, **kwagrs):
    sche.add_job(*args, **kwagrs)
