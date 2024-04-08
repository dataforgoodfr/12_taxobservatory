from taipy.gui import Markdown

import numpy as np

from dataviz_taipy.data.data import data


def to_text(val):
    return '{:,}'.format(int(val)).replace(',', ' ')

logo_path = './data/image.png'
root = Markdown("pages/root.md")