from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, session, current_app
from routes.auth_utils import login_required
from datamanager.sqlite_data_manager import SQLiteDataManager
from datamanager.utils import fetch_movie_details

movie_bp = Blueprint("movie", __name__)

@movie_bp.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id):
    """
    Add a new movie to the logged-in user's movie list.
    Ensures only the current user can add to their own list, fetches movie
    details from OMDb, and handles any errors that may occur.
    """
    if session.get("user_id") != user_id:
        flash("You can only add movies to your own list.", "danger")
        return redirect(url_for("user.user_movies", user_id=session.get("user_id")))

    user = current_app.data_manager.get_user_by_id(user_id)
    if not user:
        abort(404, description="User not found")

    if request.method == "POST":
        title = request.form.get("title", "").strip()

        if not title:
            flash("Please enter a movie title.", "warning")
            return redirect(url_for("movie.add_movie", user_id=user_id))

        movie_data = fetch_movie_details(title)
        if not movie_data:
            flash("Movie not found in OMDb or an error occurred.", "danger")
            return redirect(url_for("movie.add_movie", user_id=user_id))

        movie_data["user_id"] = user_id  # Ensure the movie is tied to the current user

        try:
            current_app.data_manager.add_movie(**movie_data)
            flash(f'Movie "{movie_data["name"]}" added successfully!', "success")
            return redirect(url_for("user.user_movies", user_id=user_id))
        except ValueError as ve:
            flash(str(ve), "warning")
        except Exception as e:
            current_app.logger.error(f"Movie addition failed: {e}")
            flash("An unexpected error occurred while adding the movie.", "danger")

        return redirect(url_for("movie.add_movie", user_id=user_id))

    return render_template("add_movie.html", user=user)


@movie_bp.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    """
    Update an existing movie in a user's collection.
    Only the owner of the movie (logged-in user) can update it.
    """
    # Ensure only the logged-in user can update their own movies
    if session.get("user_id") != user_id:
        flash("You can only update your own movies.", "danger")
        return redirect(url_for("user.user_movies", user_id=session.get("user_id")))

    user = current_app.data_manager.get_user_by_id(user_id)
    movie = current_app.data_manager.get_movie_by_id(movie_id)

    # Ensure the movie exists and belongs to the user
    if not user or not movie or movie.user_id != user.id:
        abort(404, description="User or Movie not found")

    if request.method == "POST":
        try:
            # Get form data
            name = request.form.get("name", "").strip() or None
            director = request.form.get("director", "").strip() or None
            year_str = request.form.get("year", "").strip()
            rating_str = request.form.get("rating", "").strip()

            # Convert string inputs safely
            year = int(year_str) if year_str else None
            rating = float(rating_str) if rating_str else None

            # Validate rating range
            if rating is not None and not (0 <= rating <= 10):
                raise ValueError("Rating must be between 0 and 10.")

            # Perform update
            current_app.data_manager.update_movie(
                movie_id=movie_id,
                name=name,
                director=director,
                year=year,
                rating=rating,
            )

            flash(f'Movie "{name or movie.name}" updated successfully!', "success")
            return redirect(url_for("user.user_movies", user_id=user_id))

        except ValueError as ve:
            flash(str(ve), "warning")
        except Exception as e:
            return render_template("error.html", message=f"Failed to update movie: {e}")

    return render_template("update_movie.html", user_id=user_id, movie=movie)


@movie_bp.route("/users/<int:user_id>/delete_movie/<int:movie_id>", methods=["POST"])
def delete_movie(user_id, movie_id):
    """
    Delete a movie from a user's list. Restricted to the movie's owner.
    """
    # Ensure the logged-in user is the owner
    if session.get("user_id") != user_id:
        flash("You can only delete your own movies.", "danger")
        return redirect(url_for("user.user_movies", user_id=session.get("user_id")))

    user = current_app.data_manager.get_user_by_id(user_id)
    movie = current_app.data_manager.get_movie_by_id(movie_id)

    # Handle case where user or movie doesn't exist, or mismatch
    if not user or not movie or movie.user_id != user.id:
        abort(404, description="User or Movie not found")

    try:
        movie_name = movie.name
        current_app.data_manager.delete_movie(movie_id)
        flash(f'Movie "{movie_name}" deleted successfully!', "success")
    except Exception as e:
        # Show a general error page with the message
        return render_template("error.html", message=f"Failed to delete movie: {e}")

    return redirect(url_for("user.user_movies", user_id=user_id))
