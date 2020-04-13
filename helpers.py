from flask import redirect, render_template, request, session
from functools import wraps
import datetime
import psycopg2
import os
from random import randint
from flask_sqlalchemy import SQLAlchemy
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
def apology(message, url="/", code=400):
    def escape(s):
        
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", msg = message)
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
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
