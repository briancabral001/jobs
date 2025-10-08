import pandas as pd
import numpy as np

def filter_jobs(df, job_titles=None, ctgory= None, country=None, schedule=None,  drop_dupes=True):
    """
    Filter a DataFrame of job posts based on flexible parameters.

      Parameters:
    -----------
    df : pandas.DataFrame
        Original DataFrame.
    job_titles : list, optional
        List of job titles to filter.
    category : list, optional
        Types of experience and expertise.
    countries : list, optional
        List of countries to filter.
    schedule : str, optional
        Contract type (e.g., "full_time").
    drop_dupes : bool, optional
        Remove duplicates if True (default).

    Returns:
    --------
    pandas.DataFrame
        DataFrame filtered according to the given parameters.
    """
    df_filtered = df.copy()


    if job_titles:
      df_filtered = df_filtered[df_filtered['job_title_short'].isin(job_titles)]
    if ctgory:
      df_filtered = df_filtered[df_filtered['category'].isin(ctgory)]  
    if country:
      df_filtered = df_filtered[df_filtered['normalized_location'].isin(country)]
    if schedule:
      df_filtered = df_filtered[df_filtered['job_schedule_type'].isin(schedule)]
    if drop_dupes:
      df_filtered = df_filtered.drop_duplicates()

    return df_filtered
