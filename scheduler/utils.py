#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: utils.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-02-02 12:24:45 (CST)
# Last Update:星期四 2017-2-2 16:53:41 (CST)
#          By:
# Description:
# **************************************************************************
from flask import jsonify


class HTTPResponse(object):
    NORMAL_STATUS = '200'
    JOB_ALREADY_EXISTS = '600'
    JOB_NOT_FOUND = '601'

    FORBIDDEN = '403'
    OTHER_ERROR = '500'

    STATUS_DESCRIPTION = {
        NORMAL_STATUS: 'normal',
        FORBIDDEN: 'You have no permission!',
        JOB_ALREADY_EXISTS: 'Job already exists.',
        JOB_NOT_FOUND: 'Job not found',
        OTHER_ERROR: 'other error'
    }

    def __init__(self,
                 status='200',
                 message='',
                 data=None,
                 description='',
                 pageinfo=None):
        self.status = status
        self.message = message or self.STATUS_DESCRIPTION.get(status)
        self.data = data
        self.description = description
        self.pageinfo = pageinfo

    def to_dict(self):
        response = {
            'status': self.status,
            'message': self.message,
            'data': self.data,
            'description': self.description,
        }
        if self.pageinfo is not None:
            response.update(pageinfo=self.pageinfo.as_dict())
        return response

    def to_response(self):
        response = self.to_dict()
        return jsonify(response)


class Serializer(object):
    def __init__(self, instance, scheduler=False):
        self.instance = instance
        self.scheduler = scheduler

    @property
    def data(self):
        if isinstance(self.instance, list):
            return self._serializerlist(self.instance)
        return self._serializer(self.instance)

    def _serializerlist(self, instances):
        return [self._serializer(i) for i in instances]

    def _serializer(self, instance):
        if self.scheduler:
            return {
                'running': instance.running,
                'executors': instance.executors,
                'job_defaults': instance.job_defaults
            }
        return {
            'args': instance.args,
            'coalesce': instance.coalesce,
            'executor': instance.executor,
            'func': instance.func.__doc__,
            'func_ref': instance.func_ref,
            'id': instance.id,
            'kwargs': instance.kwargs,
            'max_instances': instance.max_instances,
            'misfire_grace_time': instance.misfire_grace_time,
            'name': instance.name,
            'next_run_time': instance.next_run_time,
            'pending': instance.pending,
        }
