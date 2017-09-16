# encoding: utf-8
"""
@author: chep 

@file: manage.py.py
@time: 2017/9/12 16:15


"""
import os
from app import create_app,db
from app.models import Movie,Movie_info
from flask_script import Manager,Shell
from flask_migrate import  Migrate,MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app, db=db, Movie = Movie,Movie_info=Movie_info)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
