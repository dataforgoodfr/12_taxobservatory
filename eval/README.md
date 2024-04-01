# Evaluation of the table extraction

## Qualitative evaluation

The evaluation is performed with the `eval_table_extraction.py` script. This
script will iterate through several reports and apply the set of table
extraction algorithms you gave in your yaml configuration. 

As an example, you might consider selecting the pages in the report from their
filename and then apply several table extraction algorithms :

A suitable `config.yaml` script would be :

```
pagefilter:
  type: FromFilename

table_extraction:
  - type: Unstructured
    params:
      hi_res_model_name: "yolox"
  - type: Unstructured
    params:
      hi_res_model_name: "yolox"
      pdf_image_dpi: 300
  - type: Unstructured
    params:
      hi_res_model_name: "yolox"
      pdf_image_dpi: 500
  - type: UnstructuredAPI
    params:
      hi_res_model_name: "yolox"
  - type: LLamaParse
```

You can then call the evaluation script as :

```
python eval/eval_table_extraction.py configs/eval_table_extraction.yaml
./example_set/inputs/ ./example_set/extractions
```

This will apply the pipeline for all the reports in the `./example_set/inputs`
directory and save :

- the extracted tables with all the algorithms in one file per report in the
  `./example_set/extractions` directory
- all the extracted assets in a pickle file in the current directory `eval_xxxx.pkl`

## Comparison with a streamlit app

To facilitate the qualitative comparison of the extractions, you can use the
streamlit app `eval/eval_app.py`. 

To run the application, it is as simple as :

```
streamlit run eval/eval_app.py
```

If you have access to the `data_step2_before-currency-unit.csv` extraction of
the tax observatory, you can give its path to the command line :


```
streamlit run eval/eval_app.py ./path/to/data_step2_before-currency-unit.csv
```
