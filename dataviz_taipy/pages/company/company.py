import numpy as np
import pandas as pd
import io
from taipy.gui import Markdown,Gui, download

from dataviz_taipy.data.data import data

import dataviz_taipy.algo as algo

header_right_image_path = 'images/pexels-ingo-joseph-1880351.png'
download_icon_path = 'images/Vector.svg'

selected_company = 'ACCIONA'

company_md = Markdown("pages/company/company.md")

df_selected_company = data[data["mnc"]==selected_company]

colname_company = 'mnc'
selector_company = list(np.sort(data[colname_company].astype(str).unique()))

selected_year = 2023
colname_year = 'year'
selector_year = list(np.sort(data[colname_year].astype(str).unique()))

df_count_company = algo.number_of_tracked_reports_over_time_company(df_selected_company)


number_of_tracked_reports_company = algo.number_of_tracked_reports_company(df_selected_company)

def download_viz1(state): download_el(state,viz1)
viz1 = {
    'data': None,
    'title': "Sector",
    'sub_title': "",
    'on_action': download_viz1
}

def download_viz2(state): download_el(state,viz2)
viz2 = {
    'data': df_selected_company,
    'title': "Headquarter",
    'sub_title': "",
    'on_action': download_viz2
}

def download_viz3(state): download_el(state,viz3)
viz3 = {
    'data': number_of_tracked_reports_company,
    'title': "Reports",
    'sub_title': "CbC reports tracked",
    'on_action': download_viz3
}

def download_viz4(state): download_el(state,viz4)
viz4 = {
    'data': number_of_tracked_reports_company,
    'title': "CbC Transparency Grade",
    'sub_title': "average over all reports",
    'on_action': download_viz4
}

def download_viz5(state): download_el(state,viz5)
viz5 = {
    'data': number_of_tracked_reports_company,
    'title': "CbC Transparency  Grade",
    'sub_title': "selected fiscal year",
    'on_action': download_viz5
}

def download_viz6(state): download_el(state,viz6)
viz6 = {
    'data': df_selected_company,
    'title': "More on transparency (tbd)",
    'sub_title': "",
    'on_action': download_viz6
}

# Viz 13
data_key_metric = algo.compute_company_key_financials_kpis(data, selected_company,selected_year)
def download_viz7(state): download_el(state,viz7)
viz7 = {
    'data': pd.DataFrame.from_dict(data_key_metric),
    'title': "Key metrics",
    'sub_title': "Selected fiscal year",
    'on_action': download_viz7
}

# Viz 14
def download_viz8(state): download_el(state,viz8)
viz8 = {
    'data': df_selected_company,
    'title': "Distribution of revenues across partner jurisdictions",
    'sub_title': "Selected fiscal year",
    'on_action': download_viz8
}


def download_viz9(state): download_el(state,viz9)
viz9 = {
    'data': df_selected_company,
    'title': "% profit and employees by partner jurisdiction",
    'sub_title': "CbC reports tracked",
    'on_action': download_viz9
}
def download_viz10(state): download_el(state,viz10)
viz10 = {
    'data': df_selected_company,
    'title': "% profit and profit / employee by partner jurisdiction",
    'sub_title': "CbC reports tracked",
    'on_action': download_viz10
}


def download_viz11(state): download_el(state,viz11)
viz11 = {
    'data': df_selected_company,
    'title': "% profits, % employees and profit / employee",
    'sub_title': "domestic vs. havens vs. non havens, selected fiscal year",
    'on_action': download_viz11,

}

def download_viz12(state): download_el(state,viz12)
viz12 = {
    'data': df_selected_company,
    'title': "Breakdown of revenue between unrelated and related revenue",
    'sub_title': "domestic vs. havens vs. non havens, selected fiscal year",
    'on_action': download_viz12,

}

def download_viz13(state): download_el(state,viz13)
viz13 = {
    'data': df_selected_company,
    'title': "Profits, employees and revenue breakdown by tax haven",
    'sub_title': "selected fiscal year",
    'on_action': download_viz13,

}

def download_viz14(state): download_el(state,viz14)
viz14 = {
    'data': df_selected_company,
    'title': "Percentage of profits, percentage of employees and profit per employees over time ",
    'sub_title': "domestic vs. havens vs. non havens, selected fiscal year",
    'on_action': download_viz14,
}

def on_change_company(state):
    print("Chosen company: ", state.selected_company)
    state.df_selected_company = data[data["mnc"]==state.selected_company]
    state.df_count_company = algo.number_of_tracked_reports_over_time_company(state.df_selected_company)

def on_change_year(state):
    print("Chosen year: ", state.selected_year)

def download_el(state, viz):
    buffer = io.StringIO()
    data = viz['data']
    if type(data) == pd.DataFrame:
        data.to_csv(buffer)
    else:
        buffer.write(state["sub_title"] + "\n" + str(data))
    download(state, content=bytes(buffer.getvalue(), "UTF-8"), name="data.csv")
# <|{download_icon_path}|image|class_name=download|on_action=on_click|properties={viz}>

