# tests/test_visualizations.py
import sys
import os
sys.path.append(os.path.abspath(".."))  
import plotly.graph_objects as go
import pandas as pd
from features.plots import DataJobsViz  # adapta el import a tu estructura

def test_plot_salary_distribution_runs():

    data = {
        "job_title_short": ["Data Scientist", "Data Engineer", "Data Analyst"],
        "salary_year_avg": [120000, 110000, 90000],
        "normalized_location": ["United States", "Argentina", "Argentina"]
    }
    df = pd.DataFrame(data)

    viz = DataJobsViz()
    fig = viz.plot_salary_distribution(df)


    assert fig is not None
    assert hasattr(fig, "to_dict")  


def test_plot_salary_by_country_and_job():
    
    data = {
        "job_title_short": ["Data Scientist", "Data Engineer", "Data Analyst"],
        "salary_year_avg": [120000, 110000, 90000],
        "normalized_location": ["United States", "Argentina", "Argentina"]
    }
    df = pd.DataFrame(data)

    viz = DataJobsViz()
    fig = viz.plot_salary_by_country_and_job(df, top_countries=2, min_count=1)

    assert fig is not None
    assert hasattr(fig, "to_dict") 


def test_pie_charts_side_by_side():
    
    data = {
        "job_work_from_home": [True, False, True],
        "job_no_degree_mention":[True, True, False]
    } 
    df = pd.DataFrame(data)

    viz = DataJobsViz()
    fig = viz.pie_charts_side_by_side(
        df,
        columns=["job_work_from_homme", "job_no_degree_mention"],
        maintitle="Job Types",
        titles=["Remote Jobs", "No Degree Mentions Jobs"]
    )

    # Validaciones
    assert fig is not None
    assert isinstance(fig, go.Figure)

    # Debe haber un trace por columna (dos en este caso)
    assert len(fig.data) == 2

    # Validar títulos de los subplots
    subplot_titles = [a.text for a in fig.layout.annotations]
    assert "Remote Jobs" in subplot_titles
    assert "No Degree Mentions Jobs" in subplot_titles

    
    
def test_plot_skills_wordcloud_runs():
    # DataFrame de ejemplo
    data = {
        "job_skills": [
            ["Python", "SQL", "Machine Learning"],
            ["Python", "Data Analysis"],
            ["SQL", "Tableau", "Excel"],
            ["Python", "SQL"]
        ]
    }
    df = pd.DataFrame(data)

    viz = DataJobsViz()
    # Solo verificamos que no lance excepciones
    fig = viz.plot_skills_wordcloud(df, column="job_skills", top_n=5, title="Top Skills")
    assert fig is not None


   
def test_plot_distribution_interactive_runs():
    # DataFrame de ejemplo
    data = {
        "salary_year_avg": [120000, 110000, 90000, 130000],
        "normalized_location": ["Spain", "United States", "Argentina", "Germany"]
    }
    df = pd.DataFrame(data)

    viz = DataJobsViz()

    # Debe correr sin errores con todos los datos
    fig_all = viz.plot_distribution_interactive(df)
    assert fig_all is not None
    # Debe correr sin errores filtrando por un país que existe
    fig = viz.plot_distribution_interactive(df, country="Spain")
    assert "Spain" in [d.name for d in fig.data]  
   


def test_plot_distribution_interactive(self,df, country=None, title= None):
        
    data = {
        "salary_year_avg": [120000, 110000, 90000, 130000],
        "normalized_location": ["Spain", "Spain", "Argentina", "Germany"]
    }

    df = pd.DataFrame(data)

    viz = DataJobsViz()

    fig = viz.plot_distribution_interactive(df, country="Argentina", title= None)

    assert fig is not None
    assert "Argentina" in [d.name for d in fig.data]  