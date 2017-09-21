# encoding: utf-8
"""
@author: chep 

@file: forms.py
@time: 2017/9/19 11:00

这一行开始写关于本文件的说明与解释
"""
from flask_wtf import FlaskForm
from wtforms import DateField,StringField,SubmitField
from wtforms.validators import DataRequired

class add_item(FlaskForm):
    date = DateField("日期",validators=[DataRequired()])
    content=StringField("内容",validators=[DataRequired()])
    submit = SubmitField('提交')
