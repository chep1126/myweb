# encoding: utf-8
"""
@author: chep 

@file: __init__.py.py
@time: 2017/9/12 16:10

程序工厂
"""
from flask import Flask
from flask_bootstrap import Bootstrap
from config import config
bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
