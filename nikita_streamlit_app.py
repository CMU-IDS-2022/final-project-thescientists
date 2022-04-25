'''
@author: Nikita Jyoti
'''
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
from vega_datasets import data


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

    def load_data(fname):
        """
        Write 1-2 lines of code here to load the data from CSV to a pandas dataframe
        and return it.
        :param fname:
        """
        df = pd.read_csv(fname)
        return df
        # pass


    # MAIN CODE
    #
    st.title("Data Analyst")

    with st.spinner(text="Loading data..."):
        df = load_data("https://raw.githubusercontent.com/CMU-IDS-2022/final-project-thescientists/main/datasets/Final_Data_Analyst2.csv")

    # Creating checkbox for showing the table. Sample Dataset:
    st.header("Data Analyst Jobs in the US")

    industry_list = list(df['Industry'].unique()) + [None]
    input_dropdown = alt.binding_select(options=industry_list)
    selection = alt.selection_single(fields=['Industry'], bind=input_dropdown, name='New')

    st.header("Where are the headquarters?")
    st.write(
        "The headquarters of companies offering data roles in USA are given below. Hover over a location (circle) on the map to view more details.")

    # CHART 1 - USA Map -
    states1 = alt.topo_feature(data.us_10m.url, feature='states')

    background = alt.Chart(states1).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project('albersUsa').properties(
        width=500,
        height=300
    )

    # Headquarters
    hq_list = list(df['Job Location']) + [None]

    points = alt.Chart(df).mark_point().encode(
        longitude='lng:Q',
        latitude='lat:Q',
        size=alt.value(10),
        tooltip=['Company Name', 'Headquarters', 'Industry', 'Type of ownership']
    )

    background + points

    # CHART 2 - grouped salaries, industry wise
    with st.spinner(text="Loading data..."):
        df2 = load_data("https://github.com/CMU-IDS-2022/final-project-thescientists/blob/main/datasets/DataScientiestsSalaries2021Cleaned.csv")
    st.header("Data Roles Salaries in the US")

    # REFERENCE - https://stackoverflow.com/questions/62315591/altair-select-all-values-when-using-binding-select
    industry_list = list(df2['Sector'].unique()) + [None]
    input_dropdown = alt.binding_select(options=industry_list)
    selection = alt.selection_single(fields=['Sector'], bind=input_dropdown, name='New')

    industry_brush = alt.selection_multi(fields=['Sector'])

    # Creating a selection box:
    industry_selectbox = st.selectbox("Select the industry", df2['Sector'].unique())
    industry_df = df2[df2['Sector'] == industry_selectbox]

    # We want to firstly understand the distribution of salary across data roles within an industry
    st.write("Change the Industry to see the distribution of salary across data roles within it.")
    salary_distribution = alt.Chart(industry_df).transform_filter(industry_brush).mark_bar().encode(
        x='job_title_sim:N',
        y='average(Avg Salary(K)):Q',
        color='job_title_sim:N',
        column='Sector:N',
        tooltip=[alt.Tooltip('job_title_sim', title="Job Role"), alt.Tooltip('Avg Salary(K)')]
    ).interactive().transform_window(
        rank='rank(Avg Salary(K))'
    ).properties(
        height=300,
        width=300
    ).interactive().add_selection(industry_brush)

    st.altair_chart(salary_distribution)

    # CHART 3 - Bubbles with Salary
    st.write(
        "Now lets look at the companies in the selected industry along with the salary range they offer. Zoom in to see the whole thing!")

    salaryBubbles = alt.Chart(industry_df).transform_filter(industry_brush).mark_point(filled=True).encode(
        alt.X('Avg Salary(K):Q'),
        alt.Y('Company Name:N'),
        alt.Color("Avg Salary(K):Q"),
        size='Avg Salary(K):Q',
        tooltip=[alt.Tooltip('job_title_sim', title="Job Role"), alt.Tooltip('Avg Salary(K)'),
                 alt.Tooltip('Company Name'), alt.Tooltip('Location')]
    ).transform_window(
        rank="rank(Avg Salary(K):Q)",
        sort=[
            alt.SortField("Avg Salary(K):Q", order="descending"),
        ],
    ).transform_filter(
        'datum.rank < 30'
    ).interactive().add_selection(industry_brush)

    if st.checkbox('Show Average Salaries for Companies in This Industry'):
        st.altair_chart(salaryBubbles, use_container_width=True)

    companyRating = alt.Chart(industry_df).transform_filter(industry_brush).mark_circle(filled=True, size=200,
                                                                                        opacity=1).encode(
        alt.X('Rating:Q', scale=alt.Scale(zero=False)),
        alt.Y('Company Name:N'),
        alt.Color("Rating Score:N", scale=alt.Scale(domain=["good", "ok", "bad"], range=["green", "yellow", "red"])),
        tooltip=['Company Name', 'Rating', 'Avg Salary(K)']
    ).properties(
        width=170
    ).interactive().add_selection(industry_brush)

    if st.checkbox('Show Employee Ratings for Companies in This Industry'):
        st.altair_chart(companyRating, use_container_width=True)

    salaryBubblesCopy = alt.Chart(industry_df).transform_filter(industry_brush).mark_point(filled=True,
                                                                                           size=200).encode(
        alt.X('Avg Salary(K):Q', scale=alt.Scale(zero=False)),
        alt.Y('Company Name:N'),
        alt.Color("Avg Salary(K):Q", legend=None),
        tooltip=['Avg Salary(K)', 'Company Name', 'Location']
    ).properties(
        width=170
    ).transform_window(
        rank='rank(Avg Salary(K))'
    ).add_selection(industry_brush)

    if st.checkbox('Show Employee Ratings for Selected Salaries'):
        st.write(
            'Drag the cursor to select a rectangular area containing companies in the first chart. The second chart will change to display the employee ratings for the selected companies.')
        selection = alt.selection_interval()
        salaryBubblesCopy.add_selection(selection).encode(
            color=alt.condition(selection, "Avg Salary(K)", alt.value("grey"))
        ) | companyRating.transform_filter(selection)

    st.write('Industry/Company charts')

    ####################################################################################################################

elif add_selectbox == 'Job Recommendation Dashboard':
    ####################################################################################################################

    st.write('Job reco charts')

    ####################################################################################################################
