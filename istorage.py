from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        """
        Returns a dictionary that contains
        the movies information in the database."""
        pass

    @abstractmethod
    def add_movie(self):
        """Functions get data from movie API, and adds a movie to the movies database"""
        pass

    @abstractmethod
    def delete_movie(self):
        """Deletes a movie from the storage"""
        pass

    @abstractmethod
    def update_movie(self):
        """Updates movie rating """
        pass
