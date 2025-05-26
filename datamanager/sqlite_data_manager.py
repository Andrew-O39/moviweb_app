
from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface
from app_models import User, Movie

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all_users(self):
        return User.query.all()

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_user(self, user):
        self.db.session.add(user)
        self.db.session.commit()

    def add_movie(self, movie):
        self.db.session.add(movie)
        self.db.session.commit()

    def update_movie(self, movie):
        # Assumes movie is an instance of Movie with the correct id already loaded
        existing = Movie.query.get(movie.id)
        if not existing:
            return False
        existing.name = movie.name
        existing.director = movie.director
        existing.year = movie.year
        existing.rating = movie.rating
        self.db.session.commit()
        return True

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()
            return True
        return False