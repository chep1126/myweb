# encoding: utf-8
"""
@author: chep 

@file: errors.py
@time: 2017/9/12 16:11

这一行开始写关于本文件的说明与解释
"""
from . import main
from flask import render_template


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
