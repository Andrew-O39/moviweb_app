from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """Represents a user of the MovieWeb app.
    Attributes:
        id (int): Primary key, unique identifier for the user.
        name (str): The name of the user.
        email (str): User's unique email address.
        movies (List[Movie]): List of movies added by the user.
        reviews (List[Review]): List of reviews written by the user.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Relationships:
    # movies: One-to-many relationship with Movie, deletes movies if user is deleted
    # reviews: One-to-many relationship with Review, deletes reviews if user is deleted
    movies = db.relationship("Movie", back_populates="user", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.id}: {self.name}>"


class Movie(db.Model):
    """Represents a movie entry created by a user.
    Attributes:
        id (int): Primary key, unique identifier for the movie.
        user_id (int): Foreign key to the user who added the movie.
        name (str): Title of the movie.
        director (str): Director of the movie.
        year (int): Release year of the movie.
        rating (float): Rating given to the movie by the user.
        poster_url (str): URL to the movie poster image.
        user (User): The user who added the movie.
        reviews (List[Review]): List of reviews associated with this movie
    Notes:
        - There is a uniqueness constraint ensuring a user cannot add the same movie name twice.
        - Cascade delete is enabled so deleting a movie removes its reviews automatically..
    """

    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    director = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    poster_url = db.Column(db.String(255))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'name', name='uix_user_movie'),
    )

    # user: Many-to-one relationship back to User
    # reviews: One-to-many relationship with Review, deletes reviews if movie is deleted
    user = db.relationship("User", back_populates="movies")
    reviews = db.relationship("Review", back_populates="movie", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Movie {self.id}: {self.name} ({self.year}) - Rating: {self.rating}>"


class Review(db.Model):
    """Represents a review written by a user for a specific movie.
    Attributes:
        id (int): Primary key, unique identifier for the review.
        review_text (str): The written review content.
        created_at (datetime): Timestamp when the review was created.
        user_id (int): Foreign key referencing the reviewing user.
        movie_id (int): Foreign key referencing the reviewed movie.
        user (User): The user who wrote the review.
        movie (Movie): The movie being reviewed.
    """

    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=True)  # Allow users to skip if they want
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationships:
    # user: Many-to-one relationship back to User
    # movie: Many-to-one relationship back to Movie
    user = db.relationship("User", back_populates="reviews")
    movie = db.relationship("Movie", back_populates="reviews")

    def __repr__(self):
        return f"<Review {self.id} - User {self.user_id} - Movie {self.movie_id}>"