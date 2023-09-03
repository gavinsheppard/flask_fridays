from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Flask instance
app = Flask(__name__)

# create a secret key
app.config['SECRET_KEY'] = "super_key"

# define database, using SQLite, called users.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# initialise database
db = SQLAlchemy(app)

# create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  # 200 chars
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #  create a string
    def __repr__(self):
        return '<Name %r>' % self.name





# create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email address", validators=[DataRequired()])
    submit = SubmitField("Submit")

# create a route decorator
@app.route('/')
def index():
    favorites = ['dfjf', 'kwjhf', 'hffljkf', 'hbflkh']
    return render_template("index.html", favorites=favorites)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()   # uses this form class
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:    # then add to db
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''     # reset form
        form.email.data = ''     # reset form
        flash("User added successfully")

    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", 
        form=form,
        name=name,
        our_users=our_users,
        )


# localhost:5000/user/Gavin
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)

# error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = UserForm()
    # validate form
    if form.validate_on_submit():
        name = form.name.data   # get name from form
        form.name.data = ''     # reset form
        flash("Form submitted successfully")

    return render_template("name.html",
        name = name,
        form = form,
        )
