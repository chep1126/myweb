# encoding: utf-8
"""
@author: chep 

@file: email.py
@time: 2017/9/17 22:02

这一行开始写关于本文件的说明与解释
"""
from flask_mail import Message
from flask import current_app,render_template
from . import mail

def send_email(to,subject,template,**kwargs):
    msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=current_app.config["FLASKY_MAIL_SENDER"],recipients=[to])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.body = render_template(template + '.html', **kwargs)
    mail.send(msg)

