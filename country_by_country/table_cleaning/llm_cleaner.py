# MIT License
#
# Copyright (c) 2024 dataforgood
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Standard imports
import logging

import pandas as pd

# External imports
from dotenv import load_dotenv
from IPython.display import display
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from country_by_country.utils import constants


class LLMCleaner:
    def __init__(self, **kwargs: dict) -> None:
        """
        Builds a table cleaner, by extracting clean data from tables
        extracted during table extraction stage.
        The kwargs given to the constructor are directly propagated
        to the LLMCleaner constructor.
        You are free to define any parameter LLMCleaner recognizes.
        """
        self.kwargs = kwargs

        # Load OPENAI and LANGCHAIN API keys from .env file
        load_dotenv()

    def __call__(self, assets: dict) -> None:
        logging.info("Kicking off cleaning stage...")

        # TODO: CURRENTLY ONLY WORKS IF UNSTRUCTURED WAS USED IN PREVIOUS STAGE
        # Extract tables from previous stage
        tables = assets["img_table_extractors"]["unstructured"]["tables"]

        logging.info(f"Pulling {len(tables)} tables from extraction stage")

        # Convert tables to html to add to LLM prompt
        html_tables = [table.to_html() for table in tables]

        # Define our LLM model
        model = ChatOpenAI(temperature=0, model="gpt-4-turbo-preview")

        # ---------- CHAIN 1/2 - Pull countries from each table ----------
        logging.info("Starting chain 1/2: extracting country names from tables")

        # Output should have this model (a list of country names)
        class CountryNames(BaseModel):
            country_names: list[str] = Field(
                description="Exhaustive list of countries with financial data in the table",
                enum=constants.COUNTRIES,
            )

        # Output should be a JSON with above schema
        parser1 = JsonOutputParser(pydantic_object=CountryNames)

        # Prompt includes one extracted table and some JSON output formatting instructions
        prompt1 = PromptTemplate(
            template="Extract an exhaustive list of countries from the following table "
            + "in html format:\n{table}\n{format_instructions}",
            input_variables=["table"],
            partial_variables={
                "format_instructions": parser1.get_format_instructions(),
            },
        )

        # Chain
        chain1 = {"table": lambda x: x} | prompt1 | model | parser1

        # Run it
        responses1 = chain1.batch(html_tables, {"max_concurrency": 4})

        # Extract country lists from responses
        country_lists = [resp["country_names"] for resp in responses1]

        # ---------- CHAIN 2/2 - Pull financial data for each country ----------
        logging.info("Starting chain 2/2: extracting financial data from tables")

        # Define country data model
        class Country(BaseModel):
            """Financial data about a country"""

            jur_name: str = Field(..., description="Name of the country")
            total_revenues: float | None = Field(None, description="Total revenues")
            profit_before_tax: float | None = Field(
                None,
                description="Amount of profit (or loss) before tax",
            )
            tax_paid: float | None = Field(None, description="Income tax paid")
            tax_accrued: float | None = Field(None, description="Accrued tax")
            employees: float | None = Field(None, description="Number of employees")
            stated_capital: float | None = Field(None, description="Stated capital")
            accumulated_earnings: float | None = Field(
                None,
                description="Accumulated earnings",
            )
            tangible_assets: float | None = Field(
                None,
                description="Tangible assets other than cash and cash equivalent",
            )

        # Output should have this model (a list of country objects)
        class Countries(BaseModel):
            """Extracting financial data for each country"""

            countries: list[Country]

        # Output should be a JSON with above schema
        parser2 = PydanticOutputParser(pydantic_object=Countries)

        # Prompt includes one extracted table and some JSON output formatting instructions
        template = (
            """You are an assistant tasked with extracting financial """
            + """data about {country_list} from the following table in html format:\n
        {table}\n
        {format_instructions}
        """
        )

        # Set up prompt
        prompt = PromptTemplate.from_template(
            template,
            partial_variables={
                "format_instructions": parser2.get_format_instructions(),
            },
        )

        # Chain
        chain2 = (
            {"table": lambda x: x[0], "country_list": lambda x: x[1]}
            | prompt
            | model.with_structured_output(Countries)
        )

        # Run it
        responses2 = chain2.batch(
            list(zip(html_tables, country_lists, strict=True)),
            {"max_concurrency": 4},
        )

        # Merge the tables into one dataframe
        df = pd.concat(
            [pd.json_normalize(resp.dict()["countries"]) for resp in responses2],
        ).reset_index(drop=True)

        # Save the dataframe
        assets["table_cleaners"]["LLM"] = {
            "table": df,
        }

        # Display
        display(df)
