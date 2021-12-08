from flask import Blueprint
from flask import render_template, request, redirect, session
from flask.helpers import url_for
from flask_login import login_user
from models.user import User
from views.login_manager import login_manager
import re

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
      
      if not  __is_request_enabled(user_name, password):
        return redirect(url_for('login.login', msg='利用できる半角英数字のみです'))
      
      user = User.query.filter_by(user_name=user_name).first()

      if user is None:
          return redirect(url_for('login.login', msg='ユーザー名もしくはパスワードが誤っています。'))

      if user.password == password:
          login_user(user)
          session["user_name"] = user.user_name
          session["address"] = user.address

          next_page = request.args.get('next')
          return  redirect(next_page) if next_page else redirect('/')

      return redirect(url_for('login.login', msg='ユーザー名もしくはパスワードが誤っています。'))
    else:
        req = request.args
        msg = req.get("msg")
        print(msg)
        return render_template('login.html', msg=msg)

def __is_request_enabled(user_name, password):
    repatter = re.compile(r'^\w{1,20}$')
    validation_user_name = repatter.match(user_name)
    validation_password = repatter.match(password)
    
    if validation_user_name and validation_password:
        return True
    else:
        return False
