import pandas as pd
import json


# path_to_data = "data/dataset_multi_years_cleaned_completed.tab"
# data = pd.read_csv(path_to_data, sep='\t', low_memory=False)
path_to_data = "./data/data_final_dataviz.csv"
data = pd.read_csv(path_to_data, sep=',', low_memory=False)

# vaccination = pd.read_csv("data/vaccination-data.csv")

# with open("data/countries.geojson") as f:
#     geojson = json.load(f)