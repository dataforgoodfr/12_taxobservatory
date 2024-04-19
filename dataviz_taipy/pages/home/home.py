import numpy as np
import pandas as pd
from PIL import Image
import io
from taipy.gui import Markdown,Gui, download

from dataviz_taipy import algo
from dataviz_taipy.data.data import data

original_image = "images/viz.png"
layout = {'barmode':'stack', "hovermode":"x"}
options = {"unselected":{"marker":{"opacity":0.5}}}

download_icon_path = 'images/Vector.svg'
df = data.head()


def download_viz1(state): download_el(state,viz1)
def download_viz_2(state): download_el(state,viz_2)
def download_viz3(state): download_el(state,viz3)

df_viz1 = algo.number_of_tracked_reports(data)
viz1 = {
    'data': df_viz1,
    'title': "Reports",
    'sub_title': "CbC reports tracked",
    'on_action': download_viz1
}

df_viz3 = algo.number_of_tracked_reports_company(data)
viz3 = {
    'data': df_viz3,
    'title': "Multinationals ",
    'sub_title': "with 1+ report tracked",
    'on_action': download_viz3
}

df_viz_2 = algo.number_of_tracked_reports_over_time(data)
viz_2 = {
    'data': df_viz_2,
    'title': "Evolution of reports over time",
    'sub_title': "CbC reports tracked",
    'on_action': download_viz_2
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



# Generate the digits, save them in a CSV file content, and trigger a download action
# so the user can retrieve them
def download_el(state, viz):
    buffer = io.StringIO()
    data = viz['data']
    if type(data) == pd.DataFrame:
        data.to_csv(buffer)
    else:
        buffer.write(state["sub_title"] + "\n" + str(data))
    download(state, content=bytes(buffer.getvalue(), "UTF-8"), name="data.csv")
# <|{download_icon_path}|image|class_name=download|on_action=on_click|properties={viz}>



home_md = Markdown("pages/home/home.md")