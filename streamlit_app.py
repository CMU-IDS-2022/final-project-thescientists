import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

@st.cache
def load_data():
    data = pd.read_csv("https://raw.githubusercontent.com/CMU-IDS-2022/final-project-thescientists/main/datasets/DataScientiestsSalaries2021.csv")
    return data


add_selectbox = st.sidebar.selectbox("Select a view to explore:",
    ('US Data Science Jobs visualizations',
     'Industry and Company visualizations',
     'Job Recommendation Dashboard'))

if add_selectbox == 'US Data Science Jobs visualizations':
    ####################################################################################################################

    st.write('US charts')

    ####################################################################################################################

elif add_selectbox == 'Industry and Company visualizations':
    ####################################################################################################################

    st.write('Industry/Company charts')

    ####################################################################################################################

elif add_selectbox == 'Job Recommendation Dashboard':
    ####################################################################################################################

    st.write('Job reco charts')

    ####################################################################################################################

