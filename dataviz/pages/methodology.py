from datetime import datetime

import pandas as pd
import streamlit as st
import altair as alt
from numpy.lib.function_base import select
from streamlit.logger import get_logger

import numpy as np
import plotly.express as px
import plotly.graph_objects as go




def show_methodology():

    text = '''
    # Methodology   
    objectives : provide transparency over how the tracker was built and choices we made  
    e.g., https://www.carbonbombs.org/methodology
    
    
    '''
    st.markdown(text)