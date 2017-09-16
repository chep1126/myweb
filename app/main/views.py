# encoding: utf-8
"""
@author: chep 

@file: views.py
@time: 2017/9/12 16:11

这一行开始写关于本文件的说明与解释
"""

from . import main
from flask import render_template,session,redirect,current_app
from .forms import MovieForm
from ..models import Movie,Movie_info
from urllib.parse import urljoin


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html")


@main.route("/query/movie",methods=['GET', 'POST'])
def movie():
    half_url = "http://www.dytt8.net/"
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
        return redirect("/query/movie")
    return render_template("movie.html",form = form,movie_data = session.get("movie_data"))


@main.route('/query/movie/<movie_id>')
def movie_info(movie_id):
    m_info={}
    movie_data = Movie_info.query.filter_by(id =movie_id).all()
    title = Movie.query.filter_by(id = movie_id).all()
    print(movie,title)
    try:
        m_info["title"] = title[0].name
        m_info['content'] = movie_data[0].content
        m_info['thunder_urls'] = movie_data[0].thunder_urls
        m_info["isexist"] = True

    except Exception as e:
        print(e)
        m_info["isexist"]=False
    return render_template("movie_info.html", movie_data=m_info)