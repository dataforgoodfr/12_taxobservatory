# streamlit run /media/pykoe/354d12b6-2f35-4a36-be0a-16b2867537f5/pykoe/PycharmProjects/pykoe-data4good-taxobservatory/data4good.py


from datetime import datetime

import pandas as pd
import streamlit as st
import altair as alt
from numpy.lib.function_base import select
from streamlit.logger import get_logger

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def show_all_viz():

    st.markdown("# Viz")

    data_root_path = './data/'

    df = pd.read_csv(data_root_path + 'dataset_multi_years_cleaned_completed (1).tab',
                     sep='\t')
    df['year'] = df['year'].astype(int)

    company_list = list(df['mnc'].unique())[::-1]
    selected_company = st.selectbox('Select a company', company_list,
                                   index=len(company_list) - 1)
    df_selected_company = df[df['mnc'] == selected_company]
    #selected_company_sector = df_selected_company['sector'].unique()

    sector_list = list(df['sector'].unique())[::-1]
    selected_sector = st.selectbox('Select a sector', sector_list,
                                   index=len(sector_list) - 1)
    df_selected_sector = df[df['sector'] == selected_sector]

    country_list = list(df['jur_name'].unique())[::-1]
    selected_country = st.selectbox('Select a country', country_list,
                                    index=len(country_list) - 1)
    df_selected_country = df[df['jur_name'] == selected_country]


    df_viz = pd.read_csv(data_root_path + 'vizs.csv')
    st.table(df_viz)


    header = st.columns(6)
    header[0].write("what")
    header[1].write("viz")
    header[2].write("how")
    header[3].write("variaint")
    header[4].write("comment")
    header[5].write("specific value")

    def number_of_tracked_reports():
        row = st.columns(6)
        row[0].write("Number of tracked reports")
        row[1].write("raw figure")

        number_of_tracked_reports = len(df.groupby(['year', 'mnc'])['mnc'])
        number_of_tracked_reports_company = len(df_selected_company.groupby(['year'])['year'])
        number_of_tracked_reports_sector = len(df_selected_sector.groupby(['year', 'mnc'])['year'])
        number_of_tracked_reports_country = len(df_selected_country.groupby(['year', 'mnc'])['year'])

        row[1].write('total ' + str(number_of_tracked_reports))
        row[1].write('per company (ex:' + selected_company + ')' + str(number_of_tracked_reports_company))
        row[1].write('per sector (ex:' + selected_sector + ')' + str(number_of_tracked_reports_sector))
        row[1].write('per country (ex:' + selected_country + ') '+ str(number_of_tracked_reports_country))
        row[2].markdown(
            '''
            - total : len(df.groupby(['year', 'mnc'])['mnc'])
            - company : len(df_selected_company.groupby(['year'])['year'])
            - sector : len(df_selected_sector.groupby(['year', 'mnc'])['year'])
            - country : len(df_selected_country.groupby(['year', 'mnc'])['year'])
            ''')
        row[3].markdown(
            '''
            - total : len(df.groupby(['year', 'mnc'])['mnc'])
            - company : len(df_selected_company.groupby(['year'])['year'])
            - sector : len(df_selected_sector.groupby(['year', 'mnc'])['year'])
            - country : len(df_selected_country.groupby(['year', 'mnc'])['year'])
            ''')
    number_of_tracked_reports()

    def number_of_tracked_reports_over_time():
        row = st.columns(6)
        row[0].write("Number of tracked reports over time")
        row[1].write("bar chart / line chart")
        row[1].write("st.line_chart(df_count, x='year', y='mnc')")

        df_count = df.groupby(['year'])['mnc'].nunique().reset_index()

        row[1].line_chart(df_count, x='year', y='mnc')

        row[1].write("st.bar_chart(df_count, x='year', y='mnc')")

        row[1].bar_chart(df_count, x='year', y='mnc')

        row[2].write("count distinct mnc x year, by year")
        row[2].write("df.groupby(['year'])['mnc'].nunique().reset_index()")
        row[2].table(df_count)

        row[3].write("selected company")
        row[3].write("df_selected_company.groupby(['year'])['mnc'].nunique().reset_index()")

        df_count_company = df_selected_company.groupby(['year'])['mnc'].nunique().reset_index()

        row[3].line_chart(df_count_company, x='year', y='mnc')
        row[3].write("all company")
        row[3].write("df.groupby(['year'])['mnc'].nunique().reset_index()")

        df_count_all_company = df.groupby(['year'])['mnc'].nunique().reset_index()

        row[3].line_chart(df_count_all_company, x='year', y='mnc')

        row[4].write("selected sector")
        row[4].write("df_selected_sector.groupby(['year'])['mnc'].nunique().reset_index()")

        df_count_sector = df_selected_sector.groupby(['year'])['mnc'].nunique().reset_index()

        row[4].line_chart(df_count_sector, x='year', y='mnc')
        row[4].write("all sector")
        row[4].write("df.groupby(['year', 'sector'])['mnc'].nunique().reset_index()")

        df_count_all_sector = df.groupby(['year', 'sector'])['mnc'].nunique().reset_index()

        row[4].line_chart(df_count_all_sector, x='year', y='mnc', color='sector')

        row[5].write("selected country")
        row[5].write("df_selected_country.groupby(['year'])['mnc'].nunique().reset_index()")

        df_count_country = df_selected_country.groupby(['year'])['mnc'].nunique().reset_index()

        row[5].line_chart(df_count_country, x='year', y='mnc')
        row[5].write("all country")
        row[5].write("df.groupby(['year', 'jur_name'])['mnc'].nunique().reset_index()")

        df_count_all_country = df.groupby(['year', 'jur_name'])['mnc'].nunique().reset_index()

        row[5].line_chart(df_count_all_country, x='year', y='mnc', color='jur_name')
    number_of_tracked_reports_over_time()

    def number_of_tracked_mnc():
        row = st.columns(6)
        row[0].write("Number of tracked mnc")
        row[1].write("raw figure")
        row[1].write("total")
        number_of_tracked_mnc_ = len(df['mnc'].unique())
        row[1].write(str(number_of_tracked_mnc_))

        row[2].write("count distinct (mnc)")
        row[2].write("len(df['mnc'].unique())")
        row[3].markdown('''
            on homepage : total   
            on sector / hq country pages : total filter by sector / hq country
            ''')

        row[4].write("per sector")
        df_number_of_tracked_mnc_sector = df.groupby('sector')['mnc'].nunique()
        row[4].write("df.groupby('sector')['mnc'].nunique()")
        row[4].table(df_number_of_tracked_mnc_sector.head(4))
        tab = row[4].expander(label='all')
        tab.table(df_number_of_tracked_mnc_sector)

        row[5].write("per country")
        df_number_of_tracked_mnc_country = df.groupby('jur_name')['mnc'].nunique()
        row[5].write("df.groupby('jur_name')['mnc'].nunique()")
        row[5].table(df_number_of_tracked_mnc_country.head(5))
        tab = row[5].expander(label='all')
        tab.table(df_number_of_tracked_mnc_country)
    number_of_tracked_mnc()


    def breakdown_of_reports_by_sector_hq_country():
        row = st.columns(6)

        # count distinct mnc x year, by sector / country

        df_ = df.groupby(['year', 'mnc', 'sector']).count().reset_index()
        df_ = df_[['year', 'mnc', 'sector']].groupby(['sector']).count().reset_index()
        row[0].table(df_.head(5))
        tab = row[0].expander(label='all')
        tab.table(df_)

        # Display the plot in Streamlit
        fig, ax = plt.subplots()
        # Data to plot
        labels = df_['sector']
        sizes = df_['year']
        # Create a pie chart
        plt.pie(sizes, labels=labels)
        # ax.scatter([1, 2, 3], [1, 2, 3])
        row[1].pyplot(fig)
        my_expander = row[1].expander(label='Pie Chart code')
        my_expander.write('''
            \# Display the plot in Streamlit  
            fig, ax = plt.subplots()  
            \# Data to plot  
            labels = df_['sector']  
            sizes = df_['year']  
            \# Create a pie chart  
            plt.pie(sizes, labels=labels)  
            \# ax.scatter([1, 2, 3], [1, 2, 3])  
            row3[1].pyplot(fig)
        ''')
    breakdown_of_reports_by_sector_hq_country()

    def sample_vis(container, df):
        # data treatment
        df_to_viz = df.groupby(['year', 'mnc', 'sector']).count().reset_index()

        # data viz
        container.write("# row X")
        container.table(df_to_viz.head(5))

    sample_vis(st, df)