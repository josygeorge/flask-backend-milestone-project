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
            flash("Username already exists")
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
        return redirect(url_for('profile', username=session['user']))
    return render_template('sign_up.html')


@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        # check for whether the user exists in the DB
        user_exists = mongo.db.users.find_one(
            {"username": request.form.get("uname").lower()})

        if user_exists:
            # ensure hashed password matches user input
            if check_password_hash(
                user_exists["password"], request.form.get("password")):
                    session["user"] = request.form.get("uname").lower()
                    flash("Welcome, {}".format(
                        request.form.get("uname")))
                    return redirect(url_for(
                        'profile', username=session['user']))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("sign_in"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("sign_in"))
    return render_template("sign_in.html")


# user profile
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    get_user = mongo.db.users.find_one(
        {"username": session["user"]})
    print(username)
    if session['user']:
        return render_template("profile.html", user=get_user)
    return redirect(url_for('sign_in'))


# update user profile
@app.route("/update-profile/<user_id>", methods=["GET", "POST"])
def update_profile(user_id):
    if request.method == 'POST':
        print(request.form.get("is_admin"))
        # password assign based on checking whether the user has made a password change
        if request.form.get("change_password") == "on":
            get_password = generate_password_hash(
                request.form.get("password"))
        else:
            get_password = mongo.db.users.find_one(
                {"_id": ObjectId(user_id)})["password"]
        update_user_profile = {
            "password": get_password,
            "firstname": request.form.get("fname"),
            "lastname": request.form.get("lname"),
            "email": request.form.get("email"),
            "is_admin": request.form.get("is_admin")
        }
        print(update_user_profile)
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_user_profile})
        flash("User Profile Updated")
        return redirect(url_for(
                    'profile', username=session['user']))
        # grab the session user's username from db for profile update
    get_user = mongo.db.users.find_one(
            {"_id": ObjectId(user_id)})
    return render_template('update_profile.html', user=get_user)


# Add Word and Definition
@app.route("/add-word", methods=["GET", "POST"])
def add_word():
    if request.method == 'POST':
        print(request.form.get("word_name"))
        print(request.form.getlist("definitions[]"))
    return render_template('add_word.html')


# Logout
@app.route("/sign-out")
def sign_out():
    # remove user from session cookie
    flash("You have been signed out...")
    session.pop("user")
    return redirect(url_for("list_words"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
