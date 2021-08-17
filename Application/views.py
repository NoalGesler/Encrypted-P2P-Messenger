from flask import Blueprint
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint

from config import db

view = Blueprint("views", __name__)

# Global constants
NAME_KEY = 'name'
MSG_LIMIT = 20

# Global variables
PUBLIC_KEY = 'KEY'


# VIEWS


@view.route("/login", methods=["POST", "GET"])
def login():
    """
    displays main login page and handles saving session variables
    :exception POST
    :return: None
    """
    if request.method == "POST":  # if user input a name
        name = request.form["inputName"]
        public_key = request.form["publicKey"]
        session[PUBLIC_KEY] = ''
        if len(name) >= 2:
            if len(public_key) >= 8:
                if db.get_key() == '':
                    session[NAME_KEY] = name
                    session[PUBLIC_KEY] = public_key
                    db.save_key(public_key)
                    flash(f'You were successfully logged in as {name} with public key {public_key}.')
                    return redirect(url_for("views.home"))
                elif public_key == db.get_key():
                    session[NAME_KEY] = name
                    flash(f'You were successfully logged in as {name} with public key {public_key}.')
                    return redirect(url_for("views.home"))
                else:
                    flash("1Public key: {public_key} does not match session. Try again.")
            else:
                flash("1Key must be at least 8 characters.")
        else:
            flash("1Name must be longer than 1 character.")

    return render_template("login.html", **{"session": "session"})


@view.route("/logout")
def logout():
    """
    logs the user out by popping name from session
    :return: None
    """
    session.pop(NAME_KEY, None)
    flash("0You were logged out.")
    return redirect(url_for("views.login"))


@view.route("/")
@view.route("/home")
def home():
    """
    displays home page if logged in
    :return: None
    """
    if NAME_KEY not in session:
        return redirect(url_for("views.login"))

    return render_template("index.html", **{"session": session})


@view.route("/get_name")
def get_name():
    """
    :return: a json object storing name of logged in user
    """
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)


@view.route("/get_key")
def get_key():
    """
    :return: a json object storing public key
    """
    data = {"public_key": ""}
    if PUBLIC_KEY in session:
        data = {"public_key": session[PUBLIC_KEY]}
    # db.save_key(session[PUBLIC_KEY])
    print("GET KEY: ", db.get_key())
    return jsonify(data)


@view.route("/get_messages")
def get_messages():
    """
    :return: all messages stored in mock database
    """
    messages = db.get_all_messages(MSG_LIMIT)

    return jsonify(messages)


def remove_seconds(msg):
    """
    :return: string with seconds trimmed off
    """
    return msg.split(".")[0][:-3]