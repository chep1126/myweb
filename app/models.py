# encoding: utf-8
"""
@author: chep 

@file: models.py
@time: 2017/9/15 9:38

这一行开始写关于本文件的说明与解释
"""

from . import db


class Movie(db.Model):
    __tablename__ = "dyzz"
    id = db.Column(db.VARCHAR(20),primary_key = True)
    name = db.Column(db.VARCHAR(256))
    url = db.Column(db.VARCHAR(256))

    def __repr__(self):
        return '<Movie %r>' % self.name