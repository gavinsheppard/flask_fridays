from flask import Flask, render_template

# Flask instance
app = Flask(__name__)

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