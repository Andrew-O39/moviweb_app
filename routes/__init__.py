from .user_routes import register_user_routes
from .movie_routes import register_movie_routes
from .error_handlers import register_error_handlers
from .main_routes import register_main_routes
from .review_routes import register_review_routes

def register_routes(app):
    register_user_routes(app)
    register_movie_routes(app)
    register_error_handlers(app)
    register_main_routes(app)
    register_review_routes(app)