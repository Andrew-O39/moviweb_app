from flask import render_template, request, redirect, url_for, flash, abort
from flask import current_app as app
from datamanager.utils import fetch_movie_details

def register_review_routes(app):
    """Registers review-related routes with the Flask application.
    Enables functionality for adding, viewing, editing, and deleting
    reviews associated with specific movies and users.
    Args:
        app (Flask): The Flask application instance."""


    @app.route('/users/<int:user_id>/movies/<int:movie_id>/add_review', methods=['GET', 'POST'])
    def add_review(user_id, movie_id):
        """Add a new review for a specific movie by a user.
        Args:
            user_id (int): ID of the user submitting the review.
            movie_id (int): ID of the movie being reviewed.
        Returns:
            Render the review form on GET.
            Redirect to user's movies page on successful POST."""
        user = app.data_manager.get_user_by_id(user_id)
        movie = app.data_manager.get_movie_by_id(movie_id)

        if not user or not movie:
            abort(404, description="User or Movie not found")

        if request.method == "POST":
            review_text = request.form.get("review_text", "").strip()
            rating_str = request.form.get("rating", "").strip()

            # Validate rating input
            try:
                rating = float(rating_str)
            except ValueError:
                flash("Rating must be a number.", "danger")
                return render_template("add_review.html", user=user, movie=movie, review_text=review_text,
                                       rating=rating_str)

            try:
                app.data_manager.add_review(user_id, movie_id, review_text, rating)
                flash("Review added successfully!", "success")
                return redirect(url_for("user_movies", user_id=user.id))
            except Exception as e:
                flash(f"Failed to add review: {e}", "danger")

        # GET or failed POST: render the form
        return render_template("add_review.html", user=user, movie=movie)


    @app.route('/movies/<int:movie_id>/reviews')
    def view_reviews(movie_id):
        """Display all reviews for a specific movie.
        Args:
            movie_id (int): ID of the movie whose reviews to display.
        Returns:
            Render a template showing the movie and its reviews."""
        try:
            movie = app.data_manager.get_movie_by_id(movie_id)
            if not movie:
                flash("Movie not found.", "warning")
                return redirect(url_for("list_users"))

            reviews = app.data_manager.get_reviews_for_movie(movie_id)
            return render_template("view_reviews.html", movie=movie, reviews=reviews)

        except Exception as e:
            app.logger.error(f"Error retrieving reviews for movie {movie_id}: {e}")
            flash("An error occurred while loading reviews.", "danger")
            return redirect(url_for("list_users"))


    @app.route('/reviews/<int:review_id>/delete', methods=['POST'])
    def delete_review(review_id):
        """Delete a review by its ID.
        Args:
            review_id (int): ID of the review to delete.
        Returns:
            Redirect to the movie's review page after deletion."""
        review = app.data_manager.get_review_by_id(review_id)
        if not review:
            abort(404, description="Review not found")

        movie_id = review.movie_id
        try:
            app.data_manager.delete_review(review_id)
            flash("Review deleted successfully.", "success")
        except Exception as e:
            flash(f"Failed to delete review: {e}", "danger")

        return redirect(url_for("view_reviews", movie_id=movie_id))


    @app.route('/reviews/<int:review_id>/edit', methods=['GET', 'POST'])
    def edit_review(review_id):
        """Edit an existing review.
        Args:
            review_id (int): ID of the review to edit.
        Returns:
            Render edit form on GET.
            Redirect to movie's review page on successful POST."""
        review = app.data_manager.get_review_by_id(review_id)
        if not review:
            abort(404, description="Review not found")

        user = review.user
        movie = review.movie

        if request.method == "POST":
            review_text = request.form.get("review_text", "").strip()
            rating_str = request.form.get("rating", "").strip()

            try:
                rating = float(rating_str)
            except ValueError:
                flash("Rating must be a number.", "danger")
                return render_template("edit_review.html", review=review, user=user, movie=movie)

            try:
                app.data_manager.update_review(review_id, review_text, rating)
                flash("Review updated successfully.", "success")
                return redirect(url_for("view_reviews", movie_id=review.movie_id))
            except Exception as e:
                flash(f"Failed to update review: {e}", "danger")

        return render_template("edit_review.html", review=review, user=user, movie=movie)