import numpy as np
import pandas as pd

from taipy.gui import Markdown

from dataviz_taipy.data.data import data

import dataviz_taipy.algo as algo

selected_company = 'ACCIONA'

company_md = Markdown("pages/company/company.md")

df_selected_company = data[data["mnc"]==selected_company]

colname_company = 'mnc'
selector_company = list(np.sort(data[colname_company].astype(str).unique()))

df_count_company = algo.number_of_tracked_reports_over_time_company(df_selected_company)

def on_change_company(state):
    print("Chosen company: ", state.selected_company)
    state.df_selected_company = data[data["mnc"]==state.selected_company]
    state.df_count_company = algo.number_of_tracked_reports_over_time_company(state.df_selected_company)