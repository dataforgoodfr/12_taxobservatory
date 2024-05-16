# Copyright 2021-2024 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from taipy.gui.extension import Element, ElementLibrary, ElementProperty, PropertyType

    # <|layout|columns=1 1|gap=4rem|clas_name=fr p4 align-columns-center|
    # <|part|
    # A title
    # a sub title
    # |>
    # <|part|
    # <|button|active|label=More key stories ->|>
    # |>
    # |>
    # <|{original_image}|image|>

class VizLibrary(ElementLibrary):
    def __init__(self) -> None:
        # Initialize the set of visual elements for this extension library
        self.elements = {
            "viz": Element(
                 "title",
                {
                    "title": ElementProperty(PropertyType.string),
                    "subtitle": ElementProperty(PropertyType.string),
                    "data": ElementProperty(PropertyType.data),
                },
                render_xhtml=VizLibrary._viz_render,
            ),
            # A static element that displays its properties in a fraction
            "fraction": Element(
                "numerator",
                {
                    "numerator": ElementProperty(PropertyType.number),
                    "denominator": ElementProperty(PropertyType.number),
                },
                render_xhtml=VizLibrary._fraction_render,
            ),
            # A dynamic element that decorates its value
            "label": Element(
                "value",
                {"value": ElementProperty(PropertyType.dynamic_string)},
                # The name of the React component (ColoredLabel) that implements this custom
                # element, exported as ExampleLabel in front-end/src/index.ts
                react_component="ExampleLabel",
            ),
        }

    # The implementation of the rendering for the "fraction" static element
    @staticmethod
    def _fraction_render(props: dict) -> str:
        # Get the property values
        numerator = props.get("numerator")
        denominator = props.get("denominator")
        # No denominator or numerator is 0: display the numerator
        if denominator is None or int(numerator) == 0:  # type: ignore[arg-type]
            return f"<span>{numerator}</span>"
        # Denominator is zero: display infinity
        if int(denominator) == 0:
            return '<span style=    "font-size: 1.6em">&#8734;</span>'
        # 'Normal' case
        return f"<span><sup>{numerator}</sup>/<sub>{denominator}</sub></span>"

    # The implementation of the rendering for the "fraction" static element
    @staticmethod
    def _viz_render(props: dict) -> str:
        # Get the property values
        title = props.get("title")
        subtitle = props.get("subtitle")
        data = props.get("data")

        return f'''
        <div class="viz">
             <div class="container">               
                 <div class="parent">
                   <div class="child">
                     {title}                     
                   </div>
                   <span/>
                   <div class="child">
                      <img src="images/Vector.svg" alt="download"/>                      
                   </div>
                 </div>
                 <p>{subtitle}</p>                 
                           
            </div>
        </div>
        '''
    # <taipy:chart mode="lines" type="bar" x="year" y[1]="mnc" line[1]="dash">{data}</taipy:chart>
    def get_name(self) -> str:
        return "viz"

    def get_elements(self) -> dict:
        return self.elements

    # def get_scripts(self) -> list[str]:
    #     # Only one JavaScript bundle for this library.
    #     return ["front-end/dist/exampleLibrary.js"]

# (<|viz.viz|title=My Title|subtitle=My_subtitle|>)
# <|{None}|file_download|on_action={viz1.on_action}|>