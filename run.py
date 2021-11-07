from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from datetime import datetime
import pytz
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# テーブル定義
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(12), nullable=False)
    address = db.Column(db.String(30), nullable=True)

# https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager.user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
@login_required
def index():
    if request.method == 'GET':
        posts = Post.query.all()

        return render_template('index.html', posts=posts)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        address = request.form.get('address')
        
        user = User(user_name=user_name, password=password, address=address)
        
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        
        user = User.query.filter_by(user_name=user_name).first()

        if user.password == password:
            login_user(user)
            session["user_name"] = user.user_name
            session["address"] = user.address
            
            return redirect('/')
        
        return redirect('/login')
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        
        post = Post(title=title, body=body)
        
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create.html')

@app.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get(id)
    
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.body = request.form.get('body')
                
        db.session.commit()
        
        return redirect('/')

@app.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get(id)
    
    db.session.delete(post)
    db.session.commit()
    
    return redirect('/')

if __name__ == '__main__':
    app.run()
