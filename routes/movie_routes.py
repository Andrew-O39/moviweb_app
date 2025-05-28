from flask import render_template, request, redirect, url_for, flash, abort
from flask import current_app as app
from datamanager.utils import fetch_movie_details

def register_movie_routes(app):

    @app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
    def add_movie(user_id):
        """Add a new movie to a user's list of favorites."""
        user = app.data_manager.get_user_by_id(user_id)
        if not user:
            abort(404, description="User not found")

        if request.method == "POST":
            try:
                title = request.form.get("title", "").strip()
                if not title:
                    flash("Please enter a movie title.", "warning")
                    return redirect(url_for("add_movie", user_id=user_id))

                movie_data = fetch_movie_details(title)  # Call function that fetches details from API

                if not movie_data:
                    flash("Movie not found in OMDb or an error occurred.", "danger")
                    return redirect(url_for("add_movie", user_id=user_id))

                movie_data["user_id"] = user_id
                app.data_manager.add_movie(**movie_data)
                flash(f'Movie "{movie_data["name"]}" added successfully!', "success")
                return redirect(url_for("user_movies", user_id=user_id))

            except Exception as e:
                flash(f"An unexpected error occurred: {e}", "danger")
                return render_template("error.html", message=str(e))

        return render_template("add_movie.html", user_id=user_id)

    @app.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
    def update_movie(user_id, movie_id):
        """Update an existing movie in a user's list."""
        user = app.data_manager.get_user_by_id(user_id)
        movie = app.data_manager.get_movie_by_id(movie_id)

        if not user or not movie or movie.user_id != user.id:
            abort(404, description="User or Movie not found")

        if request.method == "POST":
            try:
                updated_data = {
                    "name": request.form["name"],
                    "director": request.form["director"],
                    "year": int(request.form["year"]),
                    "rating": float(request.form["rating"]),
                }
                app.data_manager.update_movie(movie_id, updated_data)
                flash(f'Movie "{movie.name}" updated successfully!', 'success')
                return redirect(url_for("user_movies", user_id=user.id))
            except Exception as e:
                return render_template("error.html", message=f"Failed to update movie: {e}")

        return render_template("update_movie.html", user_id=user_id, movie=movie)


    @app.route("/users/<int:user_id>/delete_movie/<int:movie_id>", methods=["POST"])
    def delete_movie(user_id, movie_id):
        """Delete a movie from a user's list of favorites."""
        user = app.data_manager.get_user_by_id(user_id)
        movie = app.data_manager.get_movie_by_id(movie_id)

        if not user or not movie or movie.user_id != user.id:
            abort(404, description="User or Movie not found")

        try:
            movie_name = movie.name
            app.data_manager.delete_movie(movie_id)
            flash(f'Movie "{movie_name}" deleted successfully!', 'success')
        except Exception as e:
            return render_template("error.html", message=f"Failed to delete movie: {e}")

        return redirect(url_for("user_movies", user_id=user.id))