# encoding: utf-8
"""
@author: chep 

@file: views.py
@time: 2017/9/18 19:16

这一行开始写关于本文件的说明与解释
"""
from . import movie
from .forms import MovieForm
from flask import session,render_template
from ..models import Movie,Movie_info
from urllib.parse import urljoin


@movie.route("/query",methods=['GET', 'POST'])
def movie_list():
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


    return render_template("movie/movie_list.html", form = form, movie_data = session.get("movie_data"))


@movie.route('/query/<movie_id>')
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

    return render_template("movie/movie_info.html", movie_data=m_info, url=url)