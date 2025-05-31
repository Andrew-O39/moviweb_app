from typing import Optional, List
from models.app_models import db, User, Movie, Review
from datamanager.data_manager_interface import DataManagerInterface

class SQLiteDataManager(DataManagerInterface):
    """Handles all database operations using Flask-SQLAlchemy's db.session."""

    def __init__(self, db_instance):
        """
        Initialize the data manager with a SQLAlchemy db instance.
        Args:
            db_instance (SQLAlchemy): The SQLAlchemy database instance.
        """
        self.db = db_instance

    def add_user(self, name: str, email: str) -> User:
        """
        Create and add a new user to the database.
        Args:
            name (str): User's name.
            email (str): User's email address.
        Returns:
            User: The created User object.
        """
        email = email.strip().lower()

        existing_user = self.get_user_by_email(email)
        if existing_user:
            raise ValueError("A user with that email already exists.")

        new_user = User(name=name.strip(), email=email)
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.
        Args:
            user_id (int): User ID.
        Returns:
            Optional[User]: User object if found, else None.
        """
        return User.query.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        Args:
            email (str): User email.
        Returns:
            Optional[User]: User object if found, else None.
        """
        return User.query.filter_by(email=email).first()

    def get_user_movies(self, user_id: int) -> List[Movie]:
        """
        Retrieve all movies associated with a user.
        Args:
            user_id (int): User ID.
        Returns:
            List[Movie]: List of Movie objects.
        """
        user = self.get_user_by_id(user_id)
        return user.movies if user else []

    def get_all_users(self) -> List[User]:
        """
        Retrieve all users in the database.
        Returns:
            List[User]: List of all User objects.
        """
        users = self.db.session.query(User).all()
        print("Fetched users:", users)
        return users

    def add_movie(self, user_id: int, **movie_data) -> Movie:
        """
        Add a new movie for a specific user.
        Args:
            user_id (int): User ID.
            movie_data: Arbitrary keyword arguments for Movie fields (name, director, year, rating, poster_url).
        Raises:
            ValueError: If the user already added a movie with the same name.
        Returns:
            Movie: The newly added Movie object.
        """
        existing = Movie.query.filter_by(user_id=user_id, name=movie_data.get('name')).first()
        if existing:
            raise ValueError(f'You have already added the movie "{movie_data.get("name")}".')

        new_movie = Movie(user_id=user_id, **movie_data)
        try:
            self.db.session.add(new_movie)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return new_movie

    def get_movie_by_id(self, movie_id: int) -> Optional[Movie]:
        """
        Retrieve a movie by its ID.
        Args:
            movie_id (int): Movie ID.
        Returns:
            Optional[Movie]: Movie object if found, else None.
        """
        return Movie.query.get(movie_id)

    def delete_movie(self, movie_id: int) -> None:
        """
        Delete a movie by its ID.
        Args:
            movie_id (int): Movie ID.
        """
        movie = self.get_movie_by_id(movie_id)
        if movie:
            try:
                self.db.session.delete(movie)
                self.db.session.commit()
            except Exception:
                self.db.session.rollback()
                raise

    def update_movie(
        self,
        movie_id: int,
        name: Optional[str] = None,
        director: Optional[str] = None,
        year: Optional[int] = None,
        rating: Optional[float] = None,
        poster_url: Optional[str] = None
    ) -> Optional[Movie]:
        """
        Update details of a movie.
        Args:
            movie_id (int): Movie ID.
            name (Optional[str]): New name.
            director (Optional[str]): New director.
            year (Optional[int]): New year.
            rating (Optional[float]): New rating.
            poster_url (Optional[str]): New poster URL.
        Returns:
            Optional[Movie]: Updated Movie object or None if not found.
        """
        movie = self.get_movie_by_id(movie_id)
        if not movie:
            return None
        if name is not None:
            movie.name = name
        if director is not None:
            movie.director = director
        if year is not None:
            movie.year = year
        if rating is not None:
            movie.rating = rating
        if poster_url is not None:
            movie.poster_url = poster_url

        try:
            self.db.session.commit()
        except Exception:
            self.db.session.rollback()
            raise
        return movie

    def add_review(self, user_id: int, movie_id: int, review_text: str, rating: Optional[float] = None) -> Review:
        """
        Add a new review for a movie by a user.
        Args:
            user_id (int): User ID.
            movie_id (int): Movie ID.
            review_text (str): Review content.
        Returns:
            Review: The created Review object.
        """
        review = Review(user_id=user_id, movie_id=movie_id, review_text=review_text, rating=rating)
        try:
            self.db.session.add(review)
            self.db.session.commit()
        except Exception:
            self.db.session.rollback()
            raise
        return review

    def get_review_by_id(self, review_id: int) -> Optional[Review]:
        """
        Retrieve a review by its ID.
        Args:
            review_id (int): Review ID.
        Returns:
            Optional[Review]: Review object if found, else None.
        """
        return Review.query.get(review_id)

    def get_reviews_for_movie(self, movie_id: int) -> List[Review]:
        """
        Retrieve all reviews for all movie records with the same name
        (i.e., shared reviews across users who added the same-titled movie).
        Args:
            movie_id (int): Movie ID used to find the shared title.
        Returns:
            List[Review]: List of Review objects across all matching movies.
        """
        # Find the movie by ID
        movie = self.get_movie_by_id(movie_id)
        if not movie:
            return []

        # Find all movies with the same name
        matching_movies = self.db.session.query(Movie).filter_by(name=movie.name).all()
        matching_ids = [m.id for m in matching_movies]

        # Return all reviews for those movie IDs
        return self.db.session.query(Review).filter(Review.movie_id.in_(matching_ids)).all()

    def update_review(self, review_id: int, review_text: str, rating: Optional[float] = None) -> Optional[Review]:
        """
        Update a review's text and optional rating.
        Args:
            review_id (int): Review ID.
            review_text (str): New review text.
            rating (Optional[float]): New rating.
        Returns:
            Optional[Review]: Updated Review object or None if not found.
        """
        review = self.get_review_by_id(review_id)
        if review:
            review.review_text = review_text
            if rating is not None:
                review.rating = rating
            try:
                self.db.session.commit()
            except Exception:
                self.db.session.rollback()
                raise
            return review
        return None

    def delete_review(self, review_id: int) -> None:
        """
        Delete a review by ID.
        Args:
            review_id (int): Review ID.
        """
        review = self.get_review_by_id(review_id)
        if review:
            try:
                self.db.session.delete(review)
                self.db.session.commit()
            except Exception:
                self.db.session.rollback()
                raise

    def delete_user(self, user_id: int) -> None:
        """
        Delete a user and all associated data.
        Args:
            user_id (int): User ID.
        """
        user = self.get_user_by_id(user_id)
        if user:
            try:
                self.db.session.delete(user)
                self.db.session.commit()
            except Exception:
                self.db.session.rollback()
                raise