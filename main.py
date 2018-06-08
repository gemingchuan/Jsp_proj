# -*- coding: utf-8 -*-

import json

from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import DevConfig, DatabaseConfig

app = Flask(__name__, static_url_path='', root_path='')
'''
app.config.from_object(DevConfig)
#app.config.from_object(DatabaseConfig)
#app.config.from_object(ProdConfig)

db = SQLAlchemy(app)

class record(db.Model):
    name = db.Column(db.String(10), primary_key=True, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    go = db.Column(db.String(5), nullable=False)
    back = db.Column(db.String(5), nullable=False)
    where = db.Column(db.String(50), nullable=False)
'''

login_manager = LoginManager(app)

@app.route('/',  methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/login',  methods=['GET', 'POST'])
def log():
    if request.method == 'GET':
        return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')