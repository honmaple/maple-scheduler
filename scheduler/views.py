#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: api.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-11 16:05:44 (CST)
# Last Update:星期五 2017-5-19 21:8:36 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request
from flask.views import MethodView
from apscheduler.jobstores.base import ConflictingIdError, JobLookupError
from . import scheduler
from .utils import HTTPResponse, Serializer
from json import loads


class SchedulerStatusView(MethodView):
    def get(self):
        """get scheduler."""
        serializer = Serializer(scheduler, scheduler=True)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def post(self):
        """start scheduler."""
        post_data = request.json
        pause = post_data.pop('pause', False)
        if pause in [1, '1', 'true', 'True']:
            pause = True
        else:
            pause = False
        scheduler.start(pause)
        serializer = Serializer(scheduler, scheduler=True)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def delete(self):
        """shutdown scheduler."""
        if scheduler.running:
            scheduler.shutdown()
        serializer = Serializer(scheduler, scheduler=True)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()


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


class JobExecuteView(MethodView):
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
        query_dict = request.args.to_dict()
        trigger = query_dict.pop('trigger', None)
        jobs = scheduler.get_jobs()
        serializer = Serializer(jobs, trigger=trigger)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def post(self):
        '''
        :param trigger:date or interval or crontab
        :param job:if job is None,the default func is http_request
        '''
        post_data = request.json
        func = post_data.get('func', None)
        trigger = post_data.get('trigger')
        kwargs = post_data.get('kwargs')
        if trigger == 'interval' and kwargs:
            post_data['kwargs'] = loads(kwargs)
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

    def put(self):
        post_data = request.json
        job_ids = post_data.pop('jobs', [])
        success_ids = []
        for pk in job_ids:
            try:
                scheduler.remove_job(pk)
                msg = 'Job ID %s delete success' % pk
                success_ids.append(pk)
            except JobLookupError:
                msg = 'Job ID %s not found' % pk
                return HTTPResponse(
                    HTTPResponse.JOB_NOT_FOUND, description=msg).to_response()
            except Exception as e:
                msg = str(e)
                return HTTPResponse(
                    HTTPResponse.OTHER_ERROR, description=msg).to_response()
        msg = '{} delete success!'.format(','.join(success_ids))
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, description=msg).to_response()


class SchedulerView(MethodView):
    def get(self, pk):
        job = scheduler.get_job(pk)
        print(dir(job))
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
