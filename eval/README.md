# Evaluation of the table extraction

This folder contains evaluation tools (scripts, Streamlit app) allowing you to visually & (NEW!) quantitatively compare tables extracted via multiple parsing methodologies (LlamaParse, ExtractTable, Unstructured, etc.) and for multiple PDF reports. The goal is to select the best parsing methodology for our extraction lib.

## Getting started

The easiest way to get started is to launch the Streamlit eval app:

```
streamlit run eval/eval_app.py eval/data/data_step2_before-currency-unit_eval.csv
```

Right after launch, you'll need to select a pickle file to load. Luckily, we already generated one for you: select `eval_20240501_161202.pkl` in the `eval/data/` directory. This file contains tables from 15 PDF reports and extracted via 6 parsing methodologies (1 FromCSV/ExtractTable, 1 LlamaParse, 2 Unstructured API & Local).

The app will then allow you to select a PDF report, see the pages of the PDF report containing the tables to be extracted and their extracted versions for each parsing methodology. Note the red/green colors allowing you to visually compare the tables.

Note the `data_step2_before-currency-unit_eval.csv` argument on the above command line. This argument is optional and allows you to compare extracted tables against reference tables manually produced by the TaxObservatory team.

## Quantitative analysis (NEW!)

In addition to visual comparison, the streamlit app computes a recall rate. For a given extraction methodology, we define the recall rate as the share of numeric values in the reference table that are present in the extracted tables. To compute the recall rate, reference data is required (see above).

The Streamlit app also prints in the terminal a recall matrix, that is the recall rate (%) for all the PDF reports and all the extraction methodologies. See the recall matrix for `eval_20240501_161202.pkl`:

|                                        |   from_csv |   llama_parse |   unstructured_api |   unstructured_api_1 |   unstructured |   unstructured_1 |
|:---------------------------------------|-----------:|--------------:|-------------------:|---------------------:|---------------:|-----------------:|
| ACS_2019_CbCR_3.pdf                    |         94 |           100 |                 44 |                    6 |             94 |               94 |
| ACS_2021_CbCR_2-3.pdf                  |        100 |           100 |                100 |                  100 |            100 |              100 |
| AXA_2021_CbCR_24-27.pdf                |         96 |           100 |                 96 |                    0 |             82 |                0 |
| Acciona_2020_CbCR_1.pdf                |         58 |           100 |                 82 |                    0 |             93 |                0 |
| Acerinox_2020_CbCR_1.pdf               |        100 |           100 |                100 |                  100 |             91 |               97 |
| Aegon_2020_CbCR_13.pdf                 |         96 |           100 |                 77 |                   77 |             93 |               93 |
| AkerSolutions_2015_CbCR_16.pdf         |        100 |            76 |                100 |                  100 |            100 |              100 |
| Allianz_2017_CbCR_7.pdf                |         94 |            50 |                 12 |                    0 |             81 |                0 |
| AmericaMovil_2019_CbCR_1.pdf           |         98 |           100 |                 75 |                    0 |             69 |                0 |
| AngloAmerican_2018_CbCR_4-5.pdf        |        100 |           100 |                 98 |                   98 |             92 |               95 |
| Applus_2021_CbCR_1.pdf                 |        100 |           100 |                 90 |                   67 |            100 |              100 |
| Atlantia_2019_CbCR_1.pdf               |        100 |            83 |                 95 |                    0 |             93 |                0 |
| AutostradePerL'Italia_2022_CbCR_78.pdf |          0 |           100 |                 20 |                    0 |             70 |                0 |
| ENI_2018_CbCR_12-13.pdf                |        100 |           100 |                100 |                  100 |             91 |               97 |
| Enel_2020_CbCR_123-126.pdf             |         30 |            70 |                 30 |                   29 |             28 |               16 |

## Generate & use your own evaluation data

You can instead generate your own evaluation data in a new picke file and load it in the streamlit app.

### Setup

Install the following package that is used to generate PDF output files.

```
apt-get install wkhtmltopdf
```

### Data generation

Run the `eval_table_extraction.py` script. This script will iterate through several PDF reports and apply the set of table extraction algorithms you provided in your yaml configuration. Check out `configs/eval_table_extraction.yaml` for a suitable yaml configuration.

You can run the script as:

```
python3 eval/eval_table_extraction.py configs/eval_table_extraction.yaml ./example_set/inputs/ ./example_set/extractions/
```

This will apply the pipeline for all the reports in the `./example_set/inputs` directory and save :

- the extracted tables with all the algorithms in one output PDF file per input report in the
  `./example_set/extractions` directory
- all the extracted assets in a pickle file `eval_xxxx.pkl` located in the `eval/data/` directory
