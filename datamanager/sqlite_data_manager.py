
from datamanager.data_manager_interface import DataManagerInterface
from app_models import db, User, Movie

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_uri):
        self.db_uri = db_uri

    def get_all_users(self):
        return User.query.all()

    def get_user_by_id(self, user_id):
        return db.session.get(User, user_id)

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def add_movie(self, movie_data):
        movie = Movie(**movie_data)
        db.session.add(movie)
        db.session.commit()

    def get_movie_by_id(self, movie_id):
        return db.session.get(Movie, movie_id)

    def update_movie(self, movie_id, updated_data):
        movie = self.get_movie_by_id(movie_id)
        if movie:
            for key, value in updated_data.items():
                setattr(movie, key, value)
            db.session.commit()

    def delete_movie(self, movie_id):
        movie = self.get_movie_by_id(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()