from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from models.post import Post, db

post_app = Blueprint("post", __name__)

@post_app.route('/')
@login_required
def index():
    if request.method == 'GET':
        posts = Post.query.all()

        return render_template('index.html', posts=posts)

@post_app.route('/create', methods=['GET', 'POST'])
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

@post_app.route('/<int:id>/update', methods=['GET', 'POST'])
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

@post_app.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get(id)
    
    db.session.delete(post)
    db.session.commit()
    
    return redirect('/')
