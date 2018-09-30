#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: jobs.py
# Author: jianglin
# Email: mail@honmaple.com
# Created: 2017-02-02 14:28:16 (CST)
# Last Update: Sunday 2018-09-30 17:50:05 (CST)
#          By:
# Description:
# **************************************************************************
from time import time, sleep


def scheduler_vvv():
    '''输出hello world'''
    print('hello world')


def scheduler_kkk():
    '''输出helloorld'''
    print('helloorld')


def scheduler_time(a):
    '''
    输出时间,参数a
    asasdsda
    '''
    print('{}{}'.format(a, time()))


def scheduler_vvvv():
    '''
    sleep 20s
    '''
    print('sleep start')
    sleep(10)
    print('sleep end')
