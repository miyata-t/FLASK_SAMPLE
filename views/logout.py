from flask import Blueprint, redirect
from flask_login import login_required, logout_user

logout_app = Blueprint("logout", __name__)

@logout_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
