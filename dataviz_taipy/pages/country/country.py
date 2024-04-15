import numpy as np
import pandas as pd

from taipy.gui import Markdown

import algo

from data.data import data

selected_country = 'Mauritius'
country_md = Markdown("pages/country/country.md")

colname_country = 'jur_name'
selector_country = list(np.sort(data[colname_country].astype(str).unique()))

df_selected_country = data[data["jur_name"]==selected_country] 
df_count_country = algo.number_of_tracked_reports_over_time_country(df_selected_country)

def on_change_country(state):
    # state contains all the Gui variables and this is through this state variable
    # that we can update the Gui
    # state.selected_country, state.data_country_date, ...
    # update data_country_date with the right country 
    # (use initialize_case_evolution)
    print("Chosen country: ", state.selected_country)
    state.df_selected_country = data[data["jur_name"]==state.selected_country] 
        
    # state.pie_chart = pd.DataFrame({"labels": ["Deaths", "Recovered", "Confirmed"],
    #                                 "values": [state.data_country_date.iloc[-1, 6], state.data_country_date.iloc[-1, 5], state.data_country_date.iloc[-1, 4]]})
    state.df_count_country = algo.number_of_tracked_reports_over_time_country(state.df_selected_country)
    # convert_density(state)
