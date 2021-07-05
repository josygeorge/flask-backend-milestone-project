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
    words = mongo.db.words.find().sort('name', 1)
    return render_template('glossary.html', words=words)


# Search word
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    words = mongo.db.words.find({"$text": {"$search": query}})
    return render_template("glossary.html", words=words)


# Word Details Page
@app.route('/list-words-details/<word_id>')
def list_words_details(word_id):
    word_list = mongo.db.words.find_one(
        {"_id": ObjectId(word_id)})
    if word_list["_id"] == ObjectId(word_id):    
        return render_template('word_details_page.html', word=word_list)
    else:
        return render_template('glossary.html')


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
        session["is_admin"] = request.form.get("is_admin")
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
                    session["is_admin"] = user_exists["is_admin"]
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
    if session['user']:
        return render_template("profile.html", user=get_user)
    return redirect(url_for('sign_in'))


# update user profile
@app.route("/update-profile/<user_id>", methods=["GET", "POST"])
def update_profile(user_id):
    if session["user"]:
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
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": update_user_profile})
            flash("User Profile Updated")
            return redirect(url_for(
                        'profile', username=session['user']))
        # grab the session user's username from db for profile update
        get_user = mongo.db.users.find_one(
                {"_id": ObjectId(user_id)})
        return render_template('update_profile.html', user=get_user)
    else:
        return render_template('sign_in.html')


# Add Word and Definition
@app.route("/add-word", methods=["GET", "POST"])
def add_word():
    if session["user"]:
        if request.method == 'POST':
            new_word_to_insert = {
                "name": request.form.get("word_name").lower(),
                "definitions": request.form.getlist("definitions[]"),
                "synonyms": request.form.getlist("synonyms[]"),
                "antonyms": request.form.getlist("antonyms[]"),
                "etymology": request.form.get("etymology"),
                "word_created_by": session["user"]
            }
            mongo.db.words.insert_one(new_word_to_insert)
            flash("New word and it's definitions created!")
            return redirect(url_for('list_words'))
        return render_template('add_word.html')
    else:
        return render_template('glossary.html')


# Edit Word and Definition
@app.route("/edit-word/<word_id>", methods=["GET", "POST"])
def edit_word(word_id):
    if session["user"]:
        if request.method == 'POST':
            word_to_update = {
                "name": request.form.get("word_name").lower(),
                "definitions": request.form.getlist("definitions[]"),
                "synonyms": request.form.getlist("synonyms[]"),
                "antonyms": request.form.getlist("antonyms[]"),
                "etymology": request.form.get("etymology"),
            }
            mongo.db.words.update_one(
                {"_id": ObjectId(word_id)}, {"$set": word_to_update})
            flash("Word Definition Updated")
            return redirect(url_for('list_words_details', word_id=word_id))
        word = mongo.db.words.find_one({"_id": ObjectId(word_id)})
        return render_template('edit_word.html', word=word)
    else:
        return render_template('glossary.html')


# Delete Word Definition
@app.route("/delete-word/<word_id>")
def delete_word(word_id):
    if session["user"]:
        mongo.db.words.remove({"_id": ObjectId(word_id)})
        flash("Word and Definition Deleted!")
        return redirect(url_for("list_words"))
    else:
        return render_template('glossary.html')


# Logout
@app.route("/sign-out")
def sign_out():
    # remove user from session cookie
    flash("You have been signed out...")
    session.pop("is_admin")
    session.pop("user")
    return redirect(url_for("list_words"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=False)
