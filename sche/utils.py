#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: utils.py
# Author: jianglin
# Email: mail@honmaple.com
# Created: 2017-02-02 12:24:45 (CST)
# Last Update: Sunday 2018-09-30 17:50:04 (CST)
#          By:
# Description:
# **************************************************************************
from flask import make_response, jsonify


class HTTPResponse(object):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500

    def __init__(self, status_code=200, message="", data=None, pageinfo=None):
        self.status_code = status_code
        self.message = message
        self.data = data
        self.pageinfo = pageinfo

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "message": self.message,
            "data": self.data,
            "pageinfo": self.pageinfo
        }

    def to_response(self):
        resp = dict(message=self.message)
        if self.data is not None:
            resp.update(data=self.data)
        if self.pageinfo is not None:
            resp.update(pageinfo=self.pageinfo)
        return make_response(jsonify(**resp), self.status_code)


class HTTP(object):
    @classmethod
    def OK(cls, message="ok", data=None, pageinfo=None):
        return HTTPResponse(
            HTTPResponse.OK,
            message,
            data,
            pageinfo,
        ).to_response()

    @classmethod
    def BAD_REQUEST(cls, message="bad request", data=None):
        return HTTPResponse(
            HTTPResponse.BAD_REQUEST,
            message,
            data,
        ).to_response()

    @classmethod
    def UNAUTHORIZED(cls, message="unauthorized", data=None):
        return HTTPResponse(
            HTTPResponse.UNAUTHORIZED,
            message,
            data,
        ).to_response()

    @classmethod
    def FORBIDDEN(cls, message="forbidden", data=None):
        return HTTPResponse(
            HTTPResponse.FORBIDDEN,
            message,
            data,
        ).to_response()

    @classmethod
    def NOT_FOUND(cls, message="not found", data=None):
        return HTTPResponse(
            HTTPResponse.NOT_FOUND,
            message,
            data,
        ).to_response()

    @classmethod
    def SERVER_ERROR(cls, message="internal server error", data=None):
        return HTTPResponse(
            HTTPResponse.SERVER_ERROR,
            message,
            data,
        ).to_response()


class Serializer(object):
    def __init__(self, instance, trigger=None):
        self.instance = instance
        self.trigger = trigger

    @property
    def data(self):
        if isinstance(self.instance, list):
            return self._serializerlist(self.instance)
        return self._serializer(self.instance)

    def _serializerlist(self, instances):
        results = []
        for instance in instances:
            result = {}
            if self.trigger and self.trigger in ['date', 'interval']:
                trigger = 'run_date' if self.trigger == 'date' else 'interval'
                if hasattr(instance.trigger, trigger):
                    result = self._serializer(instance)
            else:
                result = self._serializer(instance)
            if result:
                results.append(result)
        return results

    def _serializer(self, instance):
        result = {
            'args': instance.args,
            'coalesce': instance.coalesce,
            'executor': instance.executor,
            'func': instance.func_ref,
            # 'func': instance.func.__doc__,
            'func_ref': instance.func_ref,
            'id': instance.id,
            'kwargs': instance.kwargs,
            'max_instances': instance.max_instances,
            'misfire_grace_time': instance.misfire_grace_time,
            'name': instance.name,
            'next_run_time': instance.next_run_time,
            'pending': instance.pending,
        }
        trigger = instance.trigger
        t = {}
        if hasattr(trigger, 'interval'):
            t = {
                'trigger': 'interval',
                'end_date': trigger.end_date,
                'start_date': trigger.start_date,
                'interval': trigger.interval.seconds,
            }
        elif hasattr(trigger, 'run_date'):
            t = {
                'trigger': 'date',
            }
        result.update(**t)
        return result
