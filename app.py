import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env


# create instance of Flask
app = Flask(__name__)
# Setting environment variables
app.config["MONGO_DATABASE"] = os.environ.get("MONGO_DATABASE")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
# instance of mongo
mongo = PyMongo(app)


# Routes
@app.route('/')
@app.route('/list-words')
def list_words():
    words = mongo.db.words.find()
    return render_template('glossary.html', words=words)


# Sign Up
@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        # check for whether the user exists in the DB
        user_exists = mongo.db.users.find_one(
            {"username": request.form.get("uname").lower()}
        )
        if user_exists:
            flash("User already exists")
            return redirect(url_for("sign_up"))
        user_sign_up = {
            "username": request.form.get("uname").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "firstname": request.form.get("fname"),
            "lastname": request.form.get("lname"),
            "email": request.form.get("email"),
            "is_admin": request.form.get("is_admin")
        }
        mongo.db.users.insert_one(user_sign_up)
        # put the new user into 'session' cookie
        session["user"] = request.form.get("uname").lower()
        flash("User Created!")
        return redirect(url_for('list_words', username=session['user']))
    return render_template('sign_up.html')


# Register user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if the POST user exists in DB
        user_exists = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if user_exists:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("User Created!")
        return redirect(url_for('profile', username=session['user']))
    return render_template("register.html")

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
