from istorage import IStorage
import json
import os
import requests

API_KEY = "aeb2943f"
REQUEST_URL = f"https://www.omdbapi.com/?apikey={API_KEY}&t="


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file = file_path
        if not os.path.exists(file_path):  # Creates file_path if file does not exist
            with open(file_path, 'w') as jsonfile:
                json.dump([], jsonfile)  # Writing an empty JSON object

    def list_movies(self):
        """
        Returns a dictionary that contains
        the movies information in the database."""

        with open(self.file, "r") as handle:
            movie_list = json.load(handle)
            return movie_list

    def add_movie(self):
        """Functions get data from movie API, and adds a movie to the movies database"""
        new_movie_title = input(f"Enter new movie for {self.file}: ")
        movie_list = self.list_movies()
        for movie in movie_list:
            if new_movie_title in movie["title"]:
                print("Movies already exists")
                return

        url = REQUEST_URL + new_movie_title

        try:
            response = requests.get(url)
            if response.status_code == requests.codes.ok:
                movie = response.json()
                movie_title = movie["Title"]
                movie_year = movie["Year"]
                movie_poster = movie["Poster"]
                movie_rating = float(movie["imdbRating"])
                latest_movie = {'title': movie_title.title(), 'rating': movie_rating,
                                'year': movie_year, 'poster': movie_poster}
                movie_list.append(latest_movie)
                with open(self.file, 'w') as handle:
                    json.dump(movie_list, handle, indent=4)
                print("Movie added successfully!")
            else:
                print("Error:", response.status_code, response.text)
        except requests.exceptions.RequestException:
            print(f"No Network!\nCheck connection and try again...")
        except KeyError:

            print("Oops... Movie does not Exist!")

    def delete_movie(self):
        """Deletes a movie from the storage"""
        movie_list = self.list_movies()
        movie_to_delete = input(f"Enter movie you want to delete for ({self.file}): ").lower()
        movie_found = False  # Flag to check if movie is found

        for movie in movie_list:
            if movie_to_delete in movie["title"].lower():
                movie.clear()
                # Delete empty dictionary
                movie_list.remove({})
                with open(self.file, 'w') as handle:
                    json.dump(movie_list, handle, indent=4)
                print("Movie deleted!")
                movie_found = True  # Set flag to True if movie is found

        if not movie_found:
            print("Movie not found!")

    def update_movie(self):
        """Updates movie rating """
        movie_list = self.list_movies()
        movie_to_update = input(f"Enter to check if movie exists in ({self.file}): ").lower()
        movie_found = False  # Flag to check if movie is found

        for movie in movie_list:
            if movie_to_update in movie["title"].lower():
                while True:
                    try:
                        movie_rating = float(input("Enter new movie rating (1 - 10): "))
                        if 1 <= movie_rating <= 10:
                            break
                        else:
                            print("Movie rating needs to be from 1 to 10.")
                    except ValueError:
                        print("Invalid input! Movie rating must be a number.")

                movie["rating"] = movie_rating
                with open(self.file, 'w') as handle:
                    json.dump(movie_list, handle, indent=4)
                print(f"Movie Updated! >>> {movie_to_update.title()}: {movie_rating}")
                movie_found = True
                break  # No need to continue looping if movie is found

        if not movie_found:
            print("Movie not found!")
