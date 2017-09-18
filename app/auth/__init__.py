# encoding: utf-8
"""
@author: chep 

@file: __init__.py.py
@time: 2017/9/18 19:13

这一行开始写关于本文件的说明与解释
"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views

