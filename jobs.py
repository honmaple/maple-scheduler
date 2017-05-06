#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: jobs.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-02-02 14:28:16 (CST)
# Last Update:星期六 2017-5-6 23:1:13 (CST)
#          By:
# Description:
# **************************************************************************
from time import time


def scheduler_vvv():
    '''输出hello world'''
    print('hello world')


def scheduler_kkk():
    '''输出helloorld'''
    print('helloorld')


def scheduler_time(a):
    '''输出时间,参数a'''
    print('{}{}'.format(a, time()))
