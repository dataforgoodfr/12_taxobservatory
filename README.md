# EU Tax Observatory

# Usage

## Installing

To install the library in a dedicated virtual environnement :

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install git+https://github.com/dataforgoodfr/12_taxobservatory.git
```

## Download the reports locally

To download the reports, you can use the script `collecte/pdf_downloader.py`. You will need a [Google API key](https://developers.google.com/custom-search/v1/introduction) as well as a search engine ID (or [CX code](https://www.google.com/cse/all)).  


# Run the streamlit app
To start the stremlit app and use the extractor streamlined version, start it locally by running

`streamlit run app/index.py`

The app comes with page detection and parsers default config but you can change it by providing a yaml file following the config.yaml format below. 



## Running the pipeline from the command line

To run the pipeline from the command line, once installed, you can invoke the
`country_by_country` module on a pdf file as :

```
python3 -m country_by_country config.yaml report.pdf
```

The yaml file is describing the pipeline you want to execute. For now, you can
specify the page filter and the table extraction algorithms. An example
`config.yaml` file is given below :


**config.yaml**
```
pagefilter:
  type: RFClassifier
  params: 
    modelfile: random_forest_model_low_false_positive.joblib

table_extraction:
  img:
    - type: Camelot
      params:
        flavor: stream
    - type: Unstructured
      params:
        pdf_image_dpi: 300
        hi_res_model_name: "yolox"

table_cleaning:
  - type: LLM
    params:
      openai_model: "gpt-4-turbo-preview"
```

This config file uses:
- a pretrained random forest for selecting the pages of the report that possibly
  contain a CbCR table
- camelot with its stream flavor and unstructured with yolox as the table
  detector for locating and parsing the tables on the previously selected pages
- LangChain with GPT-4-turbo-preview for requesting the parsed tables to extract
  and re-order the necessary informations

# Available blocks

## Page filter

A page filter takes as input a pdf filepath and fills in the assets under the
key `pagefilter`:

- `src_pdf`: the path to the original pdf
- `selected_pages`: the list of indices of the selected pages. The indices are 0
  based.

The available filters are :

- [Copy As is](#copy-as-is)
- [From filename](#from-filename)
- [RF Classifier](#rf-classifier)


### Copy as is

This filter does not perform any selection on the input document and just copy
the whole content as is.

### From filename

This filter expects the pages to extract from the input filename either as a
single page number or a page range. Valid names are given below :

- `arbitrarily_long_and_cumBerSOME_prefix_PAGENUMBER.pdf` : gets the page
  numbered PAGENUMBER
- `arbitrarily_long_and_cumBerSOME_prefix_PAGENUMBER1-PAGENUMBER2.pdf` : gets the range [PAGENUMBER1, PAGENUMBER2]

### RF Classifier

This filter uses a random forest trained to identify the pages from the text the
pages content. Several features are used to identify relevant pages such as :

- the number of country names listed in the page
- the presence of keywords such as "tax", "countr", "report", "cbc", .."


## Table extraction

We allow multiple table extraction algorithms to be used simultaneously. This is
the reason why the `table_extraction` key of the `config.yaml` is a list. A
table extraction algorithm fills in the assets under the key
`table_extractors`, which is a list containing the assets for every algorithm
you considered. Every algorithm provides the following assets :

- `id`: a unique identifier for this algorithm
- `type`: the algorithm type, can be any of the listed algorithms below `camelot`, `unstructured`, `unstructured_api`,  `llama_parse`
- `params`: the named parameters and their values given to the construction of
  the algorithm
- `tables`: the list of extracted tables as pandas dataframes 

The following table extractors can be considered :

- [ExtractTable][#extracttable]
- [Camelot](#camelot)
- [Unstructured API](#unstructured-api)
- [Unstructured](#unstructured)
- [Llama parse API](#llama-parse-api)

### ExtractTable

ExtractTable is provided for legacy/benchmarking purpose. The
[ExtractTable](https://github.com/ExtractTable/ExtractTable-py) python module is
no more maintained but this was originally the package used to extract data from
PDF tables.

You can use by specifying in the `config.yaml`:

```
table_extraction:
    - type: ExtractTableAPI
```

It requires an API key to be defined in your `.env` file :

```
# Required for table exctration with ExtractTable API
EXTRACTABLE_API_KEY=CHANGE_ME

```

### Camelot

Camelot is a python library for extracting tables. The documentation is
available at
[https://camelot-py.readthedocs.io/en/master/](https://camelot-py.readthedocs.io/en/master/).

We can use two flavors : `stream` or `lattice`. It can be specified in the
config as :

```
table_extraction:
  - type: Camelot
    params:
      flavor: stream
```

### Unstructured API

The unstructured API is documented at
[https://unstructured-io.github.io/unstructured/apis/api_sdks.html](https://unstructured-io.github.io/unstructured/apis/api_sdks.html). In the `config.yaml`, you can specify any of the parameters considered by [shared.PartitionParameters](https://github.com/Unstructured-IO/unstructured-python-client/blob/main/docs/models/shared/partitionparameters.md) although we already set `strategy="hi_res", pdf_infer_table_structure="True"`.

For example, you can use their beta released model `chipper` by setting in your
`config.yaml` :

```
table_extraction:
    - type: UnstructuredAPI
      params:
        hi_res_model_name: chipper 
```

This API requires an API key. You can create one at
[https://unstructured.io/api-key-free](https://unstructured.io/api-key-free).
Once you have your key, you must copy the sample `.env.sample` to `.env` :

```
cp .env.sample .env
```

and then copy your key at 
```
UNSTRUCTURED_API_KEY=CHANGE_ME
```

### Unstructured

In addition to use the unstructured API, you can also run unstructured locally.
The parameters to be specified in your `config.yaml` script are given to the
[partition_pdf function](https://unstructured-io.github.io/unstructured/core/partition.html#partition-pdf), although we already set `strategy="hi_res", infer_table_structure=True`.

You can for example set the `pdf_image_dpi` as well as the table detection
algorithm by setting :

```
table_extraction:
    - type: Unstructured
      params:
        pdf_image_dpi: 300
        hi_res_model_name: "yolox"
```

### Llama parse API

The [llama parse](https://github.com/run-llama/llama_parse) requires an API key.
To create a key, go to [http://cloud.llamaindex.ai](http://cloud.llamaindex.ai).
This key must be specified in the `.env` file, a sample file being `.env.example` :

```
# Required for table extraction with LLAMA PARSE API
LLAMA_CLOUD_API_KEY=CHANGE_ME
```

You can then use llama parse in your configuration as below. The parameters are
forward to the constructor of
[LlamaParse](https://github.com/run-llama/llama_parse/blob/97c7a38a69f34a6d4d9c633a873de7afd57ce93d/llama_parse/base.py#L172)

For example, you can customize the verbosity, ..

```
table_extraction:
    - type: LlamaParse
      params:
        verbosity: False
```

## Table cleaning

Table cleaning is the last step of the pipeline, taking as input the parsed
tables and extracting the relevant information. You can specify multiple table
cleaners and that's the reason why `table_cleaning` is a list in the
`config.yaml`. Every list of tables extracted by every table extractor will be
processed by every table cleaner. 

The table cleaners append their assets in the list under the `table_cleaners`
key. As for the table extractors, the table cleaners fill in the following
assets :

- `id`: a unique identifier for the table cleaner execution
- `type`: the type of table cleaner
- `params`: the parameters given for the construction of the cleaner
- `table`: the output dataframe with the expected data per country

The list of available cleaners is given below :

- [Langchain / LangSmith](#langchain--langsmith)


### LangChain / LangSmith

The [LangChain](https://python.langchain.com/docs/get_started/introduction)
module can be used by specifying in the `config.yaml`:

```
table_cleaning:
    - type: LLM
      params: 
        openai_model: "gpt-4-turbo-preview"
```

For now, we only support OpenAI models but we may later also consider local
models. For OpenAI models, you need an API key (see [OpenAI website](https://openai.com/blog/openai-api)) that must be provided in your
`.env` file :

```
OPENAI_API_KEY=CHANGE_ME
```

With LangChain, you can also trace the LLMs request using [LangSmith](https://docs.smith.langchain.com/tracing). Although optional, this might be usefull to keep an eye on the expenses for paid language models and to debug the context/questions/answers. LangSmith requires an API key to be created by login in at [https://smith.langchain.com](https://smith.langchain.com) and a project name provided in your `.env` file as :

```
LANGCHAIN_API_KEY=CHANGE_ME
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT="country-by-country"
```


# Contributing

## Use a venv

    python3 -m venv name-of-your-venv

    source name-of-your-venv/bin/activate

## Utiliser Poetry

[Installer Poetry](https://python-poetry.org/docs/):

    python3 -m pip install "poetry==1.4.0"

Installer les dépendances:

    poetry install

Ajouter une dépendance:

    poetry add pandas

Mettre à jour les dépendances:

    poetry update

## Utiliser Jupyter Notebook

    jupyter notebook

and check your browser !

## Lancer les precommit-hook localement

[Installer les precommit](https://pre-commit.com/)

    pre-commit run --all-files

## Utiliser Tox pour tester votre code

    tox -vv

# Notebooks

## Démonstrateur du pipeline

<a target="_blank" href="https://colab.research.google.com/github/dataforgoodfr/12_taxobservatory/blob/main/notebooks/demo_notebook_pipeline.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>


## Detection des pages contenant un tableau CbCR

### Decision tree et random forest

Le filtre `country_by_country/pagefilter/RFClassifier` utilise un arbre de décision ou des random forest entrainés par le notebook ci-dessous

<a target="_blank" href="https://colab.research.google.com/github/dataforgoodfr/12_taxobservatory/blob/main/notebooks/page_filter_randomforest.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## Détection de Tableau

Deux modèles semblent concluants mais ne produisent pas les mêmes résultats.

### Détection de tableau avec Yolox

<a target="_blank" href="https://colab.research.google.com/github/dataforgoodfr/12_taxobservatory/blob/main/notebooks/table_detection_yolox.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

### Détection de tableau avec Microsoft Table Transformer

<a target="_blank" href="https://colab.research.google.com/github/dataforgoodfr/12_taxobservatory/blob/main/notebooks/table_detection_table_transformer.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## RAG

### Llama parse + Llama index

<a target="_blank" href="https://colab.research.google.com/github/dataforgoodfr/12_taxobservatory/blob/main/notebooks/llamaindex_table_extraction.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>
