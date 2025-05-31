from flask import Blueprint, render_template, request, redirect, session, url_for, flash, abort, current_app
from flask_login import login_required, current_user


review_bp = Blueprint("review", __name__, url_prefix="/reviews")


@review_bp.route("/add/<int:user_id>/<int:movie_id>", methods=["GET", "POST"])
def add_review(user_id, movie_id):
    """
    Allow a logged-in user to add a review to one of their movies.
    Args:
        user_id (int): ID of the user adding the review.
        movie_id (int): ID of the movie to be reviewed.
    Returns:
        Rendered template for adding a review or redirect to user's movies page on success.
    """
    # Ensure the logged-in user matches the user_id in URL
    if "user_id" not in session:
        flash("You must be logged in to add a review.", "danger")
        return redirect(url_for("auth.login"))

    if session["user_id"] != user_id:
        flash("You can only add reviews for your own movies.", "danger")
        return redirect(url_for("user.user_movies", user_id=current_user.id))

    user = current_app.data_manager.get_user_by_id(user_id)
    movie = current_app.data_manager.get_movie_by_id(movie_id)

    if not user or not movie or movie.user_id != user_id:
        abort(404, description="User or Movie not found or mismatch")

    if request.method == "POST":
        review_text = request.form.get("review_text", "").strip()
        rating_str = request.form.get("rating", "").strip()

        if not review_text:
            flash("Review text cannot be empty.", "warning")
            return render_template("add_review.html", user=user, movie=movie, review_text=review_text)

        try:
            rating = float(rating_str) if rating_str else None
            if rating is not None and not (0 <= rating <= 10):
                raise ValueError("Rating must be between 0 and 10.")
        except ValueError:
            flash("Invalid rating. Please enter a number between 0 and 10.", "danger")
            return render_template("add_review.html", user=user, movie=movie, review_text=review_text)

        try:
            current_app.data_manager.add_review(user_id, movie_id, review_text, rating)
            flash("Review added successfully!", "success")
            return redirect(url_for("review.view_reviews", movie_id=movie.id))
        except Exception as e:
            flash(f"Failed to add review: {e}", "danger")

    return render_template("add_review.html", user=user, movie=movie)


@review_bp.route("/movie/<int:movie_id>")
def view_reviews(movie_id):
    """
    Display all reviews for a given movie.
    Args:
        movie_id (int): The ID of the movie whose reviews are to be displayed.
    Returns:
        Rendered template showing the movie and its reviews.
        Raises 404 if the movie is not found.
    """
    movie = current_app.data_manager.get_movie_by_id(movie_id)
    if not movie:
        flash("Movie not found.", "danger")
        return redirect(url_for("main.home"))

    reviews = current_app.data_manager.get_reviews_for_movie(movie_id)
    return render_template("view_reviews.html", movie=movie, reviews=reviews)


@review_bp.route("/edit/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    """
    Allow the owner of a review to edit their review.
    Args:
        review_id (int): The ID of the review to be edited.
    Returns:
        On GET: Rendered template for editing the review.
        On POST: Redirects to movie review page on success or reloads form with errors.
    Raises:
        404: If the review does not exist.
        Redirects with flash message if user attempts to edit someone else's review.
    """
    # Ensure the logged-in user matches the user_id in URL
    if "user_id" not in session:
        flash("You must be logged in to edit reviews.", "danger")
        return redirect(url_for("auth.login"))

    review = current_app.data_manager.get_review_by_id(review_id)
    if not review:
        abort(404, description="Review not found")

    # Check that the logged-in user owns the review before allowing edit
    if session.get("user_id") != review.user_id:
        flash("You can only edit your own reviews.", "danger")
        return redirect(url_for("review.view_reviews", movie_id=review.movie_id))

    movie = review.movie
    user = review.user

    if request.method == "POST":
        review_text = request.form.get("review_text", "").strip()
        rating_str = request.form.get("rating", "").strip()

        if not review_text:
            flash("Review text cannot be empty.", "danger")
            return render_template("edit_review.html", review=review, movie=movie, user=user)

        try:
            rating = float(rating_str)
            if not (0 <= rating <= 10):
                raise ValueError("Rating must be between 0 and 10.")
        except ValueError:
            flash("Invalid rating. Please enter a number between 0 and 10.", "danger")
            return render_template("edit_review.html", review=review, movie=movie, user=user)

        try:
            current_app.data_manager.update_review(review_id, review_text, None)
            flash("Review updated successfully.", "success")
            return redirect(url_for("review.view_reviews", movie_id=movie.id))
        except Exception as e:
            flash(f"Failed to update review: {e}", "danger")

    return render_template("edit_review.html", review=review, movie=movie, user=user)


@review_bp.route("/delete/<int:review_id>", methods=["POST"])
def delete_review(review_id):
    """
    Delete a specific review from the database.
    This route handles POST requests to delete a review by its ID.
    If the review does not exist, it returns a 404 error.
    Upon successful deletion, the user is redirected to the movie's reviews page.
    Args:
        review_id (int): The ID of the review to be deleted.
    Returns:
        A redirect response to the movie's reviews page, or an error flash message if deletion fails.
    """
    review = current_app.data_manager.get_review_by_id(review_id)
    if not review:
        abort(404, description="Review not found")

    movie_id = review.movie_id

    try:
        current_app.data_manager.delete_review(review_id)
        flash("Review deleted successfully.", "success")
    except Exception as e:
        flash(f"Failed to delete review: {e}", "danger")

    return redirect(url_for("review.view_reviews", movie_id=movie_id))

