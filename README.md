# EU Tax Observatory

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
