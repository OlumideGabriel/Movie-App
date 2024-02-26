import statistics
import website_generator
import random

HTML_TEMPLATE = "website/index_template.html"


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def _movie_stats(self):
        """Prints out various statistics of movies"""
        lst_of_ratings = []
        movie_list = self._storage.list_movies()  # Assuming list_movies() returns the movie list
        for movie in movie_list:
            ratings = float(movie["rating"])
            lst_of_ratings.append(ratings)

        # Average rating
        print(f"Average rating: {round(statistics.mean(lst_of_ratings), 2)}")

        # Median rating
        print(f"Median rating: {statistics.median(lst_of_ratings)}")

        # Best movie
        best_movie = max(movie_list, key=lambda x: x["rating"])
        print(f'Best movie: {best_movie["title"].title()}, {best_movie["rating"]}')

        # Worst movie
        worst_movie = min(movie_list, key=lambda x: x["rating"])
        print(f'Worst movie: {worst_movie["title"].title()}, {worst_movie["rating"]}')

    def _random_movie(self):
        """Displays a random movie, alongside its rating"""
        movie_list = self._storage.list_movies()  # Assuming list_movies() returns the movie list
        rand_movie = random.choice(movie_list)
        print(f'Your movie tonight is {rand_movie["title"]}, with a rating of {rand_movie["rating"]}')

    def _search_movie(self):
        """This functions prints out movie search results with rating in descending order"""
        movie_list = self._storage.list_movies()
        search_lst = []
        movie_search = input("Search movie: ")
        for movie in movie_list:
            if fuzz.partial_ratio(movie_search, movie["title"]) > 75:
                search_lst.append(movie)

        desc_list = search_lst[::-1]
        for movie in desc_list:
            print(f'{movie["title"]}, {movie["rating"]}')

    def _sort_movies_by_rating(self):
        """This displays movies with ratings in descending order"""
        movie_list = self._storage.list_movies()
        movie_rating = []
        for movie in movie_list:
            movie_rating.append(movie["rating"])
        movie_rating.sort()
        desc_rating = movie_rating[::-1]

        sorted_movie = []
        for rating in desc_rating:
            for movie in movie_list:
                if rating == movie["rating"]:
                    if movie not in sorted_movie:
                        sorted_movie.append(movie)

        for movie in sorted_movie:
            print(movie["title"], movie["rating"], movie["year"])

    def _generate_website(self):
        movie_list = self._storage.list_movies()  # Assuming list_movies() returns the movie list
        new_data = website_generator.serialized_html(movie_list)
        old_html_data = website_generator.load_html_data(HTML_TEMPLATE)
        website_generator.insert_data_to_html(old_html_data, new_data)
        print("Website successfully generated!")

    def run(self):
        """
        Runs the MovieApp application.

        Displays a menu of options for interacting with movie data and prompts the user to input a command.
        The available commands include listing movies, adding, deleting, and updating movies,
        displaying movie statistics, getting a random movie, searching for a movie, sorting movies by rating,
        and generating a website.
        """
        while True:
            # Print menu
            print(f"Menu:\n0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n4. Update movie\n"
                  f"5. Stats\n6. Random movie\n7. Search movie\n8. Movies sorted by rating\n9. Generate website\n")
            # Get user command
            menu_choice = input("Enter choice (0-9): ")
            print(f"Choice selected: {menu_choice}\n")
            # Execute command
            if menu_choice == "0":
                print("Bye!")
                break
            elif menu_choice == "1":
                # Print a list of movies
                movies = self._storage.list_movies()
                s = "s" if len(movies) > 1 else ""  # Pluralize movies when movies list > 1
                print(f"{len(movies)} movie{s} in total\n")
                for movie in movies:
                    print(f'{movie["title"].title()}: {movie["rating"]}, {movie["year"]}')

            elif menu_choice == "2":
                self._storage.add_movie()
            elif menu_choice == "3":
                self._storage.delete_movie()
            elif menu_choice == "4":
                self._storage.update_movie()
            elif menu_choice == "5":
                self._movie_stats()
            elif menu_choice == "6":
                self._random_movie()
            elif menu_choice == "7":
                self._search_movie()
            elif menu_choice == "8":
                self._sort_movies_by_rating()
            elif menu_choice == "9":
                self._generate_website()
            else:
                print("Invalid selection.")
