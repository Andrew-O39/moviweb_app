from flask import render_template, request, redirect, url_for, flash, abort
from flask import current_app as app

def register_user_routes(app):

    @app.route("/users")
    def list_users():
        """Display all users in the application."""
        users = app.data_manager.get_all_users()
        return render_template("users.html", users=users)


    @app.route("/users/<int:user_id>")
    def user_movies(user_id):
        """Display favorite movies for a specific user."""
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
        """Add a new user to the application."""
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
        """Delete a user and all associated movies."""
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

