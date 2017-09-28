#!/usr/bin/env python3

# -------
# imports
# -------

from math import sqrt
import pickle
from requests import get
from os import path
from numpy import sqrt, square, mean, subtract


def create_cache(filename):
    """
    filename is the name of the cache file to load
    returns a dictionary after loading the file or pulling the file from the public_html page
    """
    cache = {}
    filePath = "/u/fares/public_html/netflix-caches/" + filename

    if path.isfile(filePath):
        with open(filePath, "rb") as f:
            cache = pickle.load(f)
    else:
        webAddress = "http://www.cs.utexas.edu/users/fares/netflix-caches/" + \
            filename
        bytes = get(webAddress).content
        cache = pickle.loads(bytes)

    return cache


AVERAGE_RATING = 3.60428996442
ACTUAL_CUSTOMER_RATING = create_cache(
    "cache-actualCustomerRating.pickle")
AVERAGE_MOVIE_RATING_PER_YEAR = create_cache(
    "cache-movieAverageByYear.pickle")
YEAR_OF_RATING = create_cache("cache-yearCustomerRatedMovie.pickle")
CUSTOMER_AVERAGE_RATING_YEARLY = create_cache(
    "cache-customerAverageRatingByYear.pickle")

actual_scores_cache = create_cache("JT26983-ActualRatingByCustomerIDAndMovieID.pickle")
movie_year_cache = create_cache("JT26983-MovieYearByMovieID.pickle")
avg_score_year_cache = create_cache("cache-movieAverageByYear.pickle")
avg_movie_rating_cache = create_cache("JT26983-AvgMovieRatingByMovieID.pickle")

# ------------
# netflix_eval
# ------------

def netflix_eval(reader, writer):
    predictions = []
    actual = []
    prediction = 0
    # iterate throught the file reader line by line
    for line in reader:
        # need to get rid of the '\n' by the end of the line
        line = line.strip()
        # check if the line ends with a ":", i.e., it's a movie title 
        if line[-1] == ':':
            # It's a movie
            writer.write(line)
            writer.write('\n')
            current_movie = line.rstrip(':')
            pred = avg_movie_rating_cache[int(current_movie)]
        else:
	    # Its a customer
            current_customer = line
            predictions.append(prediction)
            actual_score = actual_scores_cache[(int(current_customer),int(current_movie))]
            actual.append(int(actual_score))
            writer.write(str(pred)) 
            writer.write('\n')

                
    # calculate rmse for predications and actuals
#    rmse = sqrt(mean(square(subtract(predictions, actual))))
#    writer.write(str(rmse)[:4] + '\n')
