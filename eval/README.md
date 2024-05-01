# Evaluation of the table extraction

## Evaluate extractions with the streamlit eval app

To get started, run the streamlit eval app as:

```
streamlit run eval/eval_app.py eval/data/data_step2_before-currency-unit_eval.csv
```

This app allows you to visually compare tables extracted via multiples methodologies and for multiple reports. It needs two input files (only one mandatory):
- *[Optional]* The optional REF data file `data_step2_before-currency-unit_eval.csv` is a cleaned up version of `data_step2_before-currency-unit.csv`. The latter file contains reference data extracted and manually cleaned up by the TaxObservatory team and allows you to benchmark the extractions against it.
- *[Mandatory]* At launch, the app will request you to provide a pickle file with extracted data. Select `eval_20240408_200249.plk` in the `eval/data/` directory to not have to generate evaluation data yourself and get started easily!

## Generate your own evaluation data

You can instead generate your own picke file containing extracted data.

### Setup

Install the following package that is used to generate PDF output files.

```
apt-get install wkhtmltopdf
```

### Data generation

Run the `eval_table_extraction.py` script. This script will iterate through several reports and apply the set of table extraction algorithms you provided in your yaml configuration. Check out `configs/eval_table_extraction.yaml` for a suitable yaml configuration.

You can run the script as:

```
python eval/eval_table_extraction.py configs/eval_table_extraction.yaml
./example_set/inputs/ ./example_set/extractions
```

This will apply the pipeline for all the reports in the `./example_set/inputs` directory and save :

- the extracted tables with all the algorithms in one output PDF file per input report in the
  `./example_set/extractions` directory
- all the extracted assets in a pickle file `eval_xxxx.pkl` located in the `eval/data/` directory
