from app import app,db,login
#third party imports
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self,password):
        self.password_hash= generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
#user loader that loads users form the db
@login.user_loader
def load_user(id):
    user = User.query.get(int(id))
    return user
#tasks model
class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),index=True)
    details = db.Column(db.String(128),index=True)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return '<Task {}>'.format(self.name)
