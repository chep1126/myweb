# encoding: utf-8
"""
@author: chep 

@file: views.py
@time: 2017/9/12 16:11

这一行开始写关于本文件的说明与解释
"""

from . import main
from flask import render_template,session,redirect,url_for,request,flash
from .forms import MovieForm,LoginForm,RegistrationForm
from ..models import Movie,Movie_info,User,Role
from urllib.parse import urljoin
from flask_login import login_user,login_required,logout_user,current_user
from .. import db
from ..email import send_email


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html")


@main.route("/query/movie",methods=['GET', 'POST'])
def movie():
    half_url = "http://www.ygdy8.net/"
    form = MovieForm()
    if form.validate_on_submit():
        key_word = "%%"+form.movie_name.data+"%%"
        data = Movie.query.filter(Movie.name.ilike(key_word)).all()
        if len(data) == 0:
            session['movie_data'] = ['查询的电影不存在']
        else:
            movies=[]
            for d in data:
                movie={}
                movie['id'] = d.id
                movie["name"] = d.name
                movie["url"] = urljoin(half_url,d.url)
                movies.append(movie)
            session['movie_data'] = movies


    return render_template("movie.html",form = form,movie_data = session.get("movie_data"))


@main.route('/query/movie/<movie_id>')
def movie_info(movie_id):
    url={}
    m_info={}
    movie_data = Movie_info.query.filter_by(id =movie_id).all()
    title = Movie.query.filter_by(id = movie_id).all()
    print(movie_data,title)
    try:
        m_info["title"] = title[0].name
        m_info['content'] = movie_data[0].content
        thunder_urls = movie_data[0].thunder_urls
        ftp_urls =movie_data[0].ftp_urls
        for x,y in zip(thunder_urls.split(';'),ftp_urls.split(';')):
            url[x]=y
        m_info["isexist"] = True

    except Exception as e:
        print(e)
        m_info["isexist"]=False

    return render_template("movie_info.html", movie_data=m_info,url=url)


@main.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            flash('登陆成功')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码不正确')
    return render_template('login.html',form = form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出')
    return redirect(url_for('main.index'))


@main.route('/register',methods=['GET','POST'])
def register():
   form =  RegistrationForm()
   if form.validate_on_submit():
       user = User(email =form.email.data,username = form.username.data,password=form.password.data)
       db.session.add(user)
       db.session.commit()
       token = user.generate_confirmation_token()
       send_email(user.email,'Confirm Your Account','email/confirm',user=user,token=token)
       flash("已经向你的邮箱里发了一封确认邮件")
       return redirect(url_for('main.index'))
   return render_template('register.html',form = form)


@main.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash("您的邮箱已确认")

    else:
        flash("确认链接无效或已超时")
    return redirect('main.index')


@main.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5]!='main.' and request.endpoint !='static':

        return redirect(url_for('main.unconfirmed'))


@main.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('unconfirmed.html')


@main.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account','email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))