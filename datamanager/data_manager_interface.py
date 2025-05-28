from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    """Abstract base class defining the interface for data manager implementations.
        This interface outlines the essential methods for managing users and movies
        within the application, such as adding, retrieving, updating, and deleting
        records. Any concrete data manager class should implement all these methods
        to ensure consistent behavior.

        Methods to implement include:
            - get_all_users()
            - get_user_by_id(user_id)
            - add_user(name)
            - get_user_movies(user_id)
            - get_movie_by_id(movie_id)
            - add_movie(user_id, **movie_data)
            - update_movie(movie_id, **movie_data)
            - delete_movie(movie_id)
            - delete_user(user_id)
        """
    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_user(self, user):
        pass

    @abstractmethod
    def add_movie(self, movie):
        pass

    @abstractmethod
    def update_movie(self, movie):
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass