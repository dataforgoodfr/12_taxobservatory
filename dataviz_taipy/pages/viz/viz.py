import numpy as np
import pandas as pd

from taipy.gui import Markdown

from dataviz_taipy.data.data import data
import dataviz_taipy.algo as algo

import plotly.graph_objects as go


colname_company = 'mnc'
colname_sector = 'sector'
colname_country = 'jur_name'

selected_company = 'AXA'
selected_sector = 'Metals & Metal Products'
selected_country = 'France'


selector_company = list(np.sort(data[colname_company].astype(str).unique()))
def on_change_company(state):
    print("Chosen company: ", state.selected_company)
    state.df_selected_company = data[data[colname_company]==state.selected_company]
    state.tracked_reports_company = \
        algo.number_of_tracked_reports_company(state.df_selected_company)
    state.df_count_company = algo.number_of_tracked_reports_over_time_company(state.df_selected_company)

selector_sector = list(np.sort(data[colname_sector].astype(str).unique()))
def on_change_sector(state):
    print("Chosen sector: ", state.selected_sector)
    state.df_selected_sector = data[data[colname_sector]==state.selected_sector]
    state.tracked_reports_sector = \
        algo.number_of_tracked_reports_sector(state.df_selected_sector)
    state.df_count_sector = algo.number_of_tracked_reports_over_time_sector(state.df_selected_sector)



selector_country = list(np.sort(data[colname_country].astype(str).unique()))
def on_change_country(state):
    print("Chosen country: ", state.selected_country)
    state.df_selected_country = data[data[colname_country]==state.selected_country] 
    state.tracked_reports_counrty = \
        algo.number_of_tracked_reports_country(state.df_selected_country)    
    state.df_count_country = algo.number_of_tracked_reports_over_time_country (state.df_selected_country)

df_selected_company = data[data[colname_company]==selected_company]
df_selected_sector = data[data[colname_sector]==selected_sector]
df_selected_country = data[data[colname_country]==selected_country]


# Viz 4 - Breakdown of reports by sector (pie chart)
df_reports_per_sector_year = algo.breakdown_of_reports_by_sector(data)
breakdown_of_reports_by_sector_fig = algo.breakdown_of_reports_by_sector_viz(df_reports_per_sector_year)


tracked_reports = algo.number_of_tracked_reports(data)
tracked_reports_company = algo.number_of_tracked_reports_company(df_selected_company)
tracked_reports_sector = algo.number_of_tracked_reports_sector(df_selected_sector)
tracked_reports_counrty = algo.number_of_tracked_reports_country(df_selected_country)

df_count = algo.number_of_tracked_reports_over_time(data)
df_count_company = algo.number_of_tracked_reports_over_time_company(df_selected_company)
df_count_sector = algo.number_of_tracked_reports_over_time_sector(df_selected_sector)
df_count_country = algo.number_of_tracked_reports_over_time_country (df_selected_country)


df_company_info, df_tax_haven_company = algo.tax_haven_used_by_company(df_selected_company)
df_company_table = algo.company_table(df_selected_company)
viz_md = Markdown("pages/viz/viz.md")



