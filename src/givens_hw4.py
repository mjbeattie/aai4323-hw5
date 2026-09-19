"""
givens_hw4.py
AAI4323_5323
July 13, 2025
Matthew J. Beattie
University of Oklahoma

These functions and values are written for you.  You will call them in your code.  Do not modify
the functions or the tests of your code will fail.
"""

def get_zipcode_from_coordinates(row, geocode):
    """
    Reverse‑geocode latitude/longitude and return the ZIP/postcode.
    """

    # Extract latitude and longitude from the row
    latitude = row.get('latitude')
    longitude = row.get('longitude')

    try:
        # Use the geocode function to get the location
        location = geocode((latitude, longitude))
        if location and location.raw and 'address' in location.raw:
            return location.raw['address'].get('postcode')
        return None

    except Exception as e:
        print(f"Error for {latitude}, {longitude}: {e}")
        return None

# This dictionary contains the ages of the customers
customer_ages = {'Amy': 27, 'Bill': 51, 'Charlotte': 72}

# This dictionary contains the fraction of the populations that have had COVID
covid_probabilities = {
    '97130': {
        'under_50': 0.35,
        '50_plus': 0.25
    },
    '97141': {
        'under_50': 0.25,
        '50_plus': 0.15
    },
    '97150': {
        'under_50': 0.15,
        '50_plus': 0.10
    }
}
