# encoding: utf-8
"""
@author: chep 

@file: __init__.py.py
@time: 2017/9/19 10:58

这一行开始写关于本文件的说明与解释
"""
from flask import Blueprint

memory = Blueprint('memory', __name__)

from . import views