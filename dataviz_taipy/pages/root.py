# https://www.taipy.io/posts/how-to-create-an-ai-photo-app-with-python
from taipy.gui import Markdown


def to_text(val):
    return '{:,}'.format(int(val)).replace(',', ' ')

data4good_logo_path = './images/data4good-logo.svg'
taxplorer_logo_path = './images/taxplorer-logo.svg'
website_logo_path = './images/website-logo.svg'
twitter_logo_path = './images/twitter-logo.svg'
linkedin_logo_path = './images/linkedin-logo.svg'
eutax_logo_path = './images/eutax-logo.svg'

logo_path = './data/logo.png'
root = Markdown("pages/root.md")