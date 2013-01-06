"""
Methods for getting data from the TMDB API.
"""

from arthouse import secrets, models
from urllib2 import Request, urlopen
import json

from django.core.files import File 
from django.core.files.temp import NamedTemporaryFile


def get_movie_details_dict(tmdb_id):
    """
    Gets a dictionary with the general information, cast, crew, and release
    information for the movie with the specified TMDB ID.
    """
    if not secrets.TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY is not set!")

    headers = {"Accept": "application/json"}
    request_uri = "http://api.themoviedb.org/3/movie/%s?api_key=%s&append_to_response=casts,releases" % (tmdb_id, secrets.TMDB_API_KEY)

    request = Request(request_uri, headers=headers)
    response_body = urlopen(request).read()

    response_json = json.loads(response_body)
    return response_json

def tmdb_img_base_url():
    """
    Gets the current base URL needed to download image files from TMDB.
    """
    if not secrets.TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY is not set!")

    headers = {"Accept": "application/json"}
    request_url = "http://api.themoviedb.org/3/configuration?api_key=%s" % secrets.TMDB_API_KEY

    request = Request(request_url, headers=headers)
    response_body = urlopen(request).read()

    response_json = json.loads(response_body)
    
    base_img_url = response_json.get('images').get('base_url')

    return base_img_url + "/original/"


def movie_for_tmdb_id(tmdb_id):
    """
    Creats a ``Movie`` instance for a movie with the given TMDB ID.
    """
    tmdb_dict = get_movie_details_dict(tmdb_id)
    
    print tmdb_dict

    title = tmdb_dict.get('title')
    description = tmdb_dict.get('overview')
    slug = tmdb_id
    length = tmdb_dict.get('runtime')
    year = tmdb_dict.get('release_date')[0:4]

    genre_dicts = tmdb_dict.get('genres')
    genres = list_to_string([g.get('name') for g in genre_dicts])

    language_dicts = tmdb_dict.get('spoken_languages')
    languages = list_to_string([l.get('name') for l in language_dicts])
    
    releases_dict = tmdb_dict.get('releases')
    countries_list = releases_dict.get('countries')

    CINEMA_REGION = 'US' # this should be a cinema setting in the future

    rating = None

    for country_dict in countries_list:
        if country_dict.get('iso_3166_1') == CINEMA_REGION:
            rating = country_dict.get('certification')
            break

    casts_dict = tmdb_dict.get('casts')

    list_of_cast_dicts = casts_dict.get('cast')
    list_of_crew_dicts = casts_dict.get('crew')

    MAX_CAST_TO_LIST = 5 # this should be a cinema setting in the future
    #                    # or, really, the entire list should be saved, in the correct order

    cast_list = list()
    directors_list = list()
    writers_list = list()

    for castmember_dict in list_of_cast_dicts:
        if castmember_dict.get('order') < MAX_CAST_TO_LIST:
            cast_list.append(castmember_dict.get('name'))

    for crewmember_dict in list_of_crew_dicts:
        if crewmember_dict.get('job') == 'Director':
            directors_list.append(crewmember_dict.get('name'))
        if crewmember_dict.get('department') == 'Writing':
            writers_list.append(crewmember_dict.get('name'))            

    cast = list_to_string(cast_list)
    directors = list_to_string(directors_list)
    writers = list_to_string(writers_list)

    print "Cast: " + cast

    poster_image = None
    banner_image = None
    tile_image = None

    image_base_url = tmdb_img_base_url()

    poster_img_url = image_base_url + tmdb_dict.get('poster_path')
    banner_img_url = image_base_url + tmdb_dict.get('backdrop_path')

    # temp_poster_img = NamedTemporaryFile(delete=True)
    # temp_poster_img.write(urllib2.urlopen(poster_img_url).read())

    site_url = tmdb_dict.get('homepage')
    imdb_url = "http://www.imdb.com/title/" + tmdb_dict.get('imdb_id')

    movie = models.Movie(   title=title,
                            description=description,
                            slug=slug,
                            genres=genres,
                            length=length,
                            year=year,
                            languages=languages,
                            rating=rating,
                            cast=cast,
                            directors=directors,
                            writers=writers,
                            poster_image=poster_image,
                            banner_image=banner_image,
                            tile_image=tile_image,
                            site_url=site_url,
                            imdb_url=imdb_url,
            )

    movie.save()
    
    return movie


def list_to_string(list_of_strings):
    """
    Converts a list of strings into one comma-delimited string.

    Example:
    ['a', 'b', 'c'] -> 'a, b, c'
    """
    if list_of_strings is None or len(list_of_strings) < 1:
        return None

    return_string = ""

    for s in list_of_strings:
        return_string += s + ", "

    return return_string[:-2]