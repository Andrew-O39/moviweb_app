from flask import (Blueprint, render_template, request, redirect, url_for,
                   flash, abort, session, current_app,)

user_bp = Blueprint("user", __name__)

@user_bp.route("/users")
def list_users():
    """Display a list of all users.
    Only accessible after login."""
    try:
        users = current_app.data_manager.get_all_users()
        return render_template("users.html", users=users)
    except Exception as e:
        current_app.logger.error(f"Failed to load users: {e}")
        return render_template("error.html", message="Unable to load users at the moment.")


@user_bp.route("/<int:user_id>")
def user_movies(user_id):
    """
    Display a list of movies for the currently logged-in user.
    Ensures that users can only access their own movie list.
    """
    current_user_id = session.get("user_id")

    if not current_user_id:
        flash("You need to log in first.", "warning")
        return redirect(url_for("auth.login"))

    # Redirect to the correct user's own page if mismatch
    if current_user_id != user_id:
        flash("Access denied: You can only view your own movies.", "danger")
        return redirect(url_for("user.user_movies", user_id=current_user_id))

    try:
        user = current_app.data_manager.get_user_by_id(current_user_id)
        if not user:
            abort(404, description="User not found")

        movies = current_app.data_manager.get_user_movies(current_user_id)
        return render_template("user_movies.html", user=user, movies=movies)

    except Exception as e:
        current_app.logger.error(f"Error loading movies for user {current_user_id}: {e}")
        flash("An error occurred while loading your movies.", "danger")
        return render_template("error.html", message="An error occurred while loading your movies.")


@user_bp.route("/add", methods=["GET", "POST"])
def add_user():
    """
    Register a new user in the application.
    Prevents logged-in users from re-registering. Validates form inputs
    and handles user creation errors gracefully.
    """
    if session.get("user_id"):
        flash("You are already logged in.", "info")
        return redirect(url_for("user.user_movies", user_id=session["user_id"]))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()

        if not name or not email:
            flash("Name and email are required.", "warning")
            return render_template("add_user.html")

        try:
            user = current_app.data_manager.add_user(name, email)
            # Set session so user is logged in immediately
            session["user_id"] = user.id

            flash(f"User {user.name} added successfully!", "success")
            return redirect(url_for("user.user_movies", user_id=user.id))

        except ValueError as ve:
            flash(str(ve), "danger")  # For duplicate email
        except Exception as e:
            current_app.logger.error(f"Failed to add user: {e}")
            flash("An unexpected error occurred.", "danger")

    return render_template("add_user.html")

