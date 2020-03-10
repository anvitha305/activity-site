from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from tempfile import mkdtemp
import sqlite3
import os
from sqlalchemy.dialects import postgresql
from random import randint
from smtplib import SMTP_SSL as SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from flask_sqlalchemy import SQLAlchemy
import sys
# Configure application
app = Flask(__name__)
app.secret_key = os.environ.get("secret_key")
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)
class Dataentry(db.Model):
    __tablename__ = "users"
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    club_list = db.Column(postgresql.ARRAY(db.String), nullable=True)
    def __init__ (self, first_name, last_name, email, password_hash, club_list):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.club_list = club_list
def password_set(email):
    password = "" + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9))
    msg = MIMEMultipart()
    msg['From'] = "anvitha2k20@gmail.com"
    msg['To'] = email
    msg['Subject'] = 'Hey guess what? You\'ve got a new best friend in ABctivities.'
    message = "So. You tried to make an account with us, the ever-humble ABctivities group. Thanks and congratulations. Here's your six-digit code you can enter into login for a password reset: "+ password
    msg.attach(MIMEText(message))
    smtp_server = SMTP('smtp.gmail.com','465')
    em = os.environ.get("email")
    pw  = os.environ.get("password")
    smtp_server.login(em, pw)
    smtp_server.sendmail(em, email, msg.as_string())
    smtp_server.close()
    return password
@app.route('/home')
@app.route("/")
@login_required
def home():
    return render_template("homepage.html")

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method=="POST":
        if not request.form.get("f_name"):
            return apology("Give me thine first name you fool. You absolute coward.")
        f_name = request.form.get("f_name")
        if not request.form.get("l_name"):
            return apology("Give me thine surname you fool. You absolute coward.")
        l_name = request.form.get("l_name")
        if not request.form.get("email"):
            return apology("Give me thine email you fool. You absolute coward.")
        elif (request.form.get("email")).find("@abschools.org", 0, len(request.form.get("email"))) == -1:
            return apology("Please use your abschools.org email")
        email = request.form.get("email")
        password = password_set(email)
        user = Dataentry(f_name, l_name, email, generate_password_hash(password), [])
        data = copy(user. __dict__ )
        del data["_sa_instance_state"]
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method=="POST":
        if not request.form.get("email"):
            return apology("Enter your email!!!", "/register")
        elif (request.form.get("email")).find("@abschools.org", 0, len(request.form.get("email"))) == -1:
            return apology("Please use your abschools.org email")
        em= request.form.get("email")
        if not request.form.get("password"):
            return apology("Enter a password!!!!")
        p = request.form.get("password")
        mail = Dataentry.query.filter_by(email = em).first()
        if check_password_hash(mail.password_hash, generate_password_hash(p)):
            return apology("invalid email and/or password ")
        session["email"] = request.form.get("email")
        db.session.commit()
        return redirect("/")
    return render_template("login.html")

@app.route('/reset_password', methods=['GET','POST'])
@login_required
def reset(): 
   if request.method=="POST":
        if not request.form.get("password"):
            return apology("Enter a password you fool. You absolute coward.")
        if not request.form.get("confirmation"):
            return apology("cOnFiRm Ur PaSsWoRd")
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("you fool!!! ur password and confirmed password don't match")
        password_hash = generate_password_hash(request.form.get("password"))
        mail = Dataentry.query.filter_by(email = em).first()
        mail.password_hash = password_hash
        db.session.commit()
   return render_template("reset_password.html", email=session["email"])
if __name__ == "__main__":
    app.run(debug=True)