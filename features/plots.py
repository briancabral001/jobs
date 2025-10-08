import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import math
from features.helpers import filter_jobs 
import plotly.express as px
# import ipywidgets as widgets
# from IPython.display import display
import plotly.graph_objects as go

class DataJobsViz(object):
    """

    A class to make plots from processed data jobs.

    """
    def plot_salary_distribution(self, df, country=None,
                                title="Salary Distribution", xlabel="Salary (USD)",
                                ylabel="Frequency", bins=20):
        """
        Plot a histogram of salary distribution.

        Parameters
        ----------
        df : DataFrame with salary data
        country : str or list, optional -> filter by country/countries
        title, xlabel, ylabel : str -> text for plot
        bins : int -> number of histogram bins
        """
        df_plot = df.copy()
        # Filter by Country
        if country:
            df_plot = df_plot[df_plot['normalized_location'] == country]
            title = f"Salary Distribution in {country}"
         # Histogram plot
        fig = px.histogram(
            df_plot,
            x="salary_year_avg",
            color ="job_title_short",
            nbins=30,
            title = title,
            labels={
                "salary_year_avg": "Average Year Salary (USD)",
                "job_title_short": "Job Title",
            }
        )
        fig.update_layout(
            yaxis_title="Number of Job Offers",
            boxmode="group", 
            template="plotly_white"
        )
        fig.savefig() 
        fig.show()

  

    def plot_salary_by_country_and_job(self, df, top_countries=7, min_count=100,
                                    title="Top Median Salary by Country and Job Title",
                                    xlabel="Country", ylabel="Median Salary (USD)"):
            """
            Plot median salary by job title across countries.

            Parameters
            ----------
            df : DataFrame with job and salary data
            top_countries : int -> number of most frequent countries to include
            min_count : int -> minimum job occurrences per country to display
            title, xlabel, ylabel : str -> text for plot
            """
            df = df.dropna(subset=['salary_year_avg'])

            # Contar registros por país
            country_count = df.groupby('normalized_location')['salary_year_avg'].count().reset_index(name='count')
            valid_countries = country_count[country_count['count'] >= min_count]['normalized_location']

            df_filtered = df[df['normalized_location'].isin(valid_countries)]

            # Mediana por país y job_title
            stats = df_filtered.groupby(['normalized_location', 'job_title_short'])['salary_year_avg'].median().reset_index()
            stats = stats.rename(columns={'salary_year_avg': 'median'})

            # Mediana general por país para top N
            top_country_list = stats.groupby('normalized_location')['median'].median().nlargest(top_countries).index

            stats = stats[stats['normalized_location'].isin(top_country_list)]
            
            fig = px.bar(
            stats,
            x='normalized_location',
            y='median',
            color="job_title_short", 
            title= title,
             labels={
                    "job_title_short": "Job Title"
                }
            )
            fig.update_layout(
            xaxis_title= xlabel,
            yaxis_title= ylabel,
            barmode="group",
            template="plotly_white"
        )
            fig.savefig() 
            fig.show()

 
    
    def pie_charts_side_by_side(self,df, columns=None, maintitle=None, titles=None, textinfo=None):
        """
        Create side-by-side pie charts for multiple boolean columns.

        Parameters
        ----------
        df : DataFrame with data
        columns : list of str -> boolean columns to visualize
        maintitle : str -> overall title for the figure
        titles : list of str -> individual titles for each pie chart
        textinfo : str -> controls labels/text shown in the pies (e.g., "label+percent")
        """
        from plotly.subplots import make_subplots

        n = len(columns)
        subplot_titles = titles
        fig = make_subplots(
            rows=1, cols=n, 
            specs=[[{'type':'domain'}]*n],
            subplot_titles=subplot_titles   # cada columna es un pie
        )
        
        for i, col in enumerate(columns):
            counts = df[col].value_counts()
            fig.add_trace(
                go.Pie(labels=counts.index, values=counts.values,
                       textinfo=textinfo,
                       hole=0.3
                       ),
                row=1, col=i+1
            )
        
        fig.update_layout(title_text=maintitle,
                         template= "plotly_white")
        fig.savefig() 
        fig.show()



    def plot_skills_wordcloud(self, df, column="job_skills", top_n=100, title= None):
        """
        Generate a word cloud of the most frequent skills.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame containing the skills data.
        column : str, default="job_skills"
            Column containing skills (as text or lists) to visualize.
        top_n : int, default=100
            Number of most frequent skills to include in the word cloud.
        title : str, optional
            Title of the word cloud figure.
        """
        # Explode to have one row per skill
        all_skills = df[column].dropna().explode().astype(str)
        
        # Count frecuency
        freq = all_skills.value_counts().head(top_n)
        
        # 3️⃣ Generate the Wordcloud
        wc = wordcloud = WordCloud(
            width=1200,
            height=800,
            background_color='white'
        ).generate_from_frequencies(freq.to_dict())
        
        # Better the layout with Plotly
        fig = px.imshow(wc.to_array())
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            title = title,
            margin=dict(l=7, r=7, t=7, b=7)
        )
        fig.savefig() 
        fig.show()



    def plot_distribution_interactive(self,df, country=None, title= None):
        """
        Display an interactive salary distribution plot, optionally filtered by country.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame containing salary data.
        country : str or list, optional
            Country (or countries) to filter the data before plotting. If None, uses all data.
        title : str, optional
            Title of the interactive plot.
        """

        df_countries = filter_jobs(df, country=country)

        if df_countries.empty:
            print("No data for selected countries.")
            return
        fig = px.histogram(
            df_countries,
            x="salary_year_avg",
            color="normalized_location",  
            nbins=50,
            barmode="overlay",
            histnorm='density',   
            title= title,
            labels={"salary_year_avg": "Year Salary (USD)", "normalized_location": "Country"})
        
        fig.update_layout(
            boxmode="group",
            template="plotly_white"
        )
        fig.savefig() 
        fig.show()


        # Boxplot of salary by job title
    def plot_salary_by_job_title_interactive(self, df, country=None, title="Salary by Job Title", xlabel = "Country", ylabel="Salary (USD)"):
        """
        Display an interactive box plot of salaries by job title, optionally filtered by country.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame containing job titles and salary information.
        country : str or list, optional
            Country (or countries) to filter the data. If None, uses all data.
        title : str, default="Salary by Job Title"
            Title of the interactive plot.
        xlabel : str, default="Job Title"
            Label for the x-axis.
        ylabel : str, default="Salary (USD)"
            Label for the y-axis.
        """
        df_plot = filter_jobs(df, country = country)
        
        df_plot = df_plot.dropna(subset=['salary_year_avg'])

        fig = px.box(
            df_plot,
            x="normalized_location",
            y="salary_year_avg",
            color="job_title_short",
            title = title,
            labels={
            "normalized_location" : xlabel,
            "salary_year_avg" : ylabel,
            "job_title_short" : "Job Title",

            }
            )
        fig.update_layout(
            boxmode="group",
            template="plotly_white"
        )
        fig.savefig() 
        fig.show()


 

