import sys

from movie_app import MovieApp
from storage_csv import StorageCsv
from storage_json import StorageJson


def main():
    """
    Entry point for the Movie App.

    Parses command-line arguments to specify the storage file (CSV/JSON) and initializes the movie app with the chosen storage.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <storage_file>")
        sys.exit(1)

    storage_file = sys.argv[1]

    if storage_file.endswith('.csv'):
        storage = StorageCsv(storage_file)
    else:
        # Assuming default storage format is JSON
        storage = StorageJson(storage_file)

    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
