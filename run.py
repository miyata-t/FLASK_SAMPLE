from flask import Flask
from flask.templating import render_template
from flask_login import LoginManager
import os
from flask_bootstrap import Bootstrap
from werkzeug.exceptions import NotFound


# views
from views.login import login_app
from views.logout import logout_app
from views.signup import signup_app
from views.post import post_app

# models
from models.database_manager import init_db
from models.user import User

app = Flask(__name__)
app.register_blueprint(login_app)
app.register_blueprint(logout_app)
app.register_blueprint(signup_app)
app.register_blueprint(post_app)
app.config['SECRET_KEY'] = os.urandom(24)
bootstrap = Bootstrap(app)

app.errorhandler(NotFound)
def page_not_found(error):
    return render_template('404.html')

app.register_error_handler(NotFound, page_not_found)

# DBの登録
init_db(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'

# https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager.user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

if __name__ == '__main__':
    app.run()
