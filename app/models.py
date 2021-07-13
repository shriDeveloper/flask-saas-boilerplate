
from app import db , bcrypt , login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#User Model
class User(db.Model , UserMixin):
	id = db.Column(db.Integer() , primary_key = True)
	user_name = db.Column(db.String(10) , unique = True , nullable = False)
	email = db.Column(db.String(50) , nullable = False , unique = True)
	password_hash = db.Column(db.String(50) , nullable = True)
	budget = db.Column(db.Integer() , nullable = False , default = 1000)
	products = db.relationship('Product' , backref = 'owned_by' , lazy =True)

	#for security passwords and stuffs
	@property
	def password(self):
		return self.password
	@password.setter
	def password(self , password):
		self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

	def check_password_hash(self , password):
		return bcrypt.check_password_hash(self.password_hash, password)
	
#Product Model
class Product(db.Model):
	id = db.Column(db.Integer() , primary_key = True)
	name = db.Column(db.String(10) , nullable = False , unique = True)
	price = db.Column(db.Integer() , nullable = False)
	barcode = db.Column(db.String(10) , nullable = False , unique = True)
	description = db.Column(db.String(1000) , nullable = False)
	owner = db.Column(db.Integer() , db.ForeignKey('user.id'))
	def __repr__(self):
		return f"{self.name} - {self.price}"
