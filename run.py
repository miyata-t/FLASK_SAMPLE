from flask import Flask
from flask_login import LoginManager
import os
from flask_bootstrap import Bootstrap


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

# DBの登録
init_db(app)

login_manager = LoginManager()
login_manager.init_app(app)

# https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager.user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

if __name__ == '__main__':
    app.run()
