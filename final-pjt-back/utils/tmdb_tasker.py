from pprint import pprint
from .tmdb import TMDB


tasks = [
    # TMDB().save_genre_dict,
    # TMDB().load_genre_dict,
    # TMDB().get_movie_detail,
    # TMDB().get_sample_movies,
    TMDB().load_genre_list
]

for task in tasks:
    # pprint(task(550))
    pprint(task())
