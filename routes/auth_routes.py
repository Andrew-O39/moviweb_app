from flask import (Blueprint, render_template, request, redirect, url_for, flash, session,
                   current_app)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.
    On GET: render the login form.
    On POST: authenticate user by email and create a session.

    If user email is not found, flash an error message.
    """
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if not email:
            flash("Please enter your email address.", "warning")
            return render_template("login.html")

        user = current_app.data_manager.get_user_by_email(email)
        if user:
            session["user_id"] = user.id
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("user.user_movies", user_id=user.id))
        else:
            flash("User not found. Please check your email or register.", "danger")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """
    Log out the current user by clearing the session.
    Flashes a logout confirmation message and redirects to the home page.
    """
    try:
        session.pop("user_id", None)
        flash("Logged out successfully.", "info")
    except Exception as e:
        flash(f"An error occurred while logging out: {e}", "danger")
    return redirect(url_for("main.home"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    print("Reached register route")  # DEBUG
    if request.method == "POST":
        name = request.form.get("name").strip()
        email = request.form.get("email", "").strip().lower()

        if not name or not email:
            flash("Both name and email are required.", "warning")
            return render_template("register.html")

        existing_user = current_app.data_manager.get_user_by_email(email)
        if existing_user:
            flash("User already exists. Try logging in.", "info")
            return redirect(url_for("auth.login"))

        try:
            user = current_app.data_manager.add_user(name=name, email=email)
            session["user_id"] = user.id
            flash("Registration successful. Welcome!", "success")
            return redirect(url_for("user.user_movies", user_id=user.id))
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

    return render_template("register.html")