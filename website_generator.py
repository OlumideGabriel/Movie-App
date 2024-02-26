OUTPUT_FILE = "website/index.html"
TEMP_FILE = "temp.txt"


def load_html_data(html_file):
    """" Loads an HTML file """
    with open(html_file, "r") as file:
        return file.read()


def serialized_html(movies):
    output = ""
    for movie in movies:
        try:
            movie_poster = movie["poster"]
            movie_name = movie["title"]
            movie_year = movie["year"]
            movie_rating = movie["rating"]

            output += '\n<li>\n<div class="movie">\n'
            output += f'<img class="movie-poster" src="{movie_poster}"/>\n'
            output += f'<div class="movie-title">{movie_name}</div>\n'
            output += f'<div class="movie-year">{movie_year}</div>\n'
            output += f'<div class="movie-rating">{movie_rating}</div>\n'
            output += f'</div>\n</li>'
        except KeyError:
            continue
    return output


def insert_data_to_html(old_html_data, new_data):
    """ Function replaces html files in old_data with new_data """
    # Change webpage content
    new_website_data = old_html_data.replace("__TEMPLATE_MOVIE_GRID__", f"\n{new_data}")
    with open(OUTPUT_FILE, "w") as newfile:
        newfile.write(new_website_data)

    # Change webpage title
    with open(OUTPUT_FILE, "r") as file:
        data = file.read()
    webpage_title = "MOVIEVERSE"
    new_header = data.replace("__TEMPLATE_TITLE__", f"\n{webpage_title}")
    with open(OUTPUT_FILE, "w") as newfile:
        newfile.write(new_header)

