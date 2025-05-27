from datamanager.data_manager_interface import DataManagerInterface
from app_models import db, User, Movie

class SQLiteDataManager(DataManagerInterface):
    """This class handles database operations for users and movies."""
    def __init__(self, db_uri):
        self.db_uri = db_uri

    def get_all_users(self):
        """Return all users."""
        return User.query.all()

    def get_user_by_id(self, user_id):
        """Retrieve a user from the database using their ID.
        Returns user if user object is found, otherwise None."""
        return db.session.get(User, user_id)

    def get_user_movies(self, user_id):
        """Return movies belonging to a specific user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_user(self, name):
        """Add a new user to database."""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def add_movie(self, user_id, name, director, year, rating, poster_url=None):
        """Add a movie to a user's list."""
        new_movie = Movie(
            name=name,
            director=director,
            year=int(year),
            rating=float(rating),
            user_id=user_id,
            poster_url=poster_url
        )
        db.session.add(new_movie)
        db.session.commit()

    def get_movie_by_id(self, movie_id):
        """Return a movie by ID."""
        return db.session.get(Movie, movie_id)

    def update_movie(self, movie_id, updated_data):
        """Update an existing movie."""
        movie = self.get_movie_by_id(movie_id)
        if movie:
            for key, value in updated_data.items():
                setattr(movie, key, value)
            db.session.commit()

    def delete_movie(self, movie_id):
        """Delete a movie by ID."""
        movie = self.get_movie_by_id(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()

    def delete_user(self, user_id):
        """Delete a user by ID."""
        # Delete all movies belonging to the user first
        Movie.query.filter_by(user_id=user_id).delete()
        # Then delete the user
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()