#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: apscheduler.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-10 11:10:36 (CST)
# Last Update:星期四 2016-12-15 17:23:1 (CST)
#          By:
# Description:
# **************************************************************************
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerAlreadyRunningError
from sqlalchemy.orm import sessionmaker


class APScheduler(object):
    def __init__(self, app=None, scheduler=None):
        self.scheduler = scheduler or BackgroundScheduler()
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.scheduler = app.config.setdefault('SCHEDULER', self.scheduler)
        self.jobstores = app.config.setdefault('SCHEDULER_JOBSTORES', None)
        self.executors = app.config.setdefault('SCHEDULER_EXECUTORS', None)
        self.job_defaults = app.config.setdefault('SCHEDULER_JOB_DEFAULTS',
                                                  None)
        self.timezone = app.config.setdefault('SCHEDULER_TIMEZONE', None)

        assert self.jobstores is not None
        assert self.executors is not None
        assert self.job_defaults is not None
        assert self.timezone is not None
        self.scheduler.configure(
            jobstores=self.jobstores,
            executors=self.executors,
            job_defaults=self.job_defaults,
            timezone=self.timezone)

    def query(self, table='jobs_t', jobstore='default'):
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
        except SchedulerAlreadyRunningError:
            pass

    def __getattr__(self, name):
        return getattr(self.scheduler, name)


scheduler = APScheduler()
