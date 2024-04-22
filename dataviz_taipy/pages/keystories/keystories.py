import numpy as np
import pandas as pd

from taipy.gui import Markdown

import algo # from dataviz_taipy import algo
from data.data import data #from dataviz_taipy.data.data import data


keystories_md = Markdown("pages/keystories/keystories.md")

# colname_company = 'mnc'
colname_sector = 'sector'
colname_country = 'jur_name'

# selected_company = 'AXA'
selected_sector = 'Metals & Metal Products'
selected_country = 'France'


# selector_company = list(np.sort(data[colname_company].astype(str).unique()))
# def on_change_company(state):
#     print("Chosen company: ", state.selected_company)
#     state.df_selected_company = data[data[colname_company]==state.selected_company]
#     state.tracked_reports_company = \
#         algo.number_of_tracked_reports_company(state.df_selected_company)
#     state.df_count_company = algo.number_of_tracked_reports_over_time_company(state.df_selected_company)

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

# df_selected_company = data[data[colname_company]==selected_company]

df_selected_sector = data[data[colname_sector]==selected_sector]
df_selected_country = data[data[colname_country]==selected_country]