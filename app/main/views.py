# encoding: utf-8
"""
@author: chep 

@file: views.py
@time: 2017/9/12 16:11

这一行开始写关于本文件的说明与解释
"""

from . import main
from flask import render_template


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html")
