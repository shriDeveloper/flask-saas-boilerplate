
from app import app
from flask import render_template , redirect , url_for , flash
from app.models import Product , User

from app.forms import RegisterForm ,LoginForm
from flask_login import login_user , logout_user , current_user 

#db instance here
from app.models import db

@app.route('/')
@app.route('/home')
def home_page():
	if current_user.is_authenticated:
		return redirect(url_for('dashboard_page'))
	return render_template('home.html')
	
@app.route('/about')
def about_page():
	return render_template('about.html')

@app.route('/dashboard')
def dashboard_page():
	if not current_user.is_authenticated:
		flash(f"Please login to continue",category='info')
		return redirect(url_for('home_page'))
	products = Product.query.all()
	return render_template('dashboard.html', products = products)

@app.route('/logout')
def logout_page():
	logout_user()
	flash(f"You have been logged out", category='info')
	return redirect(url_for('home_page'))

@app.route('/register'  , methods = ['GET' , 'POST'])
def register_page():
	form = RegisterForm()
	if form.validate_on_submit():
		#create user here
		user = User(email = form.email.data , 
					user_name = form.username.data , 
					password = form.password_1.data )
		db.session.add(user)
		db.session.commit()
		flash(f"Account created successfully.You are logged in",category='success')
		login_user(user)
		return redirect(url_for('dashboard_page'))
	if form.errors != {}:
		for errors in form.errors.values():
			flash(f"{errors}" , category = 'danger')
	return render_template('register.html' , register_form = form)

@app.route('/login', methods=['GET','POST'])
def login_page():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user and user.check_password_hash(form.password.data):
			login_user(user)
			flash(f"You are logged in",category='success')
			return redirect(url_for('dashboard_page'))
		else:
			flash(f"User does not exist",category='danger')
	if form.errors != {}:
		for error in form.errors.values():
			flash(error,category='danger')
	return render_template('login.html' , login_form = form)