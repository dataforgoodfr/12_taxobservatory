import numpy as np
import pandas as pd
import io
from taipy.gui import Markdown,Gui, download

from dataviz_taipy.data.data import data

import dataviz_taipy.algo as algo

header_right_image_path = 'images/pexels-ingo-joseph-1880351.png'
download_icon_path = 'images/Vector.svg'

selected_company = 'ACCIONA'
selected_company = 'SHELL'

company_md = Markdown("pages/company/company.md")

df_selected_company = data[data["mnc"]==selected_company]

colname_company = 'mnc'
selector_company = list(np.sort(data[colname_company].astype(str).unique()))

selected_year = 2020
colname_year = 'year'
selector_year = list(np.sort(data[colname_year].astype(str).unique()))

df_count_company = algo.number_of_tracked_reports_over_time_company(df_selected_company)


number_of_tracked_reports_company = algo.number_of_tracked_reports_company(df_selected_company)

company_sector = list(df_selected_company["sector"].unique())[0]
company_upe_code = df_selected_company['upe_code'].unique()[0]

def download_viz1(state): download_el(state,viz1)
viz1 = {
    'data': company_sector,
    'title': "Sector",
    'sub_title': "",
    'on_action': download_viz1
}

def download_viz2(state): download_el(state,viz2)
viz2 = {
    'data': company_upe_code,
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
data_key_metric = algo.compute_company_key_financials_kpis(
    data, selected_company,selected_year)
def download_viz_13_key_metric(state): download_el(state,viz_13_key_metric)
viz_13_key_metric = {
    'data': pd.DataFrame.from_dict(data_key_metric).reset_index(),
    'title': "Key metrics",
    'sub_title': "Selected fiscal year",
    'on_action': download_viz_13_key_metric
}

# Viz 14
data_viz_14 = algo.compute_top_jurisdictions_revenue(
    data, selected_company,selected_year)
# fig_viz_14 = algo.display_jurisdictions_top_revenue(
#     data, selected_company,selected_year
# )

def download_viz_14(state): download_el(state,viz_14)
viz_14 = {
    'data': data_viz_14,
    'title': "Distribution of revenues across partner jurisdictions",
    'sub_title': "Selected fiscal year",
    'on_action': download_viz_14
}

data_viz_15 = algo.compute_pretax_profit_and_employees_rank(
        data, selected_company, selected_year)

def download_viz_15(state): download_el(state,viz_15)
properties = {
    # Shared y values
    "y":              "jur_name",
    # Bars for the female data set
    "x[1]":           "employees_%",
    "color[1]":       "#c26391",
    # Bars for the male data set
    "x[2]":           "profit_before_tax_%",
    "color[2]":       "#5c91de",
    # Both data sets are represented with an horizontal orientation
    "orientation":    "h",
    #
    "layout": {
        #"barmode": "overlay",
        # Set a relevant title for the x axis
        "xaxis": { "title": "%" },
        "legend": {
                # Place the legend above chart
                "xanchor": "bottom"
        },
        # Show/Hide the legend
        "showlegend": True
    }
}
# properties = {
#     # Shared y values
#     "x":              "jur_name",
#     # Bars for the female data set
#     "y[1]":           "employees_%",
#     "color[1]":       "#c26391",
#     # Bars for the male data set
#     "y[2]":           "profit_before_tax_%",
#     "color[2]":       "#5c91de",
#     # Both data sets are represented with an horizontal orientation
#     "orientation":    "v",
#     #
#     "layout": {
#         #"barmode": "overlay",
#         # Set a relevant title for the x axis
#         "xaxis": { "title": "%" },
#         "legend": {
#                 # Place the legend above chart
#                 "xanchor": "bottom"
#         },
#         # Show/Hide the legend
#         "showlegend": True
#     }
# }
viz_15 = {
    'data': data_viz_15,
    'title': "% profit and employees by partner jurisdiction",
    'sub_title': "CbC reports tracked",
    'on_action': download_viz_15
}
def download_viz_16(state): download_el(state,viz_16)
viz_16 = {
    'data': None,
    'title': "% profit and profit / employee by partner jurisdiction",
    'sub_title': "CbC reports tracked",
    'on_action': download_viz_16
}


def download_viz_17(state): download_el(state,viz_17)
viz_17 = {
    'data': None,
    'title': "% profits, % employees and profit / employee",
    'sub_title': "domestic vs. havens vs. non havens, selected fiscal year",
    'on_action': download_viz_17,

}

data_viz_18_dict = algo.compute_related_and_unrelated_revenues_breakdown(
    data, selected_company, selected_year)

data_viz_18 = pd.DataFrame.from_dict(data_viz_18_dict, orient='index').reset_index()
layout={ "barmode": "stack" }
print (data_viz_18)
# algo.display_related_and_unrelated_revenues_breakdown(data, selected_company, selected_year)
def download_viz_18(state): download_el(state,viz_18)
viz_18 = {
    'data': data_viz_18,
    'title': "Breakdown of revenue between unrelated and related revenue",
    'sub_title': "domestic vs. havens vs. non havens, selected fiscal year",
    'on_action': download_viz_18,

}

# what are the tax havens being used by the company
df_selected_company, df_selected_company_th_agg = (
    algo.tax_haven_used_by_company(df_selected_company))
data_viz_19 = df_selected_company_th_agg
def download_viz_19(state): download_el(state,viz_19)
viz_19 = {
    'data': data_viz_19,
    'title': "Profits, employees and revenue breakdown by tax haven",
    'sub_title': "selected fiscal year",
    'on_action': download_viz_19,

}

# Compute data
data_viz_21_dict = algo.compute_tax_havens_use_evolution(
    df=data, company=selected_company)
data_viz_21 = pd.DataFrame.from_dict(data_viz_21_dict)
print (data_viz_21)
def download_viz_21(state): download_el(state,viz_21)
viz_21 = {
    'data': data_viz_21,
    'title': "Percentage of profits, percentage of employees and profit per employees over time ",
    'sub_title': "domestic vs. havens vs. non havens, selected fiscal year",
    'on_action': download_viz_21,
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

