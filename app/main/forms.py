# encoding: utf-8
"""
@author: chep 

@file: forms.py
@time: 2017/9/12 16:11

这一行开始写关于本文件的说明与解释
"""
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


class MovieForm(FlaskForm):
    movie_name = StringField(DataRequired)
    sub = SubmitField()
