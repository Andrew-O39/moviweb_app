from flask import Blueprint, render_template, session, redirect, url_for, current_app, flash
from models.app_models import db, User
from flask_sqlalchemy import SQLAlchemy

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """
    Render the welcome page.
    Redirects to dashboard if session exists and user is valid.
    """
    user_id = session.get("user_id")

    if user_id:
        user = current_app.data_manager.get_user_by_id(user_id)
        if user:
            return redirect(url_for("user.user_movies", user_id=user.id))
        else:
            # Clear invalid session if user doesn't exist
            session.pop("user_id", None)

    return render_template("index.html")