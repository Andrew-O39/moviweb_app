from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Define relationships
    movies = db.relationship('Movie', back_populates='user', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')

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

    # Add relationship
    user = db.relationship('User', back_populates='movies')
    reviews = db.relationship('Review', back_populates='movie', cascade='all, delete-orphan')
    def __repr__(self):
        return f"<Movie {self.id}: {self.name} ({self.year}) - Rating: {self.rating}>"


class Review(db.Model):
    __tablename__ = "reviews"  # Table name

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Define relationships
    user = db.relationship('User', back_populates='reviews')
    movie = db.relationship('Movie', back_populates='reviews')

    def __repr__(self):
        return f"<Review {self.id} - User {self.user_id} - Movie {self.movie_id}>"