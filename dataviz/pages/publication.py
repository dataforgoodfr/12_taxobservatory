from datetime import datetime

import pandas as pd
import streamlit as st
import altair as alt
from numpy.lib.function_base import select
from streamlit.logger import get_logger

import numpy as np
import plotly.express as px
import plotly.graph_objects as go




def show_publication():

    text = '''
    # Publication trends explorer  (1 page)   
    **objectives : analyze quantitative and qualitative trends in CBCRs publication**  
    
    - Evolution of reports over time  
        - number of reports over time  
        - number of MNEs with at least one report over time  
        - comparison with total MNE that will be subject to the directive   
        quality of the reports (multiple ways to assess : % with all OECD var, % with all GRI var, % with country-level data, aggregated transparency score, or just boolean on whether specific var are disclosed)  
        - cloud of available companies (1+ report in database) with number of reports / avg transparency score displayed when hovering    
    - Contributing HQ countries  
        - breakdown of reports / MNEs with 1+ report by country  
        - possibility to filter 1.a/b/c/d viz on a country   
        - link to HQ country explorer  
    - Contributing sectors  
        - breakdown of reports / MNEs with 1+ report by country  
        - possibility to filter 1.a/b/c/d viz on a sector   
        - link to sector explorer  
    - Link to download data  
    - Links to other exploration tools  
        - companies  
        - countries  
        - sectors  
    
    '''
    st.markdown(text)