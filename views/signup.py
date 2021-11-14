from flask import Blueprint, render_template, request, redirect
from models.user import User, db

signup_app = Blueprint("signup", __name__)

@signup_app.route('/signup', methods=['GET', 'POST'])
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
