from flask import redirect, render_template, request, session
from functools import wraps
import datetime
import psycopg2
import os
from random import randint
from flask_sqlalchemy import SQLAlchemy
def apology(message, url="/", code=400):
    def escape(s):
        
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", msg = message)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
