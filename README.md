# EU Tax Observatory

# Usage

## Installing

To install the library in a dedicated virtual environnement :

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install git+https://github.com/dataforgoodfr/12_taxobservatory.git
```

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

# Avaiable blocks

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

- [Camelot](#camelot)
- [Unstructured API](#unstructured-api)
- [Unstructured](#unstructured)
- [Llama parse](#llama-parse)

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

### Llama parse

## Table cleaning

### LangChain / LangSmith

## Using the building blocks involving an API

### OpenAI

The data extraction may involve a block requiring an OpenAI API Key. To use it, you need to request for an API Key on the [OpenAI website](https://openai.com/blog/openai-api).

### LangChain

The data extraction may involve a block requiring a LangChain API Key. In
particular, for tracing LLM, you need an API key for LangSmith. You need to
login on the [LangSmith](https://smith.langchain.com) website and create an API
Key. 

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
