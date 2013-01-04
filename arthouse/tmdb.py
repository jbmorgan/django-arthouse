"""
Methods for getting data from the TMDB API.
"""

from arthouse import secrets
from urllib2 import Request, urlopen

def get_movie_details_dict(tmdb_id):
    if not secrets.TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY is not set!")

    headers = {"Accept": "application/json"}
    request_uri = "http://api.themoviedb.org/3/movie/%s?api_key=%s" % (tmdb_id, secrets.TMDB_API_KEY)

    request = Request(request_uri, headers=headers)
    response_body = urlopen(request).read()

    return response_body