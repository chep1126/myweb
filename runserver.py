# encoding: utf-8
"""
@author: chep 

@file: runserver.py
@time: 2017/9/15 14:57

这一行开始写关于本文件的说明与解释
"""
from app import create_app
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.run(debug=True)