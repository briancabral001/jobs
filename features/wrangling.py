import pandas as pd
import numpy as np
import pycountry
from collections import Counter
import re
import us  

          




# Diccionario de normalización manual
custom_country_map = {
    "russia": "Russian Federation",
    "uk": "United Kingdom",
    "u.k.": "United Kingdom",
    "usa": "United States",
    "turkey": "Turkiye",
    "anywhere": "Anywhere",
    "jerman": "Germany",
    "swiss": "Switzerland",
    "democratic republic of the congo": "Congo, The Democratic Republic of the",
    "u.s. virgin islands": "Virgin Islands, U.S.",
    "usvi": "Virgin Islands, U.S.",
    "the bahamas": "Bahamas",
    "singapura" : "Singapore"
    }

# Diccionario de abreviaciones de estados USA → país
us_states_plus_dc_abbrev = {state.abbr: "United States" for state in us.states.STATES + [us.states.DC]}
us_states_plus_dc_name = {state.name: "United States" for state in us.states.STATES + [us.states.DC]}


def clean_location(location):
    """Cleans up location strings.

    - Returns None if the value is NaN.
    - Removes any text inside parentheses (e.g., "(+3 others)").
    - Replaces dashes ("-" or " - ") with commas.
    - Strips leading/trailing whitespace."""
    if pd.isna(location):
        return None
    # quitar cosas como "(+3 others)"
    location = re.sub(r"\(.*?\)", "", str(location))
    # reemplazar " - " o "-" por ", "
    location = re.sub(r"\s*-\s*", ", ", location)
    return location.strip()



def get_country_from_location(location):
    """
    Extract the country using custom_country_map, us_states_plus_dc_abbrev,
    us_states_plus_dc_name and pycountry to map inside of every row
    """
    
    location = clean_location(location)
    if not location:
        return None
    
    parts = [p.strip().lower() for p in location.split(",")]
    
    for part in parts[::-1]:  # revisar de atrás hacia adelante
        # 1. Chequear en diccionario manual
        if part in custom_country_map:
            return custom_country_map[part]
        
        # 2. Chequear abreviaciones de estados de USA
        if part.upper() in us_states_plus_dc_abbrev:
            return us_states_plus_dc_abbrev[part.upper()]
        # 3. Chequear nombre de estados de USA
        if part.title() in us_states_plus_dc_name:
            return us_states_plus_dc_name[part.title()]
        # 4. Chequear en pycountry (por nombre de país)
        try:
            country = pycountry.countries.lookup(part)
            return country.name
        except LookupError:
            continue
    
    return None


def filter_location_matches_country(df, col_location="job_location", col_country="job_country"):
    """
    Filter rows where the extracted country from col_location
    match with the value in 'col_country'.
    """
    df = df.copy()
    df["normalized_location"] = df[col_location].apply(get_country_from_location)
    mask = (df[col_location].str.lower() == "anywhere") | (df["normalized_location"] == df[col_country])
    return df[mask]





# Normalize job_schedule_type (in case there are differences in capital letters or hyphens)
mapping = {
        'full-time and part-time': 'Full-time and Part-time',
        'full-time and temp': 'Full-time and Temp work',
        'full-time and internship': 'Full-time and Internship',
        'full-time and contractor': 'Full-time and Contractor',
        'contractor and temp': 'Contractor and Temp work',
        'full-time': 'Full-time',
        'part-time': 'Part-time',
        'contractor': 'Contractor',
        'internship': 'Internship',
        'temporary': 'Temporary',
        ' and ': 'Hybrid',  # Any other "and" not in the previous cases 
        'temp': 'Temp work'
    }


def normalize_job_type(df, column='job_schedule_type'):
    """
    Normalize the values in the column "column" of the Dataframe "df"
    to standart categories using the mapping: 'Full-time', 'Part-time', 'Contractor',
    'Internship', 'Temporary', 'Hybrid', 'Other'.
    """
    df = df.copy()
    def map_job_type(x):
        x_str = str(x).lower()
        for key, value in mapping.items():
            if key in x_str:
                return value
        return 'Other'   
    df[column] = df[column].apply(map_job_type) 
    return df




def remove_outliers(df, upper_percentile= 0.99):
    """
    Remove outliers of the column 'salary_year_avg' in the Dataframe 'df'
    using de upper_percentile and drop de NA values
    """
    high = df['salary_year_avg'].dropna().quantile(upper_percentile)
    return df[df['salary_year_avg'] <= high]
