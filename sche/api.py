#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: api.py
# Author: jianglin
# Email: mail@honmaple.com
# Created: 2016-11-11 16:05:44 (CST)
# Last Update: Sunday 2018-09-30 17:50:04 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request
from flask import Blueprint
from flask.views import MethodView
from apscheduler.jobstores.base import ConflictingIdError, JobLookupError
from sche import sche
from .utils import HTTP, Serializer
import json


class ScheView(MethodView):
    def get(self):
        ins = sche.status()
        return HTTP.OK(data=ins)

    def post(self):
        """start scheduler."""
        if not sche.running:
            sche.start(paused=True)
        ins = sche.status()
        return HTTP.OK(data=ins)

    def delete(self):
        """shutdown scheduler."""
        if sche.running:
            sche.resume()
        ins = sche.status()
        return HTTP.OK(data=ins)


class ScheJobView(MethodView):
    def get(self):
        request_data = request.args.to_dict()
        trigger = request_data.get('trigger')
        jobs = sche.get_jobs()
        ins = Serializer(jobs, trigger=trigger).data
        return HTTP.OK(data=ins)

    def post(self):
        '''
        :param trigger:date or interval or crontab
        :param job:if job is None,the default func is http_request
        '''
        request_data = request.get_json()
        trigger = request_data.get('trigger')
        kwargs = request_data.get('kwargs')
        if trigger == 'interval' and kwargs:
            request_data['kwargs'] = json.loads(kwargs)
        try:
            job = sche.add_job(**request_data)
            ins = Serializer(job).data
            return HTTP.OK(data=ins)
        except ConflictingIdError:
            msg = 'Job ID %s is exists' % request_data.get('id')
            return HTTP.BAD_REQUEST(message=msg)
        except Exception as e:
            msg = str(e)
            return HTTP.SERVER_ERROR(message=msg)

    def put(self):
        request_data = request.get_json()
        job_ids = request_data.pop('jobs', [])
        success_ids = []
        for pk in job_ids:
            try:
                sche.remove_job(pk)
                msg = 'Job ID %s delete success' % pk
                success_ids.append(pk)
            except JobLookupError:
                msg = 'Job ID %s not found' % pk
                return HTTP.BAD_REQUEST(message=msg)
            except Exception as e:
                msg = str(e)
                return HTTP.SERVER_ERROR(message=msg)
        msg = '{} delete success!'.format(','.join(success_ids))
        return HTTP.OK(data=success_ids, message=msg)


class ScheJobItemView(MethodView):
    def get(self, pk):
        job = sche.get_job(pk)
        if not job:
            msg = 'Job ID %s not found' % pk
            return HTTP.BAD_REQUEST(message=msg)
        ins = Serializer(job).data
        return HTTP.OK(data=ins)

    def put(self, pk):
        request_data = request.get_json()
        try:
            sche.modify_job(pk, **request_data)
            job = sche.get_job(pk)
            ins = Serializer(job).data
            return HTTP.OK(data=ins)
        except JobLookupError:
            msg = 'Job ID %s not found' % pk
            return HTTP.BAD_REQUEST(message=msg)
        except Exception as e:
            msg = str(e)
            return HTTP.SERVER_ERROR(message=msg)

    def delete(self, pk):
        try:
            sche.remove_job(pk)
            msg = 'Job ID %s delete success' % pk
            return HTTP.OK(message=msg)
        except JobLookupError:
            msg = 'Job ID %s not found' % pk
            return HTTP.BAD_REQUEST(message=msg)
        except Exception as e:
            msg = str(e)
            return HTTP.SERVER_ERROR(message=msg)


class ScheJobPauseView(MethodView):
    def post(self, pk):
        """Pauses a job."""
        try:
            sche.pause_job(pk)
            job = sche.get_job(pk)
            ins = Serializer(job).data
            return HTTP.OK(data=ins)
        except JobLookupError:
            msg = 'Job ID %s not found' % pk
            return HTTP.BAD_REQUEST(message=msg)
        except Exception as e:
            msg = str(e)
            return HTTP.SERVER_ERROR(message=msg)


class ScheJobResumeView(MethodView):
    def post(self, pk):
        """Resumes a job."""
        try:
            sche.resume_job(pk)
            job = sche.get_job(pk)
            ins = Serializer(job).data
            return HTTP.OK(data=ins)
        except JobLookupError:
            msg = 'Job ID %s not found' % pk
            return HTTP.BAD_REQUEST(message=msg)
        except Exception as e:
            msg = str(e)
            return HTTP.SERVER_ERROR(message=msg)


class ScheJobExecuteView(MethodView):
    def post(self, pk):
        """Executes a job."""
        try:
            sche.run_job(pk)
            job = sche.get_job(pk)
            ins = Serializer(job).data
            return HTTP.OK(data=ins)
        except JobLookupError:
            msg = 'Job ID %s not found' % pk
            return HTTP.BAD_REQUEST(message=msg)
        except Exception as e:
            msg = str(e)
            return HTTP.SERVER_ERROR(message=msg)


def init_app(app, url_prefix='/api/scheduler'):
    site = Blueprint('sche', __name__, url_prefix=url_prefix)

    sche_endpoint = [
        ("/status", ScheView.as_view('status')),
        ("", ScheJobView.as_view('job')),
        ("/<pk>", ScheJobItemView.as_view('job_item')),
        ('/<pk>/pause', ScheJobPauseView.as_view('job_pause')),
        ('/<pk>/resume', ScheJobResumeView.as_view('job_resume')),
        ('/<pk>/execute', ScheJobExecuteView.as_view('job_execute')),
    ]

    for url, endpoint in sche_endpoint:
        site.add_url_rule(
            url,
            view_func=endpoint,
        )
    app.register_blueprint(site)
