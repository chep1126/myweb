# encoding: utf-8
"""
@author: chep 

@file: manage.py.py
@time: 2017/9/12 16:15


"""
import os
from app import create_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    app.run()
