from flask import render_template, redirect, session
from functools import wraps

def apology(message, code):
    return render_template("apology.html", code=code, message=message), code

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") == None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
