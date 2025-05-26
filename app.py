from flask import Flask, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from app_models import db, User, Movie

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        app.data_manager = SQLiteDataManager(app.config['SQLALCHEMY_DATABASE_URI'])

    # Define routes inside app context
    @app.route("/")
    def home():
        return "Welcome to MovieWeb App!"

    @app.route("/users")
    def list_users():
        users = app.data_manager.get_all_users()
        return render_template("users.html", users=users)

    @app.route("/users/<int:user_id>")
    def user_movies(user_id):
        user = db.session.get(User, user_id)
        if not user:
            return f"User with ID {user_id} not found.", 404

        movies = app.data_manager.get_user_movies(user_id)
        return render_template("user_movies.html", user=user, movies=movies)

    from flask import request, redirect, url_for

    @app.route("/add_user", methods=["GET", "POST"])
    def add_user():
        if request.method == "POST":
            name = request.form.get("name")
            if name:
                app.data_manager.add_user(name)
                return redirect(url_for("list_users"))
            return "Name is required.", 400
        return render_template("add_user.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)