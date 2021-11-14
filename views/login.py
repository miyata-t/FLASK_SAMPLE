from flask import Blueprint
from flask import render_template, request, redirect, session
from flask_login import login_user
from models.user import User
from views.login_manager import login_manager

login_app = Blueprint("login", __name__)
# https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager.user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_app.route('/login', methods=['GET', 'POST'])
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
