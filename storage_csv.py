import os
from istorage import IStorage
import csv
import requests

API_KEY = "aeb2943f"
REQUEST_URL = f"https://www.omdbapi.com/?apikey={API_KEY}&t="


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file = file_path
        if not os.path.exists(file_path):  # Creates file_path if file does not exist
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['title', 'rating', 'year', 'poster'])
                writer.writeheader()

    def list_movies(self):
        """
        Returns a dictionary that contains
        the movies information in the database."""

        movie_dict = []
        with open(self.file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                movie_dict.append(row)
            return movie_dict

    def add_movie(self):
        """Functions get data from movie API, and adds a movie to the movies database"""
        new_movie_title = input(f"Enter new movie for {self.file}: ")
        movie_dict = self.list_movies()
        for movie in movie_dict:
            if new_movie_title == movie['title']:
                print("Movies already exists")
                return

        # Simulating movie data retrieval from API
        url = REQUEST_URL + new_movie_title

        default_poster = '/images/default_image.png'

        try:
            response = requests.get(url)
            if response.status_code == requests.codes.ok:
                movie = response.json()
                movie_title = movie["Title"].title()
                movie_year = movie["Year"]
                movie_poster = default_poster if movie["Poster"] == 'N/A' else movie["Poster"]
                movie_rating = movie["imdbRating"]
                latest_movie = {'name': movie_title, 'rating': movie_rating, 'year': movie_year, 'poster': movie_poster}
                movie_dict.append(latest_movie)
                with open(self.file, 'a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=['title', 'rating', 'year', 'poster'])
                    writer.writerow({'title': new_movie_title, 'rating': movie_rating, 'year': movie_year,
                                     'poster': movie_poster})
                print("Movie added successfully!")
            else:
                print("Error:", response.status_code, response.text)
        except requests.exceptions.RequestException:
            print(f"No Network!\nCheck connection and try again...")
        except KeyError:

            print("Oops... Movie does not Exist!")

    def delete_movie(self):
        """Deletes a movie from the storage"""
        movie_dict = self.list_movies()
        movie_to_delete = input(f"Enter movie you want to delete for ({self.file}): ").lower()
        movie_found = False  # Flag to check if movie is found

        for movie in movie_dict:
            if movie_to_delete in movie['title'].lower():
                # Movie found, do not add it to the updated dictionary
                print(f'Deleting movie: {movie["title"]}')
                movie.clear()
                # Delete empty dictionary
                movie_dict.remove({})
                print(movie_dict)
                movie_found = True

        if movie_found:
            with open(self.file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['title', 'rating', 'year', 'poster'])
                writer.writeheader()
                for movie in movie_dict:
                    writer.writerow({'title': movie['title'], 'rating': movie['rating'], 'year': movie['year'],
                                     'poster': movie['poster']})
            print("Movie deleted!")
        else:
            print("Movie not found!")
            return

    def update_movie(self):
        """Updates movie rating """
        movie_dict = self.list_movies()
        movie_to_update = input(f"Enter to check if movie exists in ({self.file}): ").lower()
        movie_found = False  # Flag to check if movie is found

        for movie in movie_dict:
            if movie_to_update in movie["title"].lower():
                while True:  # Loop until valid rating is provided
                    try:
                        movie_rating = float(input("Enter new movie rating (1 - 10): "))
                        if 1 <= movie_rating <= 10:
                            break  # Exit the loop if rating is valid
                        else:
                            print("Movie rating needs to be from 1 to 10.")
                    except ValueError:
                        print("Invalid input! Movie rating must be a number.")

                movie["rating"] = movie_rating
                print(movie_dict)

                with open(self.file, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=['title', 'rating', 'year', 'poster'])
                    writer.writeheader()
                    for _movie in movie_dict:
                        writer.writerow({'title': _movie['title'], 'rating': _movie['rating'], 'year': _movie['year'],
                                         'poster': _movie['poster']})

                print(f"Movie Updated! >>> {movie_to_update.title()}: {movie_rating}")
                movie_found = True  # Set flag to True if movie is found
                break  # No need to continue looping if movie is found

        if not movie_found:
            print("Movie not found!")

