# encoding: utf-8
"""
@author: chep 

@file: __init__.py.py
@time: 2017/9/12 16:10

程序工厂
"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_mail import Mail

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection="strong"#提供不同的安全等级防止用户会话遭篡改
login_manager.login_view='main.login'#login_view 属性设置登录页面的端点。


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')

    from .movie import movie as movie_blueprint
    app.register_blueprint(movie_blueprint,url_prefix = "/movie")

    return app
