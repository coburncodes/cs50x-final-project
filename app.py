from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///hiker.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    id = session["user_id"]
    first_name = (db.execute("SELECT first_name FROM users WHERE id=?", id))[0]["first_name"]

    return render_template("index.html", first_name=first_name)

@app.route("/login", methods=["POST", "GET"])
def login():
    # Clear memory
    session.clear()

    # Save variables
    username = request.form.get("username")
    password = request.form.get("password")

    # If sending post request
    if request.method == "POST":
        # If no username
        if username == "":
            # Apologize
            return apology("input username", 400)
        # Else if no password
        elif password == "":
            # Apologize
            return apology("input password", 400)

        # Save user info
        found = db.execute("SELECT * FROM users WHERE username = ?", username)

        # If username is not in database
        if len(found) != 1:
            # Apologize
            return apology("invalid username", 400)
        # Otherwise username is in db
        else:
            # If password doesn't match hash
            if not check_password_hash(found[0]["hash"], password):
                # Apologize
                return apology("invalid password", 400)
            # Otherwise all checks pass
            else:
                # Save user_id
                session["user_id"] = found[0]["id"]
                # Return index.html
                return redirect("/")
    # Otherwise get request
    else:
        # Returns login page
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["POST", "GET"])
def register():
    # Save variables
    first_name = request.form.get("first_name")
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_pw = request.form.get("confirm")
    users = db.execute("SELECT username FROM users")

    # When page first loads
    if first_name == None:
        # Render template
        return render_template("register.html")
    # If user puts no first name
    elif first_name == "":
        # Apologize
        return apology("input first name", 400)
    # Otherwise user input first name
    else:
        # If user put no username
        if username == "":
            # Apologize
            return apology("input username", 400)
        # Otherwise user input username
        else:
            # Loop through usernames
            for row in users:
                # If user's input name is taken
                if username == row["username"]:
                    # Apologize
                        return apology("username taken", 400)
            # If password is blank
            if password == "":
                # Apologize
                return apology("input password", 400)
            # Otherwise user input pw
            else:
                # If confirm is blank
                if confirm_pw == "":
                    # Apologize
                    return apology("confirm password", 400)
                # Else if confirm doesn't match password
                elif not confirm_pw == password:
                    # Apologize
                    return apology("passwords don't match", 400)
                # Otherwise everything is input, username is free and pws match
                else:
                    # Input to users database
                    db.execute("INSERT INTO users (username, hash, first_name) VALUES (?, ?, ?)", username, generate_password_hash(password), first_name)
                    # Take user to login screen
                    return redirect("/")


@app.route("/all_hikes", methods=["POST", "GET"])
@login_required
def all():
    # Save id
    id = session["user_id"]
    # Create list of all hikes
    hikes = db.execute("SELECT * FROM hikes")
    # Create list of user's hikes
    my_hikes = db.execute("SELECT * FROM completed WHERE user_id=?", id)
    number = len(my_hikes)
    total_hikes = len(hikes)
    found = False

    # If user submits sort
    if request.method == "POST":
        # Save the variable
        sort = request.form.get("filter")

        # Orient data according to sort request
        if sort == "Region":
            hikes = db.execute("SELECT * FROM hikes ORDER BY area")
        if sort == "Name":
            hikes = db.execute("SELECT * FROM hikes ORDER BY name")
        if sort == "Difficulty":
            hikes = db.execute("SELECT * FROM hikes ORDER BY difficulty")
        if sort == "Distance":
            hikes = db.execute("SELECT * FROM hikes ORDER BY distance")
        if sort == "Elevation Change":
            hikes = db.execute("SELECT * FROM hikes ORDER BY elevation_change")

        # Render updated current page
        return render_template("all_hikes.html", hikes=hikes, my_hikes=my_hikes, number=number, total_hikes=total_hikes, sort=sort, db=db)

    # Else user is just viewing
    else:
        return render_template("all_hikes.html", hikes=hikes, my_hikes=my_hikes, number=number, total_hikes=total_hikes, found=found)


@app.route("/add_hike", methods=["POST", "GET"])
@login_required
def add():
    # Save variables
    id = session["user_id"]
    hikes_alpha = db.execute("SELECT * FROM hikes ORDER BY name")
    total_hikes = len(hikes_alpha)
    number = db.execute("SELECT hikes FROM users WHERE id=?", id)[0]["hikes"]

    # If user submits form
    if request.method == "POST":
        # Save variables from form
        name = request.form.get("hike")
        date = request.form.get("date")
        rating = request.form.get("rating")
        review = request.form.get("review")
        # If user inputs no date
        if date == "":
            # Apologize
            return apology("Input a date", 400)
        # Otherwise a date was input
        else:
            # Get id of submitted hike
            hike_id = (db.execute("SELECT id FROM hikes WHERE name=?", name))[0]["id"]
            # Create list of user's hikes
            my_hikes = db.execute("SELECT * FROM completed WHERE user_id=?", id)
            # If its first hike completed
            if len(my_hikes) < 1:
                # Add entry
                db.execute("INSERT INTO completed (user_id, hike_id, date, rating, review) VALUES (?, ?, ?, ?, ?)", id, hike_id, date, rating, review)
                # Increment counter
                number += 1
                # Update number of hikes
                db.execute("UPDATE users SET hikes=? WHERE id=?", number, id)
                # Send user to confirmation page
                return render_template("confirmed.html", name=name, number=number, total_hikes=total_hikes)
            # Otherwise not first completed
            else:
                # Loop over user's hikes
                for hike in my_hikes:
                    # If user already logged this
                    if int(hike_id) == hike["hike_id"]:
                        # Indicate
                        indicator = True
                        break
                    # Otherwise its new
                    else:
                        # Indicate
                        indicator = False
                # If input hike matched any hike in my_hikes
                if indicator == True:
                    # Apologize
                        return apology("Already completed this hike", 400)
                # Otherwise, hike is new to my_hikes
                else:
                    # Add to database
                    db.execute("INSERT INTO completed (user_id, hike_id, date, rating, review) VALUES (?, ?, ?, ?, ?)", id, hike_id, date, rating, review)
                    # Increment hike count
                    number += 1
                    # Update user's hike count
                    db.execute("UPDATE users SET hikes=? WHERE id=?", number, id)
                    # Send user to confirmation page
                    return render_template("confirmed.html", name=name, number=number, total_hikes=total_hikes)

    # Otherwise user reached page by GET
    else:
        # Render template
        return render_template("add_hike.html", hikes=hikes_alpha)


@app.route("/my_hikes", methods=["POST", "GET"])
@login_required
def my_hikes():
    # Save variables
    id = session["user_id"]
    my_hikes = db.execute("SELECT * FROM hikes INNER JOIN completed ON hikes.id=completed.hike_id WHERE hikes.id IN (SELECT hike_id FROM completed WHERE user_id=?)", id)
    hikes = db.execute("SELECT * FROM hikes")
    number = len(my_hikes)
    total_hikes = len(hikes)

    # If user submits sort
    if request.method == "POST":
        # Save the variable
        sort = request.form.get("filter")

        # Orient data according to sort request
        if sort == "Region":
            my_hikes = db.execute("SELECT * FROM hikes INNER JOIN completed ON hikes.id=completed.hike_id WHERE hikes.id IN (SELECT hike_id FROM completed WHERE user_id=?) ORDER BY area", id)
        if sort == "Name":
            my_hikes = db.execute("SELECT * FROM hikes INNER JOIN completed ON hikes.id=completed.hike_id WHERE hikes.id IN (SELECT hike_id FROM completed WHERE user_id=?) ORDER BY name", id)
        if sort == "Difficulty":
            my_hikes = db.execute("SELECT * FROM hikes INNER JOIN completed ON hikes.id=completed.hike_id WHERE hikes.id IN (SELECT hike_id FROM completed WHERE user_id=?) ORDER BY difficulty", id)
        if sort == "Rating":
            my_hikes = db.execute("SELECT * FROM hikes INNER JOIN completed ON hikes.id=completed.hike_id WHERE hikes.id IN (SELECT hike_id FROM completed WHERE user_id=?) ORDER BY rating", id)

        # Render page
        return render_template("my_hikes.html", my_hikes=my_hikes, db=db, id=id, number=number, total_hikes=total_hikes)

    # Otherwise reached by GET
    else:
        return render_template("my_hikes.html", my_hikes=my_hikes, db=db, id=id, number=number, total_hikes=total_hikes)





@app.route("/edit", methods=["POST", "GET"])
@login_required
def edit():
    id = session["user_id"]
    # Create list of user's hikes
    my_hikes = db.execute("SELECT * FROM completed WHERE user_id=?", id)
    # Save variables from form
    name = request.form.get("hike")
    date = request.form.get("date")
    review = request.form.get("review")
    rating = request.form.get("rating")

    # When user clicks update
    if request.method == "POST":
        # If user didn't enter date
        if date == "":
            # Apologize
            return apology("Input a date", 400)
        # Otherwise
        else:
            # Get hike's id from hikes database
            hike_id = (db.execute("SELECT id FROM hikes WHERE name=?", name))[0]["id"]
            # Get specific id from completed database
            completed_id = (db.execute("SELECT id FROM completed WHERE hike_id=? AND user_id=?", hike_id, id))[0]["id"]
            # Update the database
            db.execute("UPDATE completed SET date=?, rating=?, review=? WHERE id=?", date, rating, review, completed_id)
            # Return to my hikes
            return redirect("my_hikes")
    # Otherwise user reached page by GET request
    else:
        # Render edit page
        return render_template("edit.html", my_hikes=my_hikes, db=db)


@app.route("/delete", methods=["POST", "GET"])
@login_required
def delete():
    # Save variables
    id = session["user_id"]
    number = db.execute("SELECT hikes FROM users WHERE id=?", id)[0]["hikes"]
    # Create list of user's hikes
    my_hikes = db.execute("SELECT * FROM completed WHERE user_id=?", id)

    # When user clicks delete
    if request.method == "POST":
        # Save variables from form
        name = request.form.get("hike")
        # Get hike's id from hikes database
        hike_id = (db.execute("SELECT id FROM hikes WHERE name=?", name))[0]["id"]
        # Get specific id from completed database
        completed_id = (db.execute("SELECT id FROM completed WHERE hike_id=? AND user_id=?", hike_id, id))[0]["id"]
        # Update the database
        db.execute("DELETE FROM completed WHERE id=?", completed_id)
        # Decrement hike count
        number -= 1
        # Update user's hike count
        db.execute("UPDATE users SET hikes=? WHERE id=?", number, id)
        # Redirect to my_hikes
        return redirect("/my_hikes")

    # Otherwise user reached page by GET request
    else:
        # Render delete page
        return render_template("delete.html", my_hikes=my_hikes, db=db)



@app.route("/update_password", methods=["POST", "GET"])
@login_required
def update_password():
    # Save variables
    id=session["user_id"]

    # If user clicks submit
    if request.method == "POST":
        # Save variables
        new_password = request.form.get("password")
        new_confirm = request.form.get("confirm")
        # If the passwords don't match
        if not new_password == new_confirm:
            # Apologize
            return apology("Password must match confirmation", 400)
        # Otherwise they match
        else:
            db.execute("UPDATE users SET hash = ? WHERE id=?", generate_password_hash(new_password), id)
            # Set new var
            new_info = True
            # Return confirm page
            return render_template("confirmed.html", new_info=new_info)

    # Otherwise page reached by GET request
    else:
        # Render page
        return render_template("update_password.html")


@app.route("/update_name", methods=["POST", "GET"])
@login_required
def update_name():
    # Save variables
    id=session["user_id"]
    first_name = db.execute("SELECT first_name FROM users WHERE id=?", id)[0]["first_name"]
    username = db.execute("SELECT username FROM users WHERE id=?", id)[0]["username"]

    # If user clicks submit
    if request.method == "POST":
        # Save variables
        new_first = request.form.get("first_name")
        new_username = request.form.get("username")

        # If first name is blank
        if new_first == "":
            # Apologize
            return apology("First name cannot be blank", 400)
        # Else first name has value
        else:
            # If username is blank
            if new_username == "":
                # Apologize
                return apology("Username cannot be blank", 400)
            # Else username has value
            else:
                # Update the database
                db.execute("UPDATE users SET username = ?, first_name = ? WHERE id=?", new_username, new_first, id)
                # Set new var
                new_info = True
                # Return confirm page
                return render_template("confirmed.html", new_info=new_info)
    # Otherwise page reached by GET request
    else:
        # Render page
        return render_template("update_name.html", first_name=first_name, username=username)


@app.route("/account")
@login_required
def account():
    id = session["user_id"]
    first_name = db.execute("SELECT first_name FROM users WHERE id=?", id)[0]["first_name"]
    return render_template("account.html", first_name=first_name)