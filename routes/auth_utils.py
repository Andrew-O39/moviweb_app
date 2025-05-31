from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """
    Decorator to ensure that a user is logged in before accessing a route.
    This decorator checks for the presence of 'user_id' in the Flask session.
    If the user is not logged in, it flashes a warning message and redirects
    to the login page. It also handles unexpected exceptions gracefully by
    flashing an error message and redirecting to the login page.
    Args:
        f (function): The route function to decorate.
    Returns:
        function: The wrapped function that includes the login check.
    Raises:
        None: Exceptions are caught and handled internally.
    """
    # decorator implementation
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if "user_id" not in session:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for("auth.login"))
            return f(*args, **kwargs)
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", "danger")
            return redirect(url_for("auth.login"))
    return decorated_function


