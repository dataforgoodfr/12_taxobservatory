import numpy as np
import pandas as pd

from taipy.gui import Markdown

from dataviz_taipy.data.data import data


layout = {'barmode':'stack', "hovermode":"x"}
options = {"unselected":{"marker":{"opacity":0.5}}}

df = data.head()

home_md = Markdown("pages/home/home.md")