from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from models.app_models import db, User, Movie, Review
from flask_migrate import Migrate, migrate
from datamanager.sqlite_data_manager import SQLiteDataManager
from routes import register_routes

migrate = Migrate()

def create_app():
    """Application factory function.
        Configures the Flask application, sets up extensions like SQLAlchemy,
        initializes the database, and registers all route blueprints.
        Returns:
            Flask: Configured Flask application instance."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate with app and db

    with app.app_context():
        app.data_manager = SQLiteDataManager(app.config['SQLALCHEMY_DATABASE_URI'])
        register_routes(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)