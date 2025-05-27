from flask import Flask, flash, render_template, request, redirect, url_for, abort
from datamanager.sqlite_data_manager import SQLiteDataManager
from app_models import db, User, Movie
from datamanager.utils import fetch_movie_details
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        app.data_manager = SQLiteDataManager(app.config['SQLALCHEMY_DATABASE_URI'])

    # Define routes inside app context
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/users")
    def list_users():
        users = app.data_manager.get_all_users()
        return render_template("users.html", users=users)


    @app.route("/users/<int:user_id>")
    def user_movies(user_id):
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


    @app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])


    @app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
    def add_movie(user_id):
        user = app.data_manager.get_user_by_id(user_id)
        if not user:
            abort(404, description="User not found")

        if request.method == "POST":
            try:
                title = request.form.get("title", "").strip()
                if not title:
                    flash("Please enter a movie title.", "warning")
                    return redirect(url_for("add_movie", user_id=user_id))

                movie_data = fetch_movie_details(title) # Call function that fetches details from API

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

    from flask import current_app

    @app.route("/delete_user/<int:user_id>", methods=["POST"])
    def delete_user(user_id):
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


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', message=getattr(e, 'description', 'Page not found.')), 404


    @app.errorhandler(500)
    def internal_error(e):
        return render_template('500.html', message="An internal server error occurred."), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)