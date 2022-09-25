import streamlit as st
import pandas as pd
import os

from utils.login import *
from utils.utils import *

from views.overview import *

st.set_page_config(layout='wide', page_title='Explore Strava')

st.title("Welcome to your own personal strava explorer")
st.sidebar.subheader("Modules")

view = st.sidebar.radio('Select view', ['Login','Home'], key='view')

if st.session_state.view == "Login":
    login()

if st.session_state.view == "Home":
    overview()







