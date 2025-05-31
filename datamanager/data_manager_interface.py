from abc import ABC, abstractmethod
from typing import List, Optional

class DataManagerInterface(ABC):
    """
    Abstract base class defining the interface for data manager implementations.
    This interface outlines essential methods for managing users and movies
    within the application, including adding, retrieving, updating, and deleting
    records. Concrete data manager classes must implement all these methods to
    ensure consistent behavior across different data backends.
    Methods to implement:
        - get_all_users()
        - get_user_by_id(user_id)
        - add_user(name)
        - get_user_movies(user_id)
        - get_movie_by_id(movie_id)
        - add_movie(user_id, **movie_data)
        - update_movie(movie_id, **movie_data)
        - delete_movie(movie_id)
        - delete_user(user_id)
        -etc.
    """

    @abstractmethod
    def add_user(self, name: str, email: str):
        """Add a new user and return the created user object."""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int):
        """Retrieve a user by their ID."""
        pass

    @abstractmethod
    def get_user_by_email(self, email: str):
        """Retrieve a user by their email."""
        pass

    @abstractmethod
    def get_all_users(self) -> List:
        """Return a list of all users."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id: int) -> List:
        """Return all movies associated with a user."""
        pass

    @abstractmethod
    def add_movie(self, user_id: int, **movie_data):
        """Add a new movie for a user."""
        pass

    @abstractmethod
    def get_movie_by_id(self, movie_id: int):
        """Retrieve a movie by its ID."""
        pass

    @abstractmethod
    def update_movie(self, movie_id: int, **movie_data):
        """Update movie details."""
        pass

    @abstractmethod
    def delete_movie(self, movie_id: int):
        """Delete a movie by its ID."""
        pass

    @abstractmethod
    def add_review(self, user_id: int, movie_id: int, review_text: str, rating: Optional[float] = None):
        """Add a review for a movie."""
        pass

    @abstractmethod
    def get_review_by_id(self, review_id: int):
        """Retrieve a review by its ID."""
        pass

    @abstractmethod
    def get_reviews_for_movie(self, movie_id: int) -> List:
        """Return all reviews for a given movie."""
        pass

    @abstractmethod
    def update_review(self, review_id: int, review_text: str, rating: Optional[float] = None):
        """Update review content and rating."""
        pass

    @abstractmethod
    def delete_review(self, review_id: int):
        """Delete a review by its ID."""
        pass

    @abstractmethod
    def delete_user(self, user_id: int):
        """Delete a user and associated data."""
        pass