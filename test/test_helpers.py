# Siempre que abras el proyecto de nuevo, solo necesitas:
# conda activate data_env
# cd /Users/brian/Documents/data_jobs
# PYTHONPATH=. pytest -v



import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pandas as pd
from features.helpers import check_values

def test_check_values():
    # DataFrame pequeño de prueba
    data = {
        "job_title": ["Data Analyst", "Data Scientist", "Data Analyst", "Engineer"]
    }
    df = pd.DataFrame(data)

    # Llamamos a la función
    result = check_values(df, "job_title", expected_values=["Data Analyst", "Data Scientist"])

    # Verificamos que 'value_counts' tenga la forma esperada
    assert "Data Analyst" in result["value_counts"].index
    assert result["value_counts"]["Data Analyst"] == 2

    # Verificamos que aparezca el valor inesperado
    assert "Engineer" in result["unexpected"]



import pandas as pd
from features.helpers import filter_jobs



def test_filter_jobs():
    # DataFrame pequeño de prueba
    data = {
        "job_title_short": ["Data Analyst", "Data Scientist", "Data Analyst", "Engineer"],
        "category": ["Senior", "Specialist", "Senior", "Junior"],
        "job_country": ["Austria", "Germany", "Austria", "Germany"],
        "job_schedule_type": ["full_time", "part_time", "full_time", "full_time"]
    }
    df = pd.DataFrame(data)

    # Llamamos a la función filtrando por job_title y país
    result = filter_jobs(df, job_titles=["Data Analyst"], countries=["Austria"])

    # Verificamos que el DataFrame filtrado tenga la forma esperada
    assert len(result) == 1
    assert all(result["job_title_short"] == "Data Analyst")
    assert all(result["job_country"] == "Austria")

    # Probamos otro filtro: categoría Analytics y schedule full_time
    result2 = filter_jobs(df, ctgory=["Senior"], schedule=["full_time"])

    assert len(result2) == 1
    assert all(result2["category"] == "Senior")
    assert all(result2["job_schedule_type"] == "full_time")




