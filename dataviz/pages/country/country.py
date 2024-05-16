import numpy as np
import pandas as pd

from taipy.gui import Markdown, download

import algo # from dataviz import algo
from data.data import data #from dataviz.data.data import data

import io

header_right_image_path = 'images/pexels-ingo-joseph-1880351.png'
download_icon_path = 'images/Vector.svg'

selected_country = 'Mauritius'
country_md = Markdown("pages/country/country.md")

colname_country = 'jur_name'
selector_country = list(np.sort(data[colname_country].astype(str).unique()))

df_selected_country = data[data["jur_name"]==selected_country] 
df_count_country = algo.number_of_tracked_reports_over_time_country(df_selected_country)

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

def download_el(state, viz):
    buffer = io.StringIO()
    data = viz['data']
    if type(data) == pd.DataFrame:
        data.to_csv(buffer)
    else:
        buffer.write(state["sub_title"] + "\n" + str(data))
    download(state, content=bytes(buffer.getvalue(), "UTF-8"), name="data.csv")


data_viz_2 = algo.number_of_tracked_reports_over_time(data)
def download_viz_2(state): download_el(state,viz_2)
viz_2 = {
    'data': data_viz_2,
    'title': "Evolution of reports over time",
    'sub_title': "CbC reports tracked",
    'on_action': download_viz_2
}

data_viz_tbd = algo.number_of_tracked_reports_over_time(data)
def download_viz_tbd(state): download_el(state,viz_tbd)
viz_tbd = {
    'data': data_viz_tbd,
    'title': "Transparency score over time ",
    'sub_title': "CbC reports tracked",
    'on_action': download_viz_tbd
}

data_viz_5 = algo.breakdown_of_reports_by_hq_country(data)
data_viz_5_fig = algo.breakdown_of_reports_by_hq_country_viz(data_viz_5)
def download_viz_5(state):download_el(state,viz_5)
viz_5 = {
    'fig': data_viz_5_fig,
    'data': data_viz_5,
    'title': "Breakdown of reports tracked by HQ country",
    'sub_title': "CbC reports tracked",
    'on_action': download_viz_5
}

data_viz_4 = algo.breakdown_of_reports_by_sector(data)
data_viz_4_fig = algo.breakdown_of_reports_by_sector_viz(data_viz_4)
def download_viz_4(state):download_el(state,viz_4)
viz_4 = {
    'fig': data_viz_4_fig,
    'data': data_viz_4,
    'title': "Breakdown of reports tracked by HQ country",
    'sub_title': "CbC reports tracked",
    'on_action': download_viz_4
}


data_viz_6, top_10_sectors = algo.breakdown_of_reports_by_sector_over_time(data)
data_viz_6_fig = algo.breakdown_of_reports_by_sector_over_time_viz(data_viz_6, top_10_sectors)
def download_viz_6(state):download_el(state,viz_6)
viz_6 = {
    'fig': data_viz_6_fig,
    'data': data_viz_6,
    'title': "Evolution of reports over time",
    'sub_title': "CbC reports tracked",
    'on_action': download_viz_6
}




data_viz_24 = algo.viz_24_compute_data(data)
data_viz_24_fig = algo.viz_24_viz(data_viz_24)
def download_viz_24(state):download_el(state,viz_24)
viz_24 = {
    'fig': data_viz_24_fig,
    'data': data_viz_24,
    'title': "Multinationals available",
    'sub_title': "with 1+ report tracked",
    'on_action': download_viz_24
}


# data_viz_27 = algo.viz_24_compute_data(data)
# data_viz_27_fig = algo.viz_24_viz(data_viz_24)
# def download_viz_27(state):download_el(state,viz_27)
# viz_27 = {
#     'fig': data_viz_27_fig,
#     'data': data_viz_27,
#     'title': "Number of reports and transparency score by multinational",
#     'sub_title': "",
#     'on_action': download_viz_27
# }
