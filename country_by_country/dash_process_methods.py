
# mocked module for processing methods
import base64, json
from copy import deepcopy
from io import BytesIO
import pypdfium2
import numpy as np
import pandas as pd


"""
Instructions : 
    Put here function to process pdf, then update DICT_OF_METHODS & DICT_OF_PARAMETERS 

Function parameters should be :
    data : dict, data["file"] is the PDF content
    parameters : dict, for user defined parameters (see Dash app in case it requires others params than dpi)
Function outputs should be :
   a dict with at least
      "img": dict of str (containing b64 encoded PDF pages)
      "results": dict of dict or dict of list
            keys expected for results dict : 
                "pages": page number
                "bounding_boxes": dict, as x0, y0, x1, y1, or list of these 4 corners
                "tables": pd.DataFrame
            if a dict is provided, the key will be used for table selection in Dash app
            process_results() can be used to verify correct formatting
"""


def convert_pdf_to_image(file_content:str, dpi=250):
    """
    Some method to convert pdf to image 
    (needed for Dash app if not already done during the extraction process)
    """
    document = pypdfium2.PdfDocument(
        BytesIO(base64.b64decode((
            file_content[file_content.find(";base64,") + len(";base64,"):]
            )))
        )
    image_dict = {}
    for nb, page in enumerate(document):
        buffered = BytesIO()
        page.render(
            scale=dpi / 72, # resolution conversion, base = 72dpi
            ).to_pil().save(buffered, format="JPEG")
        image_dict[nb + 1] = (
            #"data:image/jpeg;base64,"
            base64.b64encode(buffered.getvalue()).decode("utf-8")
            )   
    return image_dict


def method_example(data, parameters):
    """
    A mock-up method for demo
    """
    results = {"tables" : [pd.DataFrame([[10,11 ], [12,13]], columns=["A", "B"])],
              "pages": [1],
              "bounding_boxes": [{"x0": 0, "y0": 0, "x1": 100, "y1": 150}]
                }

    return {"results": results, 
            "img": convert_pdf_to_image(data["file"], 
                                        dpi=parameters["dpi"])}


def method_2(data, parameters):
    """
    This methods provide a bounding box and bounding box coordinates
    """
    dpi = parameters["dpi"]
    result = pd.DataFrame(columns=["page", "x0", "y0", "x1", "y1"])

    img = convert_pdf_to_image(data["file"],
                              dpi=dpi)
    default_bbox = np.array([250, 250, 1500, 1500]) / 200 * dpi
    default_bbox = {"x0": default_bbox[0], "y0": default_bbox[1],
                  "x1": default_bbox[2], "y1": default_bbox[3]}
                
    if len(parameters.get("bounding_boxes", {})) == 0:
        # init bbox if they do not exist yet for demo purpose
        bboxes = {page: default_bbox for page in img.keys()}
        pages = {page: page for page in img.keys()}
    else:    
        bboxes = parameters.get("bounding_boxes", {})
        pages = parameters.get("pages", {})
    results = {"tables": [], 
               "pages": [], 
               "bounding_boxes": []}
    for idx in bboxes.keys():
        result.at[idx, "page"] = pages[idx]
        for col in ["x0", "y0", "x1", "y1"]:
            result.at[idx, col] = np.round(bboxes[idx][col], 1)
        results["tables"].append(result.loc[[idx]].round(1))
        results["pages"].append(pages[idx])
        results["bounding_boxes"].append(bboxes[idx])
    return {"results": results,
            "img": img,
            }

def method_3(data, parameters):
    """
    This method uses another parameter
    """
    results = {"tables" : [pd.DataFrame([[1, 2], [100,200]], 
                          columns=["A3", str(parameters.get("column_name", "B3"))]
                          )],
              "pages": [1],
              "bounding_boxes": [{"x0": 0, "y0": 0, "x1": 100, "y1": 150}]
                }
    results["tables"][0]["A3"] *= parameters.get("coeff", 10)
    return  {"results": results, 
             "img": convert_pdf_to_image(data["file"],
                                         dpi=parameters["dpi"]),
             }

def show_bounding_box(data, parameters):
    img = convert_pdf_to_image(data["file"],
                                dpi=parameters["dpi"])
    result = pd.DataFrame(columns=["page", "x0", "y0", "x1", "y1"])
    bboxes = parameters.get("bounding_boxes", {})
    pages = parameters.get("pages", {})
    results = {"tables": [], 
               "pages": [], 
               "bounding_boxes": []}
    for idx in bboxes.keys():
        result.at[idx, "page"] = pages[idx]
        for col in ["x0", "y0", "x1", "y1"]:
            result.at[idx, col] = np.round(bboxes[idx][col], 1)
        results["tables"].append(result.loc[[idx]])
        results["pages"].append(pages[idx])
        results["bounding_boxes"].append(bboxes[idx])
    return {"results": results,
            "img": img,
            }

def process_results(results: dict):
    """
    will be used in the dash app 
    Sanity check of results + formatting if not providing a dict
    """
    if "results" in results.keys():
        r = process_results(results["results"])
        results["results"] = r
        return results
    expected_keys = ["tables", "pages", "bounding_boxes"]
    if (not isinstance(results, dict)
        or any([key not in results.keys() for key in expected_keys])
        ):
        raise TypeError("Unable to read the format of results")
    if len(np.unique([len(results[key]) for key in expected_keys])) != 1:
        raise ValueError(f"All outputs should have the same length in {expected_keys}")
    if isinstance(results[expected_keys[0]], dict):
        for r in results[expected_keys[0]].keys():
            if any([r not in results[key] for key in expected_keys]):
                raise ValueError(
                    f"All outputs shoud share the same keys in {expected_keys}. Some are missing for {r}"
                    )
    else:
        # convert results from list to dict
        results_as_list = deepcopy(results)
        results = {k: {} for k in expected_keys}
        count = 0
        for page in np.unique(results_as_list["pages"]):
            for i in np.where(np.array(results_as_list["pages"]) == page)[0]:
                count += 1
                table = results_as_list["tables"][i]
                idx = f"{count + 1}: {table.shape[0]} x {table.shape[1]} [p.{page}]"
                results["tables"][idx] = table
                results["pages"][idx] = results_as_list["pages"][i]
                results["bounding_boxes"][idx] = results_as_list["bounding_boxes"][i]
    for idx, bbox in results["bounding_boxes"].items():
        if not isinstance(bbox, dict) and len(bbox) == 4: # try to convert as x0, y0, x1, y1
                    results["bounding_boxes"][idx] = {
                        key: bbox[n]
                        for n, key in enumerate(["x0", "y0", "x1", "y1"])
                        }
        elif not isinstance(bbox, dict) or any([key not in bbox.keys() for key in ["x0", "y0", "x1", "y1"]]):
            raise ValueError(f"Error in formatting of 'bounding_boxes', expecting dict containing 'x0', 'y0', 'x1', 'y1' or a list of 4 values")
    results["columns"] = {key: [{"id": c, "name": c, "hideable": True}
                                for c in df.columns]
                            for key, df in results["tables"].items()}
    results["records"] = {key: df.to_dict(orient="records")
                            for key, df in results["tables"].items()}
    _ = results.pop("tables") # avoid serialisation error
    return results

DICT_OF_METHODS = {
    "Method 1": method_example,
    "Method 2": method_2,
    "Method 3": method_3,
    "Show bounding_boxes in table": show_bounding_box,
    }
DICT_OF_PARAMETERS = {
    "Method 1": ["dpi"], 
    # "Method 2": ["dpi"], # optional : default is also set in the set_parameter callback
    "Method 3": ["dpi", "column_name",]
    } # link here parameters to layout component id
DEFAULT_METHOD = "Method 2"