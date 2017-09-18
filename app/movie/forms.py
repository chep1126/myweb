# encoding: utf-8
"""
@author: chep 

@file: forms.py
@time: 2017/9/18 19:21

这一行开始写关于本文件的说明与解释
"""
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,Length

class MovieForm(FlaskForm):
    movie_name = StringField(validators=[DataRequired()])
    sub = SubmitField("submit")


