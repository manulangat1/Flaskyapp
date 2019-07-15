from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError

#local imports
from .models import User,Task
#create the form classes here
class LoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    password = StringField('password',validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')
#registration form
class RegisterForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired()])
    password2 = PasswordField('password2',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')
    #checking if the username exists
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username exists')
    #validating the email
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('email exists')
class TaskForm(FlaskForm):
    name = StringField('name',validators=[DataRequired()])
    details = TextAreaField('details',validators=[DataRequired(),Length(min=0,max=140)])
    submit = SubmitField('Post')
