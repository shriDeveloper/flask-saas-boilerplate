from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField

from .models import User
#validators
from wtforms.validators import Length , EqualTo , Email , DataRequired , ValidationError

class RegisterForm(FlaskForm):
	
	#this is the validation check
	def validate_username(self, username):
		user = User.query.filter_by(user_name = username.data).first()
		if user:
			raise ValidationError('UserName already exist. Please choose another one')

	username = StringField(label='username' , validators = [Length(min = 2 , max = 10) , DataRequired()])
	email = StringField(label='email' , validators = [Email() , DataRequired() ])
	password_1 = PasswordField(label='Password' , validators = [Length(min = 3 , max = 90) , DataRequired()])
	password_2 = PasswordField(label='Password Confirm' , validators = [EqualTo('password_1') , DataRequired()])
	submit = SubmitField(label= 'submit') 

class LoginForm(FlaskForm):
	email = StringField(validators=[Email() , DataRequired()])
	password = PasswordField(validators=[DataRequired()])
	submit = SubmitField(label='submit')
