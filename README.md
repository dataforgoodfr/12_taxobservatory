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

## Avaiable blocks

### Page filter

#### Copy as is

This filter does not perform any selection on the input document and just copy
the whole content as is.

#### From filename

This filter expects the pages to extract from the input filename either as a
single page number or a page range. Valid names are given below :

- `arbitrarily_long_and_cumBerSOME_prefix_PAGENUMBER.pdf` : gets the page
  numbered PAGENUMBER
- `arbitrarily_long_and_cumBerSOME_prefix_PAGENUMBER1-PAGENUMBER2.pdf` : gets the range [PAGENUMBER1, PAGENUMBER2]

#### RF Classifier

This filter uses a random forest trained to identify the pages from the text the
pages content. Several features are used to identify relevant pages such as :

- the number of country names listed in the page
- the presence of keywords such as "tax", "countr", "report", "cbc", .."

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
