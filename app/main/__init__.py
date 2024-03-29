# encoding: utf-8
"""
@author: chep 

@file: __init__.py.py
@time: 2017/9/12 16:10

这一行开始写关于本文件的说明与解释
"""
from flask import Blueprint
from ..models import Permission

main = Blueprint('main', __name__)

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

from . import views,errors
