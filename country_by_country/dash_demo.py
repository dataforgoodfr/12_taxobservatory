"""
Dash app demo for TaxObservatory

@author: PascalRaux-EP

# Run this app with `python %fileName.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# (cf https://dash.plotly.com/layout )
"""
import base64, json
from io import BytesIO
from dash import Dash, html, dcc, dash_table, callback, callback_context, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from PIL import Image as PIL_Image
from country_by_country.dash_process_methods import (
    DICT_OF_METHODS,
    DEFAULT_METHOD,
    DICT_OF_PARAMETERS,
    process_results,
)

app = Dash(
    __name__,
    title="*Dash Demo for EU Tax Observatory*",
    external_stylesheets=[
        dbc.themes.FLATLY,
    ],
)


app.layout = dbc.Container(
    dbc.Stack(
        [
            dcc.Store(id="store_pdf", data={}),
            dcc.Store(id="parameters", data={}),
            dcc.Markdown(
                "# Country by Country Tax Reporting analysis",
                style={"fontSize": 24, "color": "DarkBlue"},
            ),
            dcc.Upload(
                id="upload-pdf",
                children=dcc.Loading(
                    type="default", children=html.Div(id="loading_text_pdf")
                ),
                style={
                    "height": "30px",
                    "lineHeight": "30px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "15px",
                    "textAlign": "center",
                },
                multiple=False,  # Allow multiple files to be uploaded
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                options=(
                                    [
                                        {
                                            "value": DEFAULT_METHOD,
                                            "label": f"{DEFAULT_METHOD} (default)",
                                        }
                                    ]
                                    + [
                                        {"value": k, "label": k}
                                        for k in DICT_OF_METHODS
                                        if k != DEFAULT_METHOD
                                    ]
                                ),
                                value=DEFAULT_METHOD,
                                id="dropdown_method_selector",
                                placeholder="Select a method",
                            ),
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            dbc.Button(
                                dcc.Loading(
                                    type="default",
                                    children=html.Div(id="run_button_text"),
                                ),
                                id="run_button",
                                n_clicks=0,
                                outline=True,
                                color="info",
                                class_name="col-12",
                                size="sm",
                            ),
                        ],
                        width=4,
                    ),
                ],
                justify="around",
            ),
            html.Br(),
            dbc.Row(
                dcc.Markdown("Method parameters"),
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        dbc.Fade(
                            [
                                html.Div("Resolution (DPI):"),
                                dcc.Slider(
                                    id="dpi", min=100, max=500, step=50, value=250
                                ),
                            ],
                            id="dpi-col",
                            is_in=True,
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        dbc.Fade(
                            [
                                html.Div("Column name (method 3):"),
                                dcc.Input(id="column_name", type="text", value="col B"),
                            ],
                            id="column_name-col",
                        ),
                        width=4,
                    ),
                ],  # if adding additional children, need to add them to layout_options in set_parameters
                id="parameter_row",
                justify="around",
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Markdown("Editable DataFrame"),
                            dcc.Dropdown(
                                options=[],
                                value=None,
                                id="dropdown_table_selector",
                                placeholder="No table was selected",
                            ),
                            dash_table.DataTable(
                                id="table_results",
                                columns=[],
                                data=[],
                                editable=True,
                            ),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Markdown("PDF page"), width=3),
                                    dbc.Col(
                                        [
                                            dcc.Slider(
                                                marks={1: "1"},
                                                step=None,
                                                value=1,
                                                id="slider_page",
                                                included=False,
                                            ),
                                            dcc.Checklist(
                                                options=[
                                                    {
                                                        "value": "on_bbox",
                                                        "label": " Zoom on selected bounding box",
                                                    },
                                                ],
                                                value=["on_bbox"],
                                                inline=True,
                                                id="graph_options",
                                            ),
                                        ],
                                        width=6,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Button(
                                                "Add a new bounding box",
                                                id="add_bounding_box",
                                                outline=True,
                                                color="success",
                                                class_name="col-12",
                                                size="sm",
                                            ),
                                            dbc.Button(
                                                "Edit the bounding box",
                                                id="get_bounding_box",
                                                outline=True,
                                                color="warning",
                                                class_name="col-12",
                                                size="sm",
                                            ),
                                        ],
                                        width=3,
                                    ),
                                ]
                            ),
                            dcc.Graph(
                                id="graph_image",
                                style={"width": "100vh", "height": "100vh"},
                                config={"responsive": False},
                            ),
                        ],
                        width=6,
                    ),
                ],  # graphs and display of pdf, generated through callback
                id="row_results",
            ),
            dbc.Row(
                [
                    dbc.Button(
                        "Download current table",
                        id="download_current-button",
                        outline=True,
                        color="secondary",
                    ),
                    dbc.Button(
                        "Download all tables",
                        id="download_all-button",
                        outline=True,
                        color="primary",
                    ),
                    dcc.Download(id="download_xls_file"),
                ]
            ),
        ]
    )
)


@callback(
    Output("store_pdf", "data"),
    Output("loading_text_pdf", "children"),
    Output("run_button_text", "children"),
    Output("slider_page", "marks"),
    Output("slider_page", "value"),
    Output("dropdown_table_selector", "options"),
    Output("dropdown_table_selector", "value"),
    Output("table_results", "data"),
    Output("table_results", "columns"),
    State("store_pdf", "data"),
    State("parameters", "data"),
    Input("dropdown_method_selector", "value"),
    Input("run_button", "n_clicks"),
    Input("upload-pdf", "contents"),
    Input("upload-pdf", "filename"),
    Input("slider_page", "value"),
    Input("dropdown_table_selector", "value"),
    Input("table_results", "data"),
)
def read_file(
    pdf_data,
    parameters,
    method,
    run_button,
    file,
    file_name,
    selected_page,
    selected_table,
    table_data,
):
    """
    upload file, display parameters, table update and run process
    """
    triggered_ids = [t["prop_id"] for t in callback_context.triggered]
    # default values for Output that are not also States/Inputs
    page_slider, columns, table_list = [no_update] * 3
    run_button_name = f'Run method "{method}"'
    if file_name is None:
        pdf_data = {}
        if "run_button.n_clicks" in triggered_ids:
            run_button_name = f'Please select a file before running method "{method}"'
        file_name = "Select or drag-and-drop the PDF file to process"
    elif "upload-pdf.contents" in triggered_ids:
        pdf_data = {
            "file": file,
            "file_name": file_name,
            "img": {},  # page: image, will be generated on the process part
        }
    elif "run_button.n_clicks" in triggered_ids:
        print(f"Running method {method} on {file_name}")
        results = DICT_OF_METHODS[method](pdf_data, parameters)
        pdf_data["img"] = results.pop("img")
        page_slider = {page: str(page) for page in pdf_data["img"].keys()}
        results = process_results(
            results["results"]
        )  # note : other keys are discarded for now
        run_button_name = f"Method '{method}' has run"
        print(
            run_button_name
            + f" with parameters {parameters} => {len(results['records'].keys())} tables obtained"
        )
        pdf_data.update(results)
        table_list = list(pdf_data["records"].keys())
        if selected_table not in table_list and len(table_list) > 0:
            selected_table = table_list[0]
        elif len(table_list) == 0:
            selected_table = None
        selected_page = pdf_data["pages"].get(selected_table, 1)
    elif "dropdown_table_selector.value" in triggered_ids:
        selected_page = pdf_data["pages"].get(selected_table, 1)
    elif "slider_page.value" in triggered_ids:
        possible_tables = [
            k for k, p in pdf_data["pages"].items() if p == selected_page
        ]
        if len(possible_tables) == 0:
            selected_table = None
        elif selected_table not in possible_tables:
            selected_table = possible_tables[0]
    elif (
        "table_results.data" in triggered_ids
    ):  # update pdf_data to save any modification after change of selected_table
        pdf_data["records"][selected_table] = table_data

    if ("records" in pdf_data.keys()) and (
        "dropdown_table_selector.value" in triggered_ids
        or "slider_page.value" in triggered_ids
        or "run_button.n_clicks"
    ):  # update table
        if selected_table is not None:
            table_data = pdf_data["records"].get(
                selected_table, ["Run file extraction method with this bounding box"]
            )
            columns = pdf_data["columns"].get(
                selected_table, ["Instructions for new bounding box"]
            )
        else:
            table_data, columns = [], []
    return (
        pdf_data,
        file_name,
        run_button_name,
        page_slider,
        selected_page,
        table_list,
        selected_table,
        table_data,
        columns,
    )


@callback(
    Output("graph_image", "figure"),
    State("store_pdf", "data"),
    Input("parameters", "data"),
    Input("slider_page", "value"),
    Input("dropdown_table_selector", "value"),
    Input("graph_options", "value"),
)
def plot_image(data, parameters, page, selected_table, graph_options):
    """
    display image and bounding boxes
    """
    if data is None or selected_table is None or "img" not in data.keys():
        return px.imshow(np.ones((3, 3, 3)), origin="lower")
    if str(page) not in data["img"].keys():
        print(f'/!\ Page {page} ({type(page)}) not found in {data["img"].keys()}')
        raise PreventUpdate
    fig = px.imshow(
        PIL_Image.open(BytesIO(base64.b64decode(data["img"][str(page)]))),
        binary_string=True,
    )
    fig.update_layout(
        dragmode="drawrect",
        newshape_line_color="red",
        newshape_line_dash="dot",
        autosize=False,
    )
    if "on_bbox" in graph_options and selected_table is not None:
        bbox = parameters["bounding_boxes"][selected_table]
        fig.update_xaxes(
            range=[min([bbox["x0"], bbox["x1"]]), max([bbox["x0"], bbox["x1"]])]
        )
        fig.update_yaxes(
            range=[max([bbox["y0"], bbox["y1"]]), min([bbox["y0"], bbox["y1"]])]
        )

    count = 0
    for idx, bbox in parameters.get("bounding_boxes", {}).items():
        if parameters["pages"].get(idx, None) != page:
            continue
        count += 1
        color_angle = (count * 76) % 360
        fig.add_shape(
            type="rect",
            x0=bbox["x0"],
            y0=bbox["y0"],
            x1=bbox["x1"],
            y1=bbox["y1"],
            fillcolor=f"hsl({color_angle}, 1, .5)",
            opacity=0.2,
            line={"color": "black", "width": 3 if idx == selected_table else 0},
        )
    return fig


# parameters
@callback(
    Output("dpi-col", "is_in"),
    Output("column_name-col", "is_in"),
    # end of hideable parameter. if more are added, also update "layout_options"
    Output("parameters", "data"),
    State("parameters", "data"),
    State("slider_page", "value"),
    State("dropdown_table_selector", "value"),
    State("graph_image", "relayoutData"),
    Input("dropdown_method_selector", "value"),
    Input("store_pdf", "data"),
    Input("get_bounding_box", "n_clicks"),
    Input("add_bounding_box", "n_clicks"),
    # method parameters:
    Input("dpi", "value"),
    Input("column_name", "value"),
)
def set_parameters(
    parameters,
    page_selected,
    table_selected,
    figure_annotations,
    method,
    pdf_data,
    get_bounding_box,
    add_bounding_box,
    dpi,
    column_name,
):
    """
    Parameters, used to modify bounding boxes
    """
    triggered_ids = [t["prop_id"] for t in callback_context.triggered]
    layout_options = ["dpi", "column_name"]
    method_parameters = DICT_OF_PARAMETERS.get(method, ["dpi"])
    for key in method_parameters:
        parameters[key] = eval(key)  # /!\ use key for parameter in set_parameters
    if "dropdown_method_selector.value" in triggered_ids:
        parameter_children = []
        for key in layout_options:
            parameter_children.append(key in method_parameters)
        parameter_children.append(parameters)
        # for other_outputs in range(1):
        #     parameter_children.append(no_update)
        return tuple(parameter_children)
    elif any([i.split(".")[0] in method_parameters for i in triggered_ids]):
        for key in method_parameters:
            parameters[key] = eval(key)  # /!\ use key for parameter in set_parameters
    elif pdf_data is None:
        raise PreventUpdate
    elif "store_pdf.data" in triggered_ids:
        if pdf_data is None:
            pdf_data = {}
        parameters = pdf_data.get("parameters", {})
        parameters["bounding_boxes"] = pdf_data.get("bounding_boxes", {})
        parameters["pages"] = pdf_data.get("pages", {})
        for key in method_parameters:
            if key not in parameters.keys():
                parameters[key] = eval(
                    key
                )  # /!\ use copmponent id as parameter in set_parameters
    elif not isinstance(figure_annotations, dict):
        raise PreventUpdate
    elif (
        "get_bounding_box.n_clicks" in triggered_ids
        or "add_bounding_box.n_clicks" in triggered_ids
    ):
        bbox = [
            shape
            for shape in figure_annotations.get("shapes", [])
            if shape.get("type", "unknown") == "rect"
        ]
        if len(bbox) > 0:
            if (
                "get_bounding_box.n_clicks" in triggered_ids
                and table_selected is not None
            ):
                table_index = table_selected
            else:
                table_index = f"new_bounding_box {add_bounding_box}"
            parameters["bounding_boxes"][table_index] = {
                k: bbox[-1][k] for k in ["x0", "y0", "x1", "y1"]
            }
            parameters["pages"][table_index] = page_selected
    return tuple(
        [no_update] * len(layout_options) + [parameters]  # hideable parameters
    )


@callback(
    Output("download_xls_file", "data"),
    State("store_pdf", "data"),
    State("upload-pdf", "filename"),
    State("dropdown_table_selector", "value"),
    Input("download_current-button", "n_clicks"),
    Input("download_all-button", "n_clicks"),
    prevent_initial_call=True,
)
def download_tables(
    data, file_name, selected_table, download_current, download_selection
):
    """
    Export the tables
    TODO: add some kind of selector to get all / some of the table and replace the download all button ?
    """
    triggered_ids = [t["prop_id"] for t in callback_context.triggered]
    export_name = file_name[: file_name.rfind(".")] + "_extracted"
    if (
        "download_current-button.n_clicks" in triggered_ids
        and selected_table is not None
    ):
        df = pd.DataFrame.from_records(data["records"][selected_table])
        return dcc.send_data_frame(
            df.to_excel, f"{export_name}.xlsx", sheet_name="Table"
        )
    else:

        def to_xlsx(bytes_io):
            writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")
            for n, records in enumerate(data["records"].values()):
                pd.DataFrame.from_records(records).to_excel(
                    writer, sheet_name=f"Table {n + 1}"
                )
            writer.save()

        return dcc.send_bytes(to_xlsx, f"{export_name}.xlsx")


if __name__ == "__main__":
    app.run_server(debug=True)
