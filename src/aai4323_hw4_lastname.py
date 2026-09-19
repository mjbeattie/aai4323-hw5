"""
aai4323_hw4_lastname.py
AAI4323_5323
July 13, 2025
University of Oklahoma

In this script, you will complete code in functions that will enable the calculation of probabilities
that customers have had COVID.  In the script, there are four segments with the tag TODO: in front of
them.  You will insert your own code in each segment to complete the script.

There are assertion statements in the code that mimic the tests for the homework.
"""

# Import necessary libraries
import random
import math
import time
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Import given information from givens_hw4
from givens_hw4 import get_zipcode_from_coordinates, customer_ages, covid_probabilities


def get_zipcodes(geolocator):
    """
    This function takes a datafile containing customer phone calls and their locations.
    You will use the given function get_zipcode_from_coordinates() to add zipcodes to
    each phone call row.  You are working with Pandas dataframes, so you will use the apply()
    function to lookup the zipcode for each row and store it as a value in the new column.
    """
    # Define a geopy geolocator with a user agent
    geolocator = Nominatim(user_agent="aai4323_hw4")

    # Define a rate-limited reverse geocoding function with a timeout
    def reverse_with_timeout(coords):
        return geolocator.reverse(coords, timeout=10)

    # Use RateLimiter to limit the number of requests per second
    geocode = RateLimiter(
        reverse_with_timeout,
        min_delay_seconds=1,
        max_retries=3,
        error_wait_seconds=2,
    )

    # Load the TSV file into a DataFrame
    df = pd.read_csv("customer_phone_calls.tsv", sep='\t')
    
    # TODO: CREATE A NEW COLUMN IN THE DATAFRAME CALLED 'zipcode' AND SET IT EQUAL TO THE RESULT OF APPLYING
    # THE FUNCTION get_zipcode_from_coordinates TO EACH ROW IN THE DATAFRAME.  YOU WILL NEED TO PASS THE geolocator
    # OBJECT TO THE FUNCTION AS WELL.  HINT: USE A LAMBDA FUNCTION INSIDE THE APPLY FUNCTION.
    # START YOUR CODE HERE

    # END YOUR CODE HERE
    
    # Look at your dataframe
    return df


def add_zipprobs(df):
    """
    This function takes the dataframe you built in get_zipcodes and calculates the fraction of
    phone calls in each zip code for each customer.
    """
    # Step 1: Count occurrences of each (customer, zipcode) pair
    zip_probs = df.groupby(['customer', 'zipcode']).size().reset_index(name='count')

    # Step 2: Total rows per customer
    zip_totals = zip_probs.groupby('customer')['count'].transform('sum')
    
    # Step 3: Calculate fraction
    zip_probs['zipprob'] = zip_probs['count'] / zip_totals

    return zip_probs


def get_covid_fracs(df):
    """
    This function builds on the dataframe constructed in add_zipprobs.  You will lookup
    the customer's ages from the given dictionary customer_ages and store them into a
    dataframe called agedf.  You will then merge that dataframe back to the one from
    add_zipprobs based upon their common column.  Then you will apply a function called
    lookup_covid_frac to the dataframe to return the COVID fraction of the population whose
    age was in the same category as the customer's for each zipcode.
    """
    # TODO: READ THE customer_ages DICTIONARY INTO A PANDAS DATAFRAME NAMED agedf.
    # IT SHOULD HAVE TWO COLUMNS, ONE CALLED 'age' AND THE OTHER THE SAME AS THE KEY IN THE customer_ages DICTIONARY.
    # HINT: USE THE pd.DataFrame() FUNCTION AND THE .ITEMS() METHOD OF THE DICTIONARY.
    # START YOUR CODE HERE

    # END YOUR CODE HERE


    # TODO: MERGE THE agedf DATAFRAME TO THE zip_probs DATAFRAME ON THE COMMON COLUMN.  
    # STORE THE RESULT IN A NEW DATAFRAME CALLED covid_fracs.
    # HINT: USE THE pd.MERGE() FUNCTION.
    # START YOUR CODE HERE

    # END YOUR CODE HERE
    
    # Add a column to the dataframe equal to the COVID fraction of the population for the
    # zipcode and age combination using the function below
    def lookup_covid_frac(row):
        zip_info = covid_probabilities.get(row['zipcode'], {})
        if row['age'] < 50:
            return zip_info.get('under_50', None)
        else:
            return zip_info.get('50_plus', None)
    
    # Apply function to each row
    covid_fracs['covid_frac'] = covid_fracs.apply(lookup_covid_frac, axis=1)
    
    return covid_fracs


def get_covid_probs(df):
    """
    You will modify the dataframe from get_covid_fracs by multiplying the probability that
    each customer lived in a zipcode by the fraction of population that had COVID in that
    zipcode/age combination.
    """
    # TODO: SET A NEW COLUMN IN THE DATAFRAME CALLED 'covid_prob'.
    # THE NEW COLUMN IS EQUAL TO THE PRODUCT OF THE COLUMNS 'zipprob' AND 'covid_frac'.
    # HINT: YOU CAN DO THIS WITH A SINGLE LINE OF CODE.
    # START YOUR CODE HERE

    # END YOUR CODE HERE
    
    # Sum the COVID probabilities by customer
    covid_probs = df.groupby('customer', as_index=False)['covid_prob'].sum()
    
    return covid_probs


# This is the main section of the assignment that calls your functions.
def main():
    # Define a geopy geolocator and call get_zipcodes to map zipcodes to phone calls and check your work
    geolocator = Nominatim(user_agent="my-geolocation-app")
    print("Geolocating phone calls, this can take a few minutes...")
    added_zips = get_zipcodes(geolocator)

    print("Checking for accurate geolocation...")
    correct_zips = ['97130', '97141', '97150', '97141', '97150']
    myzips = added_zips.head()['zipcode'].tolist()

    assert correct_zips == myzips, "Your zipcodes do not match the correct zipcodes"

    # Calculate the fraction of calls in each zipcode for each customer and check your work
    print("Getting fraction of calls in zipcodes...")
    zip_probs = add_zipprobs(added_zips)
    
    print("Checking for accurate fractions in zipcodes...")
    correct_zipprob = 0.526316
    my_zipprob = zip_probs.loc[(zip_probs['customer'] == 'Amy') & (zip_probs['zipcode'] == '97130'), 'zipprob'].values[0]

    assert abs(correct_zipprob - my_zipprob) < 0.0001, "Your probability is outside the acceptable range"
    
    # Get the fraction of customers by customer age and zip combination that had COVID.  Check your work.
    print("Getting fractions of age+zipcode populations with COVID...")
    covid_fracs = get_covid_fracs(zip_probs)

    print("Checking for accurate fractions of COVID...")
    correct_covid_frac = 0.25
    my_covid_frac = covid_fracs.loc[(covid_fracs['customer'] == 'Bill') & (covid_fracs['zipcode'] == '97130'), 'covid_frac'].values[0]

    assert abs(correct_covid_frac - my_covid_frac) < 0.001, "Your covid fraction is outside the acceptable range"

    # Calculate the final probabilities that each customer had COVID and check your work
    print("Getting final probabilities of COVID by customer...")
    covid_probs = get_covid_probs(covid_fracs)

    print("Checking for accurate COVID probabilities...")
    correct_charlotte = 0.125862
    my_charlotte = covid_probs.loc[(covid_probs['customer'] == 'Charlotte'), 'covid_prob'].values[0]
    assert abs(correct_charlotte - my_charlotte) < 0.001, "Your covid fraction is outside the acceptable range"

    print("Saving final dataframe to TSV file...")
    covid_probs.to_csv("aai4323_hw4_output.tsv", sep="\t", encoding="utf-8", index=False)


if __name__ == "__main__":
    main()