from routes.user_routes import user_bp
from routes.movie_routes import movie_bp
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.review_routes import review_bp

"""
Package initialization for the routes module.
This module registers all Flask blueprints for the application.
"""

def register_routes(app):
    """
    Register all application blueprints to the Flask app instance.
    Args:
        app (Flask): The Flask application instance.
    """
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(review_bp)

