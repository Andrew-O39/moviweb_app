from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """Represents a user of the MovieWeb app.
        Attributes:
        id (int): Primary key, unique identifier for the user.
        name (str): The name of the user.
        movies (List[Movie]): List of movies added by the user.
        reviews (List[Review]): List of reviews written by the user."""

    __tablename__ = 'users' # Define table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # One-to-many relationship with movies
    movies = db.relationship('Movie', back_populates='user', cascade='all, delete-orphan')

    # One-to-many relationship with reviews
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User {self.id}: {self.name}>"


class Movie(db.Model):
    """Represents a movie entry created by a user.
    Attributes:
        id (int): Primary key, unique identifier for the movie.
        name (str): Title of the movie.
        director (str): Director of the movie.
        year (int): Release year of the movie.
        rating (float): Rating given to the movie by the user.
        poster_url (str): URL to the movie poster image.
        user_id (int): Foreign key to the user who added the movie.
        user (User): The user who added the movie.
        reviews (List[Review]): List of reviews associated with this movie.
    """
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    poster_url = db.Column(db.String(300))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship back to the user who added the movie
    user = db.relationship('User', back_populates='movies')

    # One-to-many relationship with reviews
    reviews = db.relationship('Review', back_populates='movie', cascade='all, delete-orphan')
    def __repr__(self):
        return f"<Movie {self.id}: {self.name} ({self.year}) - Rating: {self.rating}>"


class Review(db.Model):
    """Represents a review written by a user for a specific movie.
    Attributes:
        id (int): Primary key, unique identifier for the review.
        user_id (int): Foreign key referencing the reviewing user.
        movie_id (int): Foreign key referencing the reviewed movie.
        review_text (str): The written review content.
        rating (float): Rating given by the user for the movie.
        user (User): The user who wrote the review.
        movie (Movie): The movie being reviewed."""

    __tablename__ = "reviews"  # Define table name

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship back to the user who wrote the review
    user = db.relationship('User', back_populates='reviews')

    # Relationship back to the reviewed movie
    movie = db.relationship('Movie', back_populates='reviews')

    def __repr__(self):
        return f"<Review {self.id} - User {self.user_id} - Movie {self.movie_id}>"