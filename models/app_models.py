from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from moviweb_app import db

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.id}: {self.name}>"


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    poster_url = db.Column(db.String(300))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Movie {self.id}: {self.name} ({self.year}) - Rating: {self.rating}>"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    movie = db.relationship('Movie', backref=db.backref('reviews', lazy=True))