import numpy as np
import pandas as pd

from taipy.gui import Markdown

import algo # from dataviz_taipy import algo
from data.data import data #from dataviz_taipy.data.data import data


sector_md = Markdown("pages/sector/sector.md")

colname_sector = 'sector'
selected_sector = 'Metals & Metal Products'

selector_sector = list(np.sort(data[colname_sector].astype(str).unique()))

df_selected_sector = data[data[colname_sector]==selected_sector]
df_count_sector = algo.number_of_tracked_reports_over_time_sector(df_selected_sector)

def on_change_sector(state):
    print("Chosen sector: ", state.selected_sector)
    state.df_selected_sector = data[data[colname_sector]==state.selected_sector]
    state.tracked_reports_sector = \
        algo.number_of_tracked_reports_sector(state.df_selected_sector)
    state.df_count_sector = algo.number_of_tracked_reports_over_time_sector(state.df_selected_sector)

