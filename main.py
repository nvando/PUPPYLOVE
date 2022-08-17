from xmlrpc.client import Boolean
from flask import Flask, render_template, url_for, redirect, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, validators
from helpers import hash_password
import csv
from pathlib import Path

USERS_PATH = Path.cwd() / "users.csv"

app = Flask(__name__)
app.secret_key = "mysupersecretkey"


class LoginForm(FlaskForm):

    username = StringField("Username", [validators.InputRequired()])
    password = PasswordField("Password", [validators.InputRequired()])
    submit = SubmitField("Submit")


class RegistrationForm(LoginForm):

    email = StringField("Email", [validators.Email(message="Please enter a valid email address")])
    username = StringField("Create a username", [validators.InputRequired()])
    password = PasswordField(
        "Password",
        [
            validators.length(min=6, message="Must contain at least 6 characters"),
            validators.regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]"),
        ],
    )
    stay_loggedin = BooleanField(
        "Keep me logged in",
    )


@app.route("/")
def index():
    return render_template("bootstrap_index.html")


@app.route("/home")
def home():
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if request.method == "GET":
        error = request.args.get("error")
        return render_template("bootstrap_login.html", form=form, error=error)

    if request.method == "POST":
        if valid_login(form.username.data, form.password.data):
            session["user"] = form.username.data
            session["password"] = form.password.data

            session["logged_in"] = True
            return redirect(url_for("dashboard"))

        else:
            error = "Invalid username or password"
            return redirect(url_for("login", error=error))


@app.route("/logout", methods=["GET", "POST"])
def logout():

    session.clear()
    return redirect(url_for("index"))


@app.route("/signup", methods=["GET", "POST"])
def signup():

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data

        # session["user"] = form.username.data
        # if all(valid_username(session["user"])):  # check if all username conditions are true

            # session["email"] = form.email.data
            # session["password"] = form.password.data

            # add_user(session["user"], session["password"])
        
        if all (valid_username(username)):
            password = form.password.data
            email = form.username.data
            add_user(username, password)

            if form.stay_loggedin.data is True:
                session["user"] = username
                session["email"] = email
                session["password"] = password
                session["logged_in"] = True
                return redirect(url_for("dashboard"))

            else:
                return redirect(url_for("thankyou", username=username))

        else:
            return redirect(url_for("report", username=username))

    return render_template("bootstrap_signup.html", form=form)


@app.route("/dashboard")
def dashboard():
    if 'logged_in' in session: 
        return render_template("bootstrap_dashboard.html")
    else: return redirect(url_for("index"))


@app.route("/report")
def report():
    username = request.args.get("username")

    contains_upper, contains_lower, ends_num = valid_username(username)

    return render_template(
        "bootstrap_report.html",
        contains_lower=contains_lower,
        contains_upper=contains_upper,
        ends_num=ends_num,
    )


@app.route("/thankyou")
def thankyou():
    username = request.args.get("username")

    if not username is None:
        return render_template("bootstrap_thankyou.html", username=username)
    else:
        return redirect(url_for("index"))


def valid_login(username, password):

    with open(USERS_PATH, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if username in row[0]:
                if hash_password(password) == row[1]:
                    return True
        else:
            return False


def add_user(username, password):

    hash_pw = hash_password(password)

    with open(USERS_PATH, "a", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([username, hash_pw])


def valid_username(username):

    contains_upper = any(char.isupper() for char in username)
    contains_lower = any(char.islower() for char in username)
    ends_num = username[-1].isdigit()

    return contains_upper, contains_lower, ends_num


if __name__ == "__main__":
    app.run(debug=True)
