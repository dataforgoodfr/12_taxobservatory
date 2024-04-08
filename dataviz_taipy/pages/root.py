from taipy.gui import Markdown

import numpy as np

def to_text(val):
    return '{:,}'.format(int(val)).replace(',', ' ')

logo_path = './data/image.png'
root = Markdown("pages/root.md")