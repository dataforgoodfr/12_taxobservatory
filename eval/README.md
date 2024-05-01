# Evaluation of the table extraction

## Setup

To run the evaluation scripts, we need some additional requirements that are not listed in the project dependencies.

```
apt-get install wkhtmltopdf
```

## Generate evaluation data

First, you need to generate evaluation data with the `eval_table_extraction.py` script. This script will iterate through several reports and apply the set of table extraction algorithms you provided in your yaml configuration. 

As an example, you might select the pages in the report from their filename and then apply several table extraction algorithms. Check out `configs/eval_table_extraction.yaml` for a suitable evaluation script.

You can then call the script as :

```
python eval/eval_table_extraction.py configs/eval_table_extraction.yaml
./example_set/inputs/ ./example_set/extractions
```

This will apply the pipeline for all the reports in the `./example_set/inputs` directory and save :

- the extracted tables with all the algorithms in one output PDF file per input report in the
  `./example_set/extractions` directory
- all the extracted assets in a pickle file `eval_xxxx.pkl` located in the `eval/data/` directory

## Evaluation with a streamlit app

To facilitate the evaluation of the extractions, you can run the streamlit app `eval/eval_app.py`. 

To run the application, it is as simple as :

```
streamlit run eval/eval_app.py eval/data/data_step2_before-currency-unit_eval.csv
```

`data_step2_before-currency-unit_eval.csv` is a cleaned up version of the `data_step2_before-currency-unit.csv` file which contains reference data extracted and manually cleaned up by the team.

At launch, you will be requested to provide a pickle file with extracted data. You might select `eval_20240408_200249.plk` in the `eval/data/` directory. It contains extracted tables for multiple reports and extractions and is a great way to get started.
