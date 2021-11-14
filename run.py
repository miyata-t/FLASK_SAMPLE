from flask import Flask
from flask import render_template, request, redirect
from flask_login import LoginManager, login_required, logout_user
import os

# views
from views.login import login_app
from views.signup import signup_app

# models
from models.database_manager import init_db, db
from models.user import User, db
from models.post import Post, db


app = Flask(__name__)
app.register_blueprint(login_app)
app.register_blueprint(signup_app)
app.config['SECRET_KEY'] = os.urandom(24)

# DBの登録
init_db(app)

login_manager = LoginManager()
login_manager.init_app(app)

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
