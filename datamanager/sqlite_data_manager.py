
from datamanager.data_manager_interface import DataManagerInterface
from app_models import db, User, Movie

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_uri):
        self.db_uri = db_uri  # Not used directly, SQLAlchemy handles this

    def get_all_users(self):
        return User.query.all()

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_user(self, user):
        db.session.add(user)
        db.session.commit()

    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie):
        db.session.commit()

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()