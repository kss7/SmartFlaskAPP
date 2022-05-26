from flask import Flask, render_template,request, Blueprint, redirect
from flask_login import current_user, login_user, logout_user, login_required
from main.models import User, UserSchema
from main import db
users_schema = UserSchema(many=True)
import time

bp = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@bp.route('/')
@bp.route('/index')
def hello():
   return render_template('index.html')


@bp.route('/login', methods=['POST', 'GET'])
def login():
   msg = ''
   if current_user.is_authenticated:
      return redirect('/dashboard')
   if request.method == 'POST':
      email = request.form['email']
      user = User.query.filter_by(email=email).first()
      if user is not None and user.is_correct_password(request.form['password']):
         user.authenticated = True
         db.session.add(user)
         db.session.commit()
         login_user(user)
         return redirect('/dashboard')
      msg= "Wrong username or password"
   return render_template('login.html', msg=msg)

@bp.route('/dashboard')
@login_required
def dashboard():
   result = users_schema.dump(User.get_all_users())
   return render_template('dashboard.html', rows=result)

@bp.route('/register', methods=['POST', 'GET'])
def register():
   msg = ''
   if current_user.is_authenticated:
      return redirect('/dashboard')

   if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
      if User.query.filter_by(email=email).first():
         msg = 'Email-ID Already Present!'
         #return ('Email-ID Already Present')
      elif not password or not email:
         msg = 'Please fill Email and Password!'
      else:
         user = User(email, password)
         #user.set_password(password)
         db.session.add(user)
         db.session.commit()
         msg = email + ' : You have successfully registered. Redirecting to Login Page...'
         return render_template('register.html', msg=msg), {"Refresh": "10; url=/login"}
   return render_template('register.html', msg = msg)


@bp.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect('/login')