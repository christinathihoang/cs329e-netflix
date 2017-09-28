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

# CACHES & DESCRIPTIONS

ACTUAL_CUSTOMER_RATING = create_cache("cache-actualCustomerRating.pickle")
# a dictionary of elements below:
# (cID, mID): rt
# mID rated cID as rt.

YEAR_OF_RATING = create_cache("cache-yearCustomerRatedMovie.pickle")
# a dictionary of elements below:
# (cID, mID): yr
# cID rated mID in year yr.

AVERAGE_MOVIE_RATING = create_cache("cache-averageMovieRating.pickle")
# a dictionary of elements below:
# mID: rt
# # The avg rating of mID is rt")

AVERAGE_MOVIE_RATING_PER_YEAR = create_cache("cache-movieAverageByYear.pickle")
# a dictionary of elements below:
# (mID, yr): rt
# The avg rating of mID in year yr is rt.

CUSTOMER_AVERAGE_RATING_YEARLY = create_cache("cache-customerAverageRatingByYear.pickle")
# a dictionary of elements below:
# (cID, yr): rt
# The avg rating of cID in year yr is rt.

CUSTOMER_OVERALL_AVERAGE = create_cache("cache-averageCustomerRating.pickle")
# a dictionary of elements below:
# cID: rt
# The avg rating of cID is rt.

AVERAGE_RATING = 3.60428996442

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
            current_movie = line.rstrip(':')
            writer.write(str(current_movie) + "\n")
        else:
	    # It's a customer
            current_customer = line

# loading variables
#----
            # find the current year
            year_customer_rated_movie         = YEAR_OF_RATING[(int(current_customer),int(current_movie))]
            # find the average movie rating for that year
            movie_average_for_current_year    = AVERAGE_MOVIE_RATING_PER_YEAR[(int(current_movie),int(year_customer_rated_movie))]
            # find movie average of all time
            movie_lifetime_average            = AVERAGE_MOVIE_RATING[int(current_movie)]
            # find the customers average rating for that year
            customer_average_for_current_year = CUSTOMER_AVERAGE_RATING_YEARLY[(int(current_customer), int(year_customer_rated_movie))]
            # find the customers overall ratings average
            customer_lifetime_average         = CUSTOMER_OVERALL_AVERAGE[int(current_customer)]
#----

# prediction calculation using loaded variables
#----
            total_of_ratings = AVERAGE_RATING + movie_average_for_current_year + movie_lifetime_average \
                                + customer_average_for_current_year + customer_lifetime_average
            prediction = total_of_ratings / 5 # not sure what kind of value this will return, might need to round
#----

            predictions.append(prediction)
            actual_score = ACTUAL_CUSTOMER_RATING[int(current_customer),int(current_movie)]
            actual.append(actual_score)
            writer.write(str(prediction))
            writer.write('\n')

        # calculate rmse for predications and actuals
    rmse = sqrt(mean(square(subtract(predictions, actual))))
    writer.write(str(rmse)[:4] + '\n')
