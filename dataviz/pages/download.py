from datetime import datetime

import pandas as pd
import streamlit as st
import altair as alt
from numpy.lib.function_base import select
from streamlit.logger import get_logger

import numpy as np
import plotly.express as px
import plotly.graph_objects as go




def show_downlaod_data():

    text = '''
    # Download data   
    objective : provide access to the raw data
    SELECT BOX “FISCAL YEAR” / “HQ COUNTRY” / “SECTOR” / “COMPANY”  
    
    Reports list and quality indicators  (show snapshot)  
    CbCRs intra-reports data  (show snapshot)  
    Tax havens list (show snapshot)  
    OECD tables used  
    xx  (show snapshot)  
    xxx (show snapshot)  

    '''
    st.markdown(text)