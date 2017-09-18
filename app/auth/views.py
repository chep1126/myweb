# encoding: utf-8
"""
@author: chep 

@file: views.py
@time: 2017/9/18 19:15

这一行开始写关于本文件的说明与解释
"""
from . import auth
from ..models import User
from flask_login import login_user,login_required,logout_user,current_user
from .. import db
from ..email import send_email
from .forms import LoginForm,RegistrationForm
from flask import flash,url_for,redirect,render_template,request


@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            flash('登陆成功')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码不正确')
    return render_template('auth/login.html', form = form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出')
    return redirect(url_for('main.index'))


@auth.route('/register',methods=['GET','POST'])
def register():
   form = RegistrationForm()
   if form.validate_on_submit():
       user = User(email =form.email.data,username = form.username.data,password=form.password.data)
       db.session.add(user)
       db.session.commit()
       token = user.generate_confirmation_token()
       send_email(user.email,'Confirm Your Account','email/confirm',user=user,token=token)
       flash("已经向你的邮箱里发了一封确认邮件")
       return redirect(url_for('main.index'))
   return render_template('auth/register.html', form = form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash("您的邮箱已确认")

    else:
        flash("确认链接无效或已超时")
    return redirect('main.index')


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5]!='auth.' and request.endpoint !='static':

        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account','email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))
