"""
@author: shreya

"""

import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
from vega_datasets import data

@st.cache
def load_data():
    data = pd.read_csv("https://raw.githubusercontent.com/CMU-IDS-2022/final-project-thescientists/main/datasets/DataScientiestsSalaries2021.csv")
    return data

def load_ds_salary_data():
    #Removing index column:
    #ds_data = pd.read_csv("Final_Salary.csv", index_col=[0])
    ds_data = pd.read_csv("https://raw.githubusercontent.com/CMU-IDS-2022/final-project-thescientists/main/datasets/Final_Salary.csv", index_col=[0])
    return ds_data

def load_no_of_jobs_data():
    #jobs_data = pd.read_csv("Final_DS_Count.csv", index_col=[0])
    jobs_data = pd.read_csv("https://raw.githubusercontent.com/CMU-IDS-2022/final-project-thescientists/main/datasets/Final_DS_Count.csv", index_col=[0])
    return jobs_data

#THIS IS THE FINAL PYTHON:

add_selectbox = st.sidebar.selectbox("Select a view to explore:",
    ('US Data Science Jobs visualizations',
     'Industry and Company visualizations',
     'Job Recommendation Dashboard'))

if add_selectbox == 'US Data Science Jobs visualizations':
    ####################################################################################################################
    st.title('United States')
    st.write('The below charts are specifically created for Data Science Roles')
    
    st.title('Min Max Avg Salaries (State Wise)')
    st.write('Below visualization shows the minimum, maximum and average salaries for various states in the United States.')
    #Min max avg salary:
    with st.spinner(text="Loading data..."):        
        onlyDS = load_ds_salary_data()
    
        st.header("Sample Dataset")
        st.write("Click on the checkbox to see the data for min max avg salary")
        if st.checkbox('Show Min Max Avg Data'):
            selected_rows = onlyDS[~onlyDS.isnull()]
            st.dataframe(selected_rows.head(5))
    
        #Code starts from here for the interactive graphs
        st.header("Interactive Graphs")
        
        if st.checkbox('Show the graph for Salaries'):
            onlyDS_data = load_ds_salary_data()[['Maximum Salary','Job Location','usa_state_latitude','usa_state_longitude','Job Title','Minimum Salary','Average Salary','State','id','STATE_NAME']]
    
            salary = ['Maximum Salary']
            
            salary_radio = st.radio(
             "Salary Options: ",
             ('Maximum Salary', 'Minimum Salary', 'Average Salary'))
        
            states = alt.topo_feature(data.us_10m.url, feature='states')
        
            state_map = alt.topo_feature(data.us_10m.url, 'states')
            
            map_click = alt.selection_multi(fields=['State'])
            bar_click = alt.selection_multi(fields=['State'], on='mouseover', nearest=True)
        
            b = alt.Chart(state_map).mark_geoshape().properties(title='Minimum Maximum Average Salaries')
            
            
            background = alt.Chart(state_map).mark_geoshape(
                            fill='grey',
                            stroke='black',
                            strokeWidth=2,
                            color='id:Q'
                        ).project('albersUsa').properties(
                            width=1000,
                            height=600
                        ).properties(title='Minimum Maximum Average Salaries')
                            
            # max_salary = alt.Chart(onlyDS).mark_circle(size=35).encode(
            #                 longitude='usa_state_longitude:Q',
            #                 latitude='usa_state_latitude:Q',
            #                 #size=alt.value(20),
            #                 color='Maximum Salary:Q',
            #                 size=alt.Size('Maximum Salary', scale=alt.Scale(range=[100, 500])),
            #                 tooltip=[
            #                 'Job Location', 'Job Title',
            #                 alt.Tooltip('max(Maximum Salary)', title='Maximum Salary(K)'),
            #             ]
            #             )
            
            max_salary_coloured = alt.Chart(state_map).mark_geoshape(
                    ).transform_lookup(
                    lookup='id', 
                    from_=alt.LookupData(onlyDS_data, 'id', ['Maximum Salary', 'State', 'Job Location', 'Job Title'])
                    ).encode(color='Maximum Salary:Q',
                             tooltip=[
                            'Job Location:N', 'Job Title:N',
                            'Maximum Salary:Q']
                    ).project(type='albersUsa'
                    ).properties(
                            width=1000,
                            height=600)
        
            
            # min_salary = alt.Chart(onlyDS).mark_circle(size=35).encode(
            #                 longitude='usa_state_longitude:Q',
            #                 latitude='usa_state_latitude:Q',
            #                 color='Minimum Salary:Q',
            #                 size=alt.Size('Minimum Salary', scale=alt.Scale(range=[100, 500])),
            #                 tooltip=[
            #                 'Job Location', 'Job Title',
            #                 alt.Tooltip('min(Minimum Salary)', title='Minimum Salary(K)'),
            #             ]
            #             )
            min_salary_coloured = alt.Chart(state_map).mark_geoshape(
                    ).transform_lookup(
                    lookup='id', 
                    from_=alt.LookupData(onlyDS_data, 'id', ['Minimum Salary', 'State', 'Job Location', 'Job Title'])
                    ).encode(color='Minimum Salary:Q',
                             tooltip=[
                            'Job Location:N', 'Job Title:N',
                            'Minimum Salary:Q']
                    ).project(type='albersUsa'
                    ).properties(
                            width=1000,
                            height=600)
                        
                        
            # avg_salary = alt.Chart(onlyDS).mark_circle(size=35).encode(
            #                 longitude='usa_state_longitude:Q',
            #                 latitude='usa_state_latitude:Q',
            #                 color='Average Salary:Q',
            #                 size=alt.Size('Average Salary', scale=alt.Scale(range=[100, 500])),
            #                 tooltip=[
            #                 'Job Location', 'Job Title',
            #                 alt.Tooltip('max(Average Salary)', title='Average Salary(K)'),
            #             ]
            #             )
            avg_salary_coloured = alt.Chart(state_map).mark_geoshape(
                    ).transform_lookup(
                    lookup='id', 
                    from_=alt.LookupData(onlyDS_data, 'id', ['Average Salary', 'State', 'Job Location', 'Job Title'])
                    ).encode(color='Average Salary:Q',
                             tooltip=[
                            'Job Location:N', 'Job Title:N',
                            'Average Salary:Q']
                    ).project(type='albersUsa'
                    ).properties(
                            width=1000,
                            height=600)
            
            if salary_radio == 'Maximum Salary':
                st.altair_chart(b+max_salary_coloured)
                # st.altair_chart(background+max_salary)
                
            if salary_radio == 'Minimum Salary':
                st.altair_chart(b+min_salary_coloured)
                # st.altair_chart(background+min_salary)
                
            if salary_radio == 'Average Salary':
                st.altair_chart(b+avg_salary_coloured)
                # st.altair_chart(background+avg_salary)
                
        
#==============================================================================================================#

    st.title('Number of Data Science Roles')
    st.write('Below visualization shows the number of jobs available in various states in the United States. Users will have the ability to interact with the chart. They will be able to see a specific location and understand the job opportunities available.')
            
    #Number of Jobs in United States:
    with st.spinner(text="Loading data..."):   
        jobs = load_no_of_jobs_data()
        
    st.header("Sample Dataset")
    st.write("Click on the checkbox to see the data for DS roles")
    if st.checkbox('Show Data Science Roles Data'):
        selected_rows1 = jobs[~jobs.isnull()]
        st.dataframe(selected_rows1.head(5))
          
    st.header("Interactive Graph")
    if st.checkbox('Show the graph role count '):  
        st.write('The graph has been colored according to the Maximum Salary offered in various states. Feel free to choose the company name along with the job type to see various combinations of availability')
        
        job_type = list(jobs['Job_Type'].unique())
        job_type.insert(1, 'All')
        company_names = list(jobs['Company'].unique())
        company_names.insert(1, 'All')
                    
        input_dropdown_job = alt.binding_select(options=job_type, name='Job Type')
        job_type_selection = alt.selection_single(fields=['Job_Type'], bind=input_dropdown_job, name='Job Type')
        
        input_dropdown_company = alt.binding_select(options=company_names, name='Company Name')
        company_name_selection = alt.selection_single(fields=['Company'], bind=input_dropdown_company, name='Company Name')
    
        states = alt.topo_feature(data.us_10m.url, feature='states')
        
        background = alt.Chart(states).mark_geoshape(
                        fill='grey',
                        stroke='black',
                        strokeWidth=2,
                        color='Maximum Salary:Q'
                    ).project('albersUsa').properties(
                        width=1000,
                        height=600
                    ).properties(title='Number Of Jobs In Each State')
                        
        job_type_points = alt.Chart(jobs).mark_circle(color='white', size=10).encode(
                            longitude='lng:Q',
                            latitude='lat:Q',
                            #size=alt.value(15),
                            color='Max_Salary:Q',
                            size=alt.Size('Max_Salary', scale=alt.Scale(range=[100, 400])),
                            tooltip=[
                                alt.Tooltip('Job_title', title="Job Title"),
                                'Year', 'Job_Type', 'Company', 'Industry',
                                alt.Tooltip('count(Job_title)', title='Job Count'),
                                alt.Tooltip('max(Max_Salary)', title='Maximum Salary Offered By This Company'),
                                alt.Tooltip('max(Min_Salary)', title='Minimum Salary Offered By This Company'),
                            ]
                        ).add_selection(
                                    job_type_selection, company_name_selection
                                    ).transform_filter(
                                    job_type_selection & company_name_selection
                                    )

        
        st.altair_chart(background + job_type_points)
        
        
        ####################################################################################################################
    
elif add_selectbox == 'Industry and Company visualizations':
        ####################################################################################################################
        
    st.write('Industry/Company charts')
    
        ####################################################################################################################
    
elif add_selectbox == 'Job Recommendation Dashboard':
        ####################################################################################################################
        
    st.write('Job reco charts')
    
        ####################################################################################################################
    
