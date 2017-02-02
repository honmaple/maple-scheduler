#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: api.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-11 16:05:44 (CST)
# Last Update:星期四 2017-2-2 16:7:42 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request
from flask.views import MethodView
from apscheduler.jobstores.base import ConflictingIdError, JobLookupError
from . import scheduler
from .utils import HTTPResponse, Serializer


class SchedulerPauseView(MethodView):
    def post(self):
        """Pauses scheduler."""
        scheduler.pause_job()
        data = {'running': scheduler.running}
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=data).to_response()


class SchedulerResumeView(MethodView):
    def post(self):
        """Resumes scheduler."""
        scheduler.resume_job()
        data = {'running': scheduler.running}
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=data).to_response()


class SchedulerRunView(MethodView):
    def post(self):
        """Executes scheduler."""
        scheduler.start(paused=True)
        data = {'running': scheduler.running}
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=data).to_response()


class JobPauseView(MethodView):
    def post(self, pk):
        """Pauses a job."""
        try:
            scheduler.pause_job(pk)
            job = scheduler.get_job(pk)
            serializer = Serializer(job)
            return HTTPResponse(
                HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()
        except JobLookupError:
            msg = 'Job ID %s not found' % pk
            return HTTPResponse(
                HTTPResponse.JOB_NOT_FOUND, description=msg).to_response()
        except Exception as e:
            msg = str(e)
            return HTTPResponse(
                HTTPResponse.OTHER_ERROR, description=msg).to_response()


class JobResumeView(MethodView):
    def post(self, pk):
        """Resumes a job."""
        try:
            scheduler.resume_job(pk)
            job = scheduler.get_job(pk)
            serializer = Serializer(job)
            return HTTPResponse(
                HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()
        except JobLookupError:
            msg = 'Job ID %s not found' % pk
            return HTTPResponse(
                HTTPResponse.JOB_NOT_FOUND, description=msg).to_response()
        except Exception as e:
            msg = str(e)
            return HTTPResponse(
                HTTPResponse.OTHER_ERROR, description=msg).to_response()


class JobRunView(MethodView):
    def post(self, pk):
        """Executes a job."""
        try:
            scheduler.run_job(pk)
            job = scheduler.get_job(pk)
            serializer = Serializer(job)
            return HTTPResponse(
                HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()
        except JobLookupError:
            msg = 'Job ID %s not found' % pk
            return HTTPResponse(
                HTTPResponse.JOB_NOT_FOUND, description=msg).to_response()
        except Exception as e:
            msg = str(e)
            return HTTPResponse(
                HTTPResponse.OTHER_ERROR, description=msg).to_response()


class SchedulerListView(MethodView):
    def get(self):
        jobs = scheduler.get_jobs()
        serializer = Serializer(jobs)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def post(self):
        '''
        :param id:job id
        :param trigger:date or interval or crontab
        :param job:if job is None,the default func is http_request
        '''
        post_data = request.json
        job = post_data.pop('job', None)
        func = post_data.get('func', None)
        if func is not None and not scheduler.func_rule(func):
            return HTTPResponse(HTTPResponse.FORBIDDEN).to_response()
        try:
            job = scheduler.add_job(**post_data)
            serializer = Serializer(job)
            return HTTPResponse(
                HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()
        except ConflictingIdError:
            msg = 'Job ID %s is exists' % post_data.get('id')
            return HTTPResponse(
                HTTPResponse.JOB_ALREADY_EXISTS, description=msg).to_response()
        except Exception as e:
            msg = str(e)
            return HTTPResponse(
                HTTPResponse.OTHER_ERROR, description=msg).to_response()


class SchedulerView(MethodView):
    def get(self, pk):
        job = scheduler.get_job(pk)
        if not job:
            msg = 'Job ID %s not found' % pk
            return HTTPResponse(
                HTTPResponse.JOB_NOT_FOUND, description=msg).to_response()
        serializer = Serializer(job)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def put(self, pk):
        post_data = request.json
        try:
            scheduler.modify_job(pk, **post_data)
            job = scheduler.get_job(pk)
            serializer = Serializer(job)
            return HTTPResponse(
                HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()
        except JobLookupError:
            msg = 'Job ID %s not found' % pk
            return HTTPResponse(
                HTTPResponse.JOB_NOT_FOUND, description=msg).to_response()
        except Exception as e:
            msg = str(e)
            return HTTPResponse(
                HTTPResponse.OTHER_ERROR, description=msg).to_response()

    def delete(self, pk):
        try:
            scheduler.remove_job(pk)
            msg = 'Job ID %s delete success' % pk
            return HTTPResponse(
                HTTPResponse.NORMAL_STATUS, description=msg).to_response()
        except JobLookupError:
            msg = 'Job ID %s not found' % pk
            return HTTPResponse(
                HTTPResponse.JOB_NOT_FOUND, description=msg).to_response()
        except Exception as e:
            msg = str(e)
            return HTTPResponse(
                HTTPResponse.OTHER_ERROR, description=msg).to_response()
