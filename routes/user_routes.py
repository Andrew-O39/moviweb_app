from flask import render_template, request, redirect, url_for, flash, abort
from flask import current_app as app

def register_user_routes(app):
    """Register user-related routes to the Flask app.
        Args:
            app (Flask): The Flask application instance."""

    @app.route("/users")
    def list_users():
        """"Display a list of all registered users.
        Retrieves all users from the database and renders
        the users page showing each user's name and links
        to their respective movie lists.
        Returns:
            Response: Rendered template with the list of users."""
        users = app.data_manager.get_all_users()
        return render_template("users.html", users=users)


    @app.route("/users/<int:user_id>")
    def user_movies(user_id):
        """Display all movies associated with a specific user.
            Fetches the user by ID and retrieves their movies from the database.
            Renders a page listing the user's favorite movies with details
            such as name, director, year, rating, and actions.
            Args:
                user_id (int): The ID of the user whose movies are to be displayed.
            Returns:
                Response: Rendered template showing the user's movies."""
        try:
            user = app.data_manager.get_user_by_id(user_id)
            if not user:
                abort(404, description="User not found")

            movies = app.data_manager.get_user_movies(user_id)
            return render_template("user_movies.html", user=user, movies=movies)

        except Exception as e:
            return render_template("error.html", message=f"Could not load user movies: {e}")


    @app.route("/add_user", methods=["GET", "POST"])
    def add_user():
        """Handle adding a new user to the application.
        GET: Render the form for adding a new user.
        POST: Process the submitted form data and create a new user.
        Returns:
            Response: Redirect to users list on success or
                  re-render form with errors on failure."""
        if request.method == "POST":
            name = request.form.get("name")
            if not name:
                return render_template("error.html", message="Name is required.")

            try:
                app.data_manager.add_user(name)
                return redirect(url_for("list_users"))
            except Exception as e:
                return render_template("error.html", message=f"Failed to add user: {e}")

        return render_template("add_user.html")


    @app.route("/delete_user/<int:user_id>", methods=["POST"])
    def delete_user(user_id):
        """Delete a user and all their associated movies from the database.
        Args:
            user_id (int): The ID of the user to delete.
        Returns:
            Response: Redirect to the users list page after deletion."""
        user = app.data_manager.get_user_by_id(user_id)
        if not user:
            abort(404, description="User not found")

        try:
            user_name = user.name
            app.data_manager.delete_user(user_id)
            flash(f'User "{user_name}" and all their movies deleted successfully.', "success")
        except Exception as e:
            return render_template("error.html", message=f"Failed to delete user: {e}")

        return redirect(url_for("list_users"))

