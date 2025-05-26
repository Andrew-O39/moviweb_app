from flask import Flask, render_template
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
        return "🎬 Welcome to MoviWebApp!"

    @app.route("/users")
    def list_users():
        users = app.data_manager.get_all_users()
        return render_template("users.html", users=users)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)