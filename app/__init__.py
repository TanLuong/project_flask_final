import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .models import db

db_manage = 'mysql'
acc = 'nhattan'
pw = 'baptan0302'
host = '127.0.0.1'
db_name = 'test'
encoding = 'charset=utf8mb4'


def create_app(test_config=None):
    # create and configure the app
    app =  Flask(__name__,  instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_manage}://{acc}:{pw}@{host}/{db_name}?{encoding}'
    app.config['SECRET_KEY'] = 'dev'
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import views
    app.register_blueprint(views.bp)


    return app
