# encoding: utf-8
"""
@author: chep 

@file: models.py
@time: 2017/9/15 9:38

这一行开始写关于本文件的说明与解释
"""

from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import date,datetime

class Permission:
    FOLLOW = 0x01#关注
    COMMENT = 0x02#评论
    WRITE_ARTICLES = 0x04#写文章
    MODERATE_COMMENTS = 0x08#管理评论
    ADMINISTER = 0x80#管理员


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
    __tablename__ = "roles"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean,default=True,index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User",backref = 'role',lazy="dynamic")


    #插入角色
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(UserMixin,db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean,default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

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

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def can(self,permissions):
        return self.role is not None and (self.role.permissions &permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


class Memory(db.Model):
    __tablename__='memories'
    user_id = db.Column(db.Integer)
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    create_time = db.Column(db.Date(),default=datetime.strftime(datetime.utcnow(),format='%Y-%m-%d'))
    do_time = db.Column(db.Date(),default=datetime.strftime(datetime.utcnow(),format='%Y-%m-%d'))
    content = db.Column(db.Text())
    is_done = db.Column(db.Boolean,default=False)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))