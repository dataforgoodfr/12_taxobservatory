# data source https://drive.google.com/drive/folders/1E7ejgm7rYLMx3IwhUCrHJuf6EseDJgl0
# https://www.figma.com/proto/S5mYPmPeLSvPp4AoS5hf8x/Observatoire-de-la-fiscalit%C3%A9?page-id=0%3A1&type=design&node-id=59-93&viewport=701%2C312%2C0.37&t=EDuRKVhhwQ2t8n8F-1&scaling=scale-down

from taipy.gui import Gui
import taipy as tp

from pages.viz.viz import viz_md
from pages.home.home import home_md
from pages.country.country import country_md
from pages.company.company import company_md
from pages.keystories.keystories import keystories_md

# from pages.world.world import world_md
# from pages.map.map import map_md
# from pages.predictions.predictions import predictions_md, selected_scenario


from pages.root import root

from pages.country.country import selected_country, selector_country
from pages.company.company import selected_company, selector_company
# from pages.key_stories.key_stories 

from config.config import Config

pages = {
    '/': root,
    'Viz':viz_md,
    'Home': home_md,
    'KeyStories': keystories_md,
    'Company': company_md,
    'Country': country_md,
}


my_theme = {
#   "card": {
#     "background-color": "#333333"
#   },  
#   "palette": {
#     "background": {"default": "#808080"},
#     "primary": {"main": "#a25221"}
#   }
}

gui_multi_pages = Gui(pages=pages, css_file="css/style.css")

if __name__ == '__main__':
    print ('data4good')
    tp.Core().run()

    # gui_multi_pages.run(
    #     title="My first Dashboard", 
    #     # theme=my_theme
        
    #     )
    gui_multi_pages.run(title="data4good")