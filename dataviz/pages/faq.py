from datetime import datetime

import pandas as pd
import streamlit as st
import altair as alt
from numpy.lib.function_base import select
from streamlit.logger import get_logger

import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def show_faq():
    text = '''
    # FAQ
    objective : anticipate questions the user may have when exploring the site (might refer to other pages like methodology)  
    Non-exhaustive list of questions we can cover :  
    Why is tax transparency so important ?  
    What’s a country-by-country report ?  
    What companies must publish their country-by-country report ?  
    How do companies can minimize their taxes ?  
    Tax evasion vs. tax optimization  
    How can we detect tax evasion practices ?  
    Which countries are considered tax havens and why ?  
    …   

    '''
    st.markdown(text)
