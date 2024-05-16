# data source https://drive.google.com/drive/folders/1E7ejgm7rYLMx3IwhUCrHJuf6EseDJgl0
# https://www.figma.com/proto/S5mYPmPeLSvPp4AoS5hf8x/Observatoire-de-la-fiscalit%C3%A9?page-id=0%3A1&type=design&node-id=59-93&viewport=701%2C312%2C0.37&t=EDuRKVhhwQ2t8n8F-1&scaling=scale-down

from taipy.gui import Gui
import taipy as tp

from pages.viz.viz import viz_md
from pages.home.home import home_md
from pages.country.country import country_md
from pages.company.company import company_md
from pages.sector.sector import sector_md
from pages.keystories.keystories import keystories_md
from pages.methodology.methodology import methodology_md
from pages.contact.contact import contact_md
# from pages.world.world import world_md
# from pages.map.map import map_md
# from pages.predictions.predictions import predictions_md, selected_scenario


from pages.root import root
# from dataviz.viz_library import VizLibrary
from pages.country.country import selected_country, selector_country
from pages.company.company import selected_company, selector_company

from config.config import Config

pages = {
    '/': root,
    # 'Viz': viz_md,
    'Home': home_md,
    'KeyStories': keystories_md,
    'Company': company_md,
    'Sector/Country': country_md,
    # 'Sector': sector_md,
    'Methodology': methodology_md,
    'Contact': contact_md,
    # "Country": country_md,
    # "World": world_md,
    # "Map": map_md,
    # "Predictions": predictions_md
}


gui_multi_pages = Gui(
    pages=pages,
    # libraries=[VizLibrary()],
    css_file="css/style.css",
    )


stylekit = {
    #BADA55
  "color_primary": "#FF462B",
  "color_secondary": "#C0FFE",
  "color_paper_light":"#FFFFFF",
  "color_background_light":"#F2F2F2",
  # "color-contrast-light":rgba(0, 0, 0, 0.87),
  "font_family": "Manrope"
}

if __name__ == '__main__':
    tp.Core().run()
    gui_multi_pages.run(
        dark_mode=False,
        stylekit=stylekit,
        title="taxobservatory"
    )