# https://www.taipy.io/posts/how-to-create-an-ai-photo-app-with-python
from taipy.gui import Markdown


def to_text(val):
    return '{:,}'.format(int(val)).replace(',', ' ')

logo_path = './data/logo.png'
root = Markdown("pages/root.md")