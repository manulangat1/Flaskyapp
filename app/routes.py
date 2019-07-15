#global imports
from app import app,db

#third-party imports
from flask import url_for,render_template,flash,redirect
from datetime import datetime
from flask_login  import current_user,login_user,logout_user,login_required

#local imports
from .models import User,Task
from .forms import LoginForm,RegisterForm,TaskForm

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
#create your routes here

#login route.this will be the default page users see
@app.route('/',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not  user.check_password(form.password.data):
        # if user is None or not user.check_password(form.password.data):
            flash("inavlid login details")
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html',form=form,title="login")

#register route...
@app.route('/register',methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('you are now registered')
        return redirect(url_for('login'))
    return render_template('register.html',form=form,title="register")

#home route
@app.route('/home',methods={"GET","POST"})
@login_required
def home():
    posts = Task.query.all()
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data,details=form.details.data)
        db.session.add(task)
        db.session.commit()
        flash("posted successfully")
        return redirect(url_for('home'))
    return render_template('home.html',form=form,posts=posts,title="home")
#get homes item by id
@app.route('/post/<int:id>')
def post(id):
    post = Task.query.get_or_404(id)
    return render_template('hoe.html',post=post)

#log out controller
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
