#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: runserver.py
# Author: jianglin
# Email: mail@honmaple.com
# Created: 2017-02-02 09:18:53 (CST)
# Last Update: Sunday 2018-09-30 17:58:54 (CST)
#          By:
# Description:
# **************************************************************************
from sche import sche, api
from flask import Flask
from flask_cors import CORS
from flask import current_app
from flask.cli import FlaskGroup, run_command
from werkzeug.contrib.fixers import ProxyFix
from code import interact
import sys


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app)
    sche.init_app(app)
    api.init_app(app)
    return app


app = create_app("config")
app.wsgi_app = ProxyFix(app.wsgi_app)

cli = FlaskGroup(add_default_commands=False, create_app=lambda r: app)
cli.add_command(run_command)


@cli.command('shell', short_help='Starts an interactive shell.')
def shell_command():
    ctx = current_app.make_shell_context()
    interact(local=ctx)


@cli.command()
def runserver():
    app.run()


# a = scheduler.add_job(hello, run_date='2017-10-10 10:10', id='34')
# a = scheduler.add_job(hello, trigger='interval', seconds=10)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        app.run(port=8000)
    else:
        cli.main()
