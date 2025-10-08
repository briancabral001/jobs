# Siempre que abras el proyecto de nuevo, solo necesitas:
# conda activate data_env
# cd /Users/brian/Documents/data_jobs
# PYTHONPATH=. pytest -v

import sys
import os
import pandas as pd
import numpy as np
import pycountry
from collections import Counter
import re
import us
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from features.wrangling import get_country_from_location, filter_location_matches_country, clean_location

def test_clean_location():
    assert clean_location("New York, NY (+3 others)") == "New York, NY"
    assert clean_location("California - USA") == "California, USA"
    assert clean_location("Berlin-Germany") == "Berlin, Germany"
    assert clean_location(None) is None
    assert clean_location("Somewhere") == "Somewhere"
    assert clean_location("  Leading and trailing spaces  ") == "Leading and trailing spaces"   





@pytest.mark.parametrize("location, expected", [
    ("New York, NY", "United States"),
    ("California, USA", "United States"),
    ("Berlin, Germany", "Germany"),
    ("Toronto, Canada", "Canada"),
    ("Any location", None),
    ("Somewhere", None),
    ("", None),
    (None, None),
    ("Texas - USA", "United States"),
    ("São Paulo - Brazil", "Brazil"),
    ("London, UK", "United Kingdom"),
    ("São Paulo, Brazil", "Brazil")
])
def test_get_country_from_location(location, expected):
    assert get_country_from_location(location) == expected




def test_filter_location_matches_country():
    data = {
        "job_location": [
            "New York, NY", "Berlin, Germany", "Toronto, Canada",
            "California, USA", "London, UK", "Somewhere"
        ],
        "job_country": [
            "United States", "Germany", "Canada",
            "United States", "United Kingdom", "Unknown"
        ]
    }
    df = pd.DataFrame(data)
    df_filtered = filter_location_matches_country(df)

    assert len(df_filtered) == 5  # Debería filtrar la fila con "Somewhere" y "Unknown"
    assert all(df_filtered["job_location"] != "Somewhere")
    assert all(df_filtered["job_country"] != "Unknown")
    assert all(df_filtered["job_location"].isin([
        "New York, NY", "Berlin, Germany", "Toronto, Canada",
        "California, USA", "London, UK"
    ]))
    assert all(df_filtered["job_country"].isin([
        "United States", "Germany", "Canada", "United Kingdom"
    ]))
    assert "normalized_location" in df_filtered.columns
    assert all(df_filtered["normalized_location"].isin([
        "United States", "Germany", "Canada", "United Kingdom"
    ]))
# PYTHONPATH=. pytest -v





