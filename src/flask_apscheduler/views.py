#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: api.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-11 16:05:44 (CST)
# Last Update:星期四 2017-2-2 13:19:22 (CST)
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
            msg = 'Job %s not found' % pk
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
            msg = 'Job %s not found' % pk
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
            msg = 'Job %s not found' % pk
            return HTTPResponse(
                HTTPResponse.JOB_NOT_FOUND, description=msg).to_response()
        except Exception as e:
            msg = str(e)
            return HTTPResponse(
                HTTPResponse.OTHER_ERROR, description=msg).to_response()


class DateListView(MethodView):
    def get(self):
        jobs = scheduler.get_jobs()
        serializer = Serializer(jobs)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def post(self):
        data = request.json()
        trigger = data.pop('trigger', 'date')
        try:
            job = scheduler.add_job(trigger=trigger, **data)
            serializer = Serializer(job)
            return HTTPResponse(
                HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()
        except ConflictingIdError:
            msg = 'Job %s is exists' % data.get('id')
            return HTTPResponse(
                HTTPResponse.JOB_ALREADY_EXISTS, description=msg).to_response()
        except Exception as e:
            return HTTPResponse(
                HTTPResponse.OTHER_ERROR, description=e).to_response()


class DateView(MethodView):
    def get(self, pk):
        job = scheduler.get_job(pk)
        if not job:
            msg = 'Job %s not found' % pk
            return HTTPResponse(
                HTTPResponse.JOB_NOT_FOUND, description=msg).to_response()
        serializer = Serializer(job)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def put(self, pk):
        data = request.get_json()
        try:
            scheduler.modify_job(pk, **data)
            job = scheduler.get_job(pk)
            serializer = Serializer(job)
            return HTTPResponse(
                HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()
        except JobLookupError:
            msg = 'Job %s not found' % pk
            return HTTPResponse(
                HTTPResponse.JOB_NOT_FOUND, description=msg).to_response()
        except Exception as e:
            return HTTPResponse(
                HTTPResponse.OTHER_ERROR, description=e).to_response()

    def delete(self, pk):
        try:
            job = scheduler.delete_job(pk)
            serializer = Serializer(job)
            return HTTPResponse(
                HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()
        except JobLookupError:
            msg = 'Job %s not found' % pk
            return HTTPResponse(
                HTTPResponse.JOB_NOT_FOUND, description=msg).to_response()
        except Exception as e:
            return HTTPResponse(
                HTTPResponse.OTHER_ERROR, description=e).to_response()

# class IntervalListView(MethodView):
#     def get(self):
#         pass

#     def post(self):
#         post_data = request.get_json()
#         id = post_data.pop('id', None)
#         date = post_data.pop('date', None)
#         task = post_data.pop('task', None)
#         kwargs = dict(func='s', trigger='date', run_date=date, kwargs=task)
#         if id is not None:
#             id = str(id)
#             kwargs.update(id=id)
#             if scheduler.get_job(id) is not None:
#                 msg = u'任务ID:%s 已存在' % id
#                 return msg

#         scheduler.add_job(**kwargs)
#         return 'success'

# class IntervalView(MethodView):
#     def get(self, pk):
#         pass

#     def put(self, pk):
#         pass

#     def delete(self, pk):
#         pass
