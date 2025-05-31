from dotenv import load_dotenv
from flask import Flask
from models.app_models import db
from flask_migrate import Migrate
import os
from datamanager.sqlite_data_manager import SQLiteDataManager
from routes import register_routes
from routes.error_handlers import register_error_handlers


load_dotenv()

migrate = Migrate()

def create_app():
    """Application factory function.
    Configures the Flask application, sets up extensions like SQLAlchemy,
    initializes the database, and registers all route blueprints and error handlers.
    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Check for required environment variables
    if not app.config["SECRET_KEY"]:
        raise RuntimeError("SECRET_KEY not set in environment variables")
    if not app.config["SQLALCHEMY_DATABASE_URI"]:
        raise RuntimeError("DATABASE_URL not set in environment variables")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Data Manager, Blueprints, and Error Handlers within context
    with app.app_context():
        db.create_all()
        app.data_manager = SQLiteDataManager(db)
        register_routes(app)  # Register all blueprints via the helper function (register_routes)
        register_error_handlers(app)  # Register global error handlers

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)