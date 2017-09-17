# encoding: utf-8
"""
@author: chep 

@file: models.py
@time: 2017/9/15 9:38

这一行开始写关于本文件的说明与解释
"""

from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app



class Movie(db.Model):
    __tablename__ = "dyzz"
    id = db.Column(db.VARCHAR(20),primary_key = True)
    name = db.Column(db.VARCHAR(256))
    url = db.Column(db.VARCHAR(256))
    download = db.Column(db.Integer,nullable=False, default=1)
    error= db.Column(db.VARCHAR(256))
    def __repr__(self):
        return '<Movie %r>' % self.name


class Movie_info(db.Model):
    __tablename__ = "movie_info"
    id = db.Column(db.VARCHAR(20), primary_key=True)
    content = db.Column(db.TEXT)
    ftp_urls = db.Column(db.TEXT)
    thunder_urls = db.Column(db.TEXT)


class Role(db.Model):
    __tablename__ ="roles"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship("User",backref = 'role')


class User(UserMixin,db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean,default=False)

    def generate_confirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm')!=self.id:
            return False

        self.confirmed=True
        db.session.add(self)
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))