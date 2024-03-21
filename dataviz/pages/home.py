from datetime import datetime

import pandas as pd
import streamlit as st
import altair as alt
from numpy.lib.function_base import select
from streamlit.logger import get_logger

import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from streamlit_navigation_bar import st_navbar
import pages as pg

LOGGER = get_logger(__name__)

def show_home():

    text = '''
        # Home
        **objectives : introduce the tracker, its objective and added value + show snapshots of data to drive exploration** 
        
        - Presentation of the tracker   
            - Objective of the tracker: Collect, format, and make available 
              data from Country-by-Country Reports (CbCRs) disclosed by companies  
            - Why : facilitate access to CbCR data to all  
                - CbCRs data is instrumental for analyzing companies' tax
                 practices  
                - CbCRs data is public but not centralized/standardized, 
                hence difficult to access  
                - Difficulty to access will grow as way more reports are 
                expected  
        - Snapshot of the database  
            - Overview of available data  
                - Number of tracked reports  
                - Number of companies with at least one report  
                - Breakdown of the number of companies with at least 
                one report by hq country/sector  
                - Cloud of available companies with sector color  
            - Example of analysis it unlocks  
                - See where companies declare profits and how much tax 
                they pay : fake dataviz  
                - Detect suspicious behavior by looking at countries 
                with high profits but few employees / high profit per employee : fake data viz  
                - Analyze presence in countries considered tax havens : 
                fake data viz  
            - Database growth  
                - Number of reports actual growth : 
                Number of tracked reports over time  
                - Expected boom within the next 2 years upon the 
                implementation of the directive visualization: Number of 
                multinational corporations subject to the directive  
            - Disclaimer on the inconsistent comprehensiveness of reports 
            published  
                - % of reports with transparent data (pick 1 indicator among transparency indicators)  
        
        - Links to exploration tool  
            - publication trends  
            - companies  
            - countries  
            - sectors  
        - Link to download data  
        - Link to methodology  

    '''
    st.markdown(text)





        