from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Flask instance
app = Flask(__name__)

# create a secret key
app.config['SECRET_KEY'] = "super_key"

# create a form class
class NamerForm(FlaskForm):
    name = StringField("Enter name", validators=[DataRequired()])
    submit = SubmitField("Submit")

# create a route decorator
@app.route('/')
def index():
    favorites = ['dfjf', 'kwjhf', 'hffljkf', 'hbflkh']
    return render_template("index.html", favorites=favorites)

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
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data   # get name from form
        form.name.data = ''     # reset form

    return render_template("name.html",
        name = name,
        form = form,
        )
