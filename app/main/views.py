# encoding: utf-8
"""
@author: chep 

@file: views.py
@time: 2017/9/12 16:11

这一行开始写关于本文件的说明与解释
"""

from . import main
from flask import render_template,session,redirect,url_for
from .forms import MovieForm
from ..models import Movie



@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html")


@main.route("/query/movie",methods=['GET', 'POST'])
def movie():
    form = MovieForm()
    if form.validate_on_submit():
        key_word = "%%"+form.movie_name.data+"%%"
        data = Movie.query.filter(Movie.name.ilike(key_word)).all()
        print(data)
        if len(data)==0:
            session['movie_data'] = ['查询的电影不存在']
        else:
            movies=[]
            for d in data:
                movie={}
                movie["name"] = d.name
                movie["url"] = d.url
                movies.append(movie)
            session['movie_data'] = movies
        return redirect("/query/movie")
    return render_template("movie.html",form = form,movie_data = session["movie_data"])