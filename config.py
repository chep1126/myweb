# encoding: utf-8
"""
@author: chep 

@file: config.py
@time: 2017/9/12 16:15

程序的配置
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[CHEP]'
    FLASKY_MAIL_SENDER = 'admin@admin.com'
    FLASKY_ADMIN = os.environ.get("FLASKY_ADMIN") or "admin@admin.com"
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1126@localhost:3306/flask?charset=utf8'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS=True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "admin@admin.com"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ""


class TestingConfig(Config):
    TESTING = True
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

