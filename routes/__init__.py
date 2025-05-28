from .user_routes import register_user_routes
from .movie_routes import register_movie_routes
from .error_handlers import register_error_handlers
from .main_routes import register_main_routes
from .review_routes import register_review_routes

def register_routes(app):
    """Registers all route groups and error handlers with the Flask application.
        This function attaches user, movie, main, review, and error routes
        to the given Flask app instance. It acts as a centralized point to
        keep route registration organized.
        Args:
            app (Flask): The Flask application instance to which routes are registered."""
    register_user_routes(app)
    register_movie_routes(app)
    register_error_handlers(app)
    register_main_routes(app)
    register_review_routes(app)