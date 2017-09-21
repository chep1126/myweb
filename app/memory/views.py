# encoding: utf-8
"""
@author: chep 

@file: views.py
@time: 2017/9/19 10:59

这一行开始写关于本文件的说明与解释
"""
from flask import render_template,flash,redirect,url_for,session,request
from . import memory
from .. import db
from flask_login import current_user
from .forms import add_item
from ..models import Memory
from datetime import datetime
from flask_login import login_required
import json

@login_required
@memory.route('/',methods=["POST","GET"])
def memory_index():
    print(request.data)
    form = add_item()
    user_id = current_user.id
    memories = get_memories(user_id)
    if memories:
        has_content = True
        session['memories']=memories
    else:
        has_content=False
    if form.validate_on_submit():
        date= form.date.data
        content = form.content.data
        m = Memory(user_id=user_id,do_time=date,content=content)
        db.session.add(m)
        db.session.commit()
        flash("添加成功","success")
        return redirect(url_for('memory.memory_index'))
    return render_template('memory/memory_index.html',memories=session.get('memories'),has_content=has_content,form = form)


@memory.route('/del/<item_id>',methods=["GET","POST"])
def del_item(item_id):
    m = Memory.query.filter_by(id=item_id).all()
    m[0].is_done=True
    db.session.add(m[0])
    db.session.commit()
    return "修改成功"


@memory.route('/recovery/<item_id>',methods=["GET","POST"])
def recovery_item(item_id):
    m = Memory.query.filter_by(id=item_id).all()
    m[0].is_done=False
    db.session.add(m[0])
    db.session.commit()
    return "修改成功"


@memory.route('/query')
def query():
    user_id = current_user.id
    ms = get_memories(user_id)
    json_data = json.dumps(ms)
    return json_data


def get_memories(user_id):
    ms = Memory.query.filter_by(user_id = user_id).all()
    if ms:
        memories= []
        for m in ms:
            memory = {}
            memory['create_time'] = datetime.strftime(m.create_time,format='%Y-%m-%d')
            memory["do_time"] = datetime.strftime(m.do_time,format='%Y-%m-%d')
            memory['id'] = m.id
            memory["content"] = m.content
            memory["is_done"] = m.is_done
            memories.append(memory)
        return memories
    else:
        return False