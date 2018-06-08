# -*- coding: utf-8 -*-

import json

from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, login_required, UserMixin, logout_user


from config import DevConfig, DatabaseConfig

app = Flask(__name__, static_url_path='', root_path='')

app.config.from_object(DevConfig)
app.config.from_object(DatabaseConfig)
#app.config.from_object(ProdConfig)

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    usr = db.Column(db.String(20), primary_key=True, nullable=False)
    pwd = db.Column(db.String(20), nullable=False)

    #@property
    def get_id(self):
        return self.usr


db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)





login_manager.login_view = "login"  # 定义登录的 视图
login_manager.login_message = '请登录以访问此页面'  # 定义需要登录访问页面的提示消息


@login_manager.user_loader
def user_loader(usr):
    return User.query.filter_by(usr=usr).first()


@app.route('/',  methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/welcome',  methods=['GET'])
@login_required
def login_success():
    return render_template('welcome.html')


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        tmp_user = User.query.filter_by(usr=username).first()
        if not tmp_user:
            flash('该用户不存在')
        elif request.form.get('password') != tmp_user.pwd:
            flash('密码错误')
        else:
            login_user(tmp_user, remember=True)
            return redirect('/welcome')
    return render_template('login.html')


@app.route('/register',  methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        tmp_user = User.query.filter_by(usr=username).first()

        if tmp_user:
            flash('该用户已存在')
        #elif request.form.get('password') != user.pwd:
        #    flash('密码错误')
        else:
            t = User(usr=username, pwd=password)
            try:
                db.session.add(t)
            except:
                pass
            finally:
                db.session.commit()
                db.session.close()
                print('committed!')
                return redirect('/login')
    return render_template('register.html')


@app.route('/logout/')
@login_required
def logout():
    logout_user()  # 登出用户
    return '''
    已经退出登录 <a href='/'>回到主页</a>
    
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0')