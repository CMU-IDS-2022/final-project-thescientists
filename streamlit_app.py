from urllib.parse import urlencode

import altair as alt
import pandas as pd
import streamlit as st
import numpy as np
from annotated_text import annotated_text
from vega_datasets import data
import requests
import json
import re
import pdfplumber
import en_core_web_sm

st.set_page_config(layout="wide", page_title='Data Science Job Market Visualizer')

add_selectbox = st.sidebar.selectbox("Select a view to explore:",
                                     ('US Data Science Jobs visualizations',
                                      'Industry and Company visualizations',
                                      'Job Recommendation Dashboard'))

@st.cache
def load_data():
    data = pd.read_csv(
        "https://raw.githubusercontent.com/CMU-IDS-2022/final-project-thescientists/main/datasets/DataScientiestsSalaries2021.csv")
    return data

if add_selectbox == 'US Data Science Jobs visualizations':
    ####################################################################################################################


    def load_ds_salary_data():
        # Removing index column:
        # ds_data = pd.read_csv("Final_Salary.csv", index_col=[0])
        ds_data = pd.read_csv(
            "https://raw.githubusercontent.com/CMU-IDS-2022/final-project-thescientists/main/datasets/Final_Salary.csv",
            index_col=[0])
        return ds_data


    def load_no_of_jobs_data():
        # jobs_data = pd.read_csv("Final_DS_Count.csv", index_col=[0])
        jobs_data = pd.read_csv(
            "https://raw.githubusercontent.com/CMU-IDS-2022/final-project-thescientists/main/datasets/Final_DS_Count.csv",
            index_col=[0])
        return jobs_data


    st.title('Demand for Data Scientists across the United States')
    #st.write('The below charts are specifically created for Data Science Roles')

    st.markdown('## Number of Data Science Roles Available')
    st.write(
        'Below visualization shows the number of jobs available in various states in the United States. Users will have the ability to interact with the chart. They will be able to see a specific location and understand the job opportunities available.')

    # Number of Jobs in United States:
    with st.spinner(text="Loading data..."):
        jobs = load_no_of_jobs_data()

    #st.header("Sample Dataset")
    #st.write("Click on the checkbox to see the data for DS roles")
    #if st.checkbox('Show Data Science Roles Data'):
        # selected_rows1 = jobs[~jobs.isnull()]
        # st.dataframe(selected_rows1.head(5))

    #st.header("Interactive Graph")
    #if st.checkbox('Show the graph role count '):
        st.write(
            'The point has been colored according to the Maximum Salary offered in various states. Feel free to choose the company name along with the job type to see various combinations of availability. Choose both All in the dropdown to see all the points on the map.')

        job_type = list(jobs['Job_Type'].unique()) + [None]

        company_names = list(jobs['Company'].unique()) + [None]
        # company_names.insert(1, 'All')

        # input_dropdown_job = alt.binding_select(options=job_type, name='Job Type')
        input_dropdown_job = alt.binding_select(
            options=[None, 'FULL_TIME', 'PART_TIME', 'CONTRACTOR', 'INTERN', 'TEMPORARY'],
            labels=['All', 'FULL_TIME', 'PART_TIME', 'CONTRACTOR', 'INTERN', 'TEMPORARY'])
        job_type_selection = alt.selection_single(fields=['Job_Type'], bind=input_dropdown_job, name='Job Type')

        companies = [None, "ManTech", "GEICO", "Tecolote Research", "Systems &amp;amp; Technology Research",
                     "Booz Allen Hamilton Inc.", "Novetta", "The Knot Worldwide", "Amazon", "Seen by Indeed", "MITRE",
                     "Mathematica Policy Research", "CyberCoders", "Elder Research", "Department of Energy", "LMI",
                     "Expression Networks", "U.S. General Services Administration", "West 4th Strategy",
                     "IT Resonance Inc", "Artlin Consulting", "Applied Research Associates, Inc.", "CIA", "Fannie Mae",
                     "Analytica", "Piper Enterprise Solutions", "Meridian Knowledge Solutions", "Storyblocks",
                     "The Ashlar Group", "Koch Industries", "Aptive", "Pandera Systems", "Thresher",
                     "Na Ali&amp;#039;i", "Navigant Consulting", "DCS CORPORATION", "University of Maryland",
                     "Pragmatics", "Thomson Reuters Corporation", "World Bank", "Culmen International, LLC", "HRUCKUS",
                     "The Rock Creek Group", "Ollie&amp;#039;s Bargain Outlet", "Ridgeline International", "Cognosante",
                     "Resolvit.com", "1901 Group", "Job Juncture", "Royce Geospatial", "Pivotal Software",
                     "Sprezzatura Management Consulting", "B4Corp", "Knowesis Inc.", "I-Link Solutions",
                     "General Services Admin", "Akima Management Services", "Northrop Grumman", "ALQIMI",
                     "Sierra Nevada Corporation", "Tetra Tech", "Information Gateways", "SAIC",
                     "Office of Inspector General", "TransVoyant", "Hire Velocity", "Carolina Power &amp;amp; Light Co",
                     "Research Innovations", "Tek Leaders", "Valiant Integrated Services", "RTI Consulting", "BlueLabs",
                     "AnaVation LLC", "Latitude, Inc.", "Noblis", "Reveal Global Consulting LLC", "Berico Technologies",
                     "The Aerospace Corporation", "Varen Technologies", "Infinitive Inc", "Axiologic Solutions",
                     "Visionist, Inc.", "Pyramid Systems, Inc.", "Strategic Alliance Consulting, Inc", "1884794",
                     "Lucidus Solutions, LLC", "BlackFern Recruitment", "Leidos", "NT Concepts", "Lockheed Martin",
                     "BCT LLC", "Ops Tech Alliance", "Electronic Consulting Services, Inc.",
                     "Omni Consulting Solutions", "Dezign Concepts LLC", "General Dynamics Information Technology",
                     "ISYS Technologies, Inc.", "Praxis Engineering", "Serry Systems", "Peraton", "Nolij Consulting",
                     "Guidehouse", "Solekai Systems Corp", "Par Government Systems Corporation", "Facebook",
                     "METIS Solutions", "Accenture", "Atlas Research", "Teaching Strategies, LLC", "Ledger Investing",
                     "West Creek Financial", "Tiger Analytics", "NCQA", "Ball Corporation", "Kelly", "CGI", "IEM, Inc",
                     "Discovery Communications, Inc.", "Ball Metal Food Container Corp", "Oracle",
                     "Optimal Solutions Group", "Metaphase Consulting", "IT Resonance Inc.", "nDemand Consulting LLC",
                     "IBM Corporation", "Fors Marsh Group", "Deloitte", "New Light Technologies, Inc.",
                     "The Interface Financial Group", "Ball Corporation / Ball Aerospace",
                     "OnwardPath Technology Solutions LLC", "Premise", "Institute for Justice",
                     "US Department of Treasury", "NVIDIA", "Credence Management Solutions, LLC", "KaiHonua",
                     "CareJourney", "Veracity Engineering", "XOR Security", "Excel Global Solutions", "Resolvit",
                     "Raytheon Intelligence &amp;amp; Space", "Treasury, Departmental Offices", "CICONIX, LLC",
                     "CGI Technologies and Solutions, Inc.", "Cherokee Nation Businesses, LLC", "HUBZone HQ",
                     "Celestar Corporation", "CMCI", "Royce Geospatial Consultants Inc", "Øptimus Consulting",
                     "Metronome, LLC", "SESC", "Computercraft", "Aireon", "Param Solutions", "NIH",
                     "Microsoft Corporation", "CAMRIS International", "NCI Information Systems, Inc.",
                     "22nd Century Technologies", "Discovery Communications", "Huntington Ingalls Industries",
                     "RTI Consulting, LLC", "Mission Intel", "CEDENT", "Cedent Consulting", "Leidos Holdings Inc.",
                     "Lidl", "KPMG", "Systems Planning and Analysis, Inc.", "General Dynamics", "IntegrateIT",
                     "Salient CRGT", "Synertex LLC", "DirectViz, LLC", "NCI Information Systems Inc.",
                     "DirectViz Solutions, LLC", "Jacobs", "Whiteboard Federal",
                     "The Air-Conditioning, Heating, and Refrigeration Institute (AHRI)", "VISUAL SOFT, INC",
                     "Parsons Commercial Technology Group Inc.", "Johns Hopkins University Applied Physics Laboratory",
                     "Geodata IT, LLC", "Parsons Corporation", "DeNOVO Solutions", "Synertex",
                     "S2 Analytical Solutions LLC", "BAE Systems USA", "TENICA and Associates LLC", "HopHR", "IBM",
                     "Blue Compass, LLC", "Trusted Knowledge Options Inc.",
                     "All Native Group The Federal Services Division of Ho-Chunk Inc", "ALL NATIVE GROUP", "Boeing",
                     "Management Decisions, Inc.", "CACI International", "Bluemont Technology &amp;amp; Research, Inc.",
                     "Perspecta", "Nyla Technology Solutions", "Booz Allen Hamilton", "Brinks Home Security",
                     "Health IQ", "Zynga", "Evernote", "Lightspeed Systems", "Bakery Agency",
                     "Oscar Associates Americas LLC", "ThoughtFocus", "Home Depot", "Apple", "Keylent", "Schlumberger",
                     "Robert Half", "Aramco Services Company", "iHeartMedia", "Cytracom",
                     "Alaka`ina Foundation Family of Companies", "Inabia Software &amp;amp; consulting Inc.",
                     "Onica Group", "CGG Veritas", "Next Level Business Services, Inc.", "Dun &amp;amp; Bradstreet",
                     "JPMorgan Chase", "Southwest Business Corporation", "Randstad", "Abbott Laboratories",
                     "Alakaina Family of Companies", "Cloudflare, Inc.", "Horne LLP", "Focus America inc",
                     "Inherent Technologies", "Jabil", "Abbott", "Itbrainiac", "IMG Systems", "Cottonwood Financial",
                     "CGG", "Lorhan", "RMS Computer", "Ke`aki Technologies, LLC", "Sercel", "Cenergy International",
                     "APN Software Services Inc.", "Siri InfoSolutions Inc", "Trinity Industries", "NTT DATA Services",
                     "Geval6 Inc", "Applied Research Laboratories", "Signature Science, LLC", "Energy Cognito",
                     "Levelset", "PriceSenz", "Kairos Technologies", "Frontier Communications", "Vinli",
                     "Whole Foods Market", "Sense Corp", "Onica, a Rackspace Company", "Infosys", "LivaNova", "Humana",
                     "Walmart", "Veear Projects", "Givelify", "ka-hoot", "SEVEN Networks", "Wise Men Consultants",
                     "Rackspace", "Zdaly", "University of Texas Medical Branch", "Parkland Health and Hospital System",
                     "Kinder Morgan", "Cloudflare", "BlockTrace, LLC", "IT First Source", "Cyber Warrior Network",
                     "USAA", "Enbridge", "Alliance Data", "Ava Consulting", "Spectral MD, Inc.", "Neiman Marcus",
                     "AmerisourceBergen", "US Army Network Enterprise Technology Command", "VIVA USA", "Faire",
                     "GovTech", "Triplebyte", "Notion Labs", "Autodesk", "Formation", "Duetto", "Demandbase",
                     "Balyasny Asset Management", "Centraprise", "Upstart", "Nuna", "Strivr", "Aktana", "Unlearn.AI",
                     "Turn/River Capital", "University of California San Francisco", "Descript", "Medidata Solutions",
                     "Divvy Homes", "Ready Responders", "MasterClass", "SoftBank Robotics", "Lilt", "RiskIQ",
                     "Cogitativo", "Brightidea", "Trace Data", "Observable", "Eaze", "Mindstrong", "Mackin", "Appen",
                     "Roblox", "Geli", "Genentech", "Sartorius", "Aclima", "Mentor Graphics", "TECHNOCRAFT Solutions",
                     "PG&amp;amp;E Corporation", "TRM Labs", "Navio", "Entefy", "Canopy Health", "Goodwater Capital",
                     "The Judge Group, Inc.", "Snowflake", "Quantifind", "Landing AI", "Getty Images", "TCG", "Twitter",
                     "The Climate Corporation", "Jobot", "Stitch Fix", "Philo", "PG&amp;amp;E",
                     "Sunvalleytek International Inc.", "Allstate", "ClassDojo", "Chime", "Atlassian",
                     "Motif Investing", "Aetna", "PsiNapse Technology, Ltd.", "Landing", "Tesla Motors",
                     "EDI Specialists, Inc.", "DocuSign", "Thunder", "Tempus Labs", "Vhire", "Slack",
                     "Swinerton Builders", "Sensor Tower", "Center for Sustainable", "Twist Bioscience", "Meraki",
                     "Moloco, Inc.", "Noblr", "Tencent", "Windfall Data", "Denali Therapeutics",
                     "Two95 International Inc.", "Lawrence Berkeley Lab", "Aisera", "DoorDash", "One Concern",
                     "FortressIQ", "VDart, Inc.", "AutoGrid", "insitro", "OneinaMil", "Tesla", "PAVIR",
                     "The Play Station", "Ayata", "Lattice Engines", "GRAIL", "CitiusTech",
                     "Leibniz Center for Psychological", "Vitria Technology", "Rad AI", "The Clorox Company",
                     "QUICKEN INVESTMENT SERVICES, INC.", "Lam Research", "Project Ronin", "Eluvio",
                     "Non Specific Employer", "Electronic Arts", "V3 Talent Partners Inc.", "Crystal Dynamics",
                     "Siemens Healthineers"]
        use_labels = ["All", "ManTech", "GEICO", "Tecolote Research", "Systems &amp;amp; Technology Research",
                      "Booz Allen Hamilton Inc.", "Novetta", "The Knot Worldwide", "Amazon", "Seen by Indeed", "MITRE",
                      "Mathematica Policy Research", "CyberCoders", "Elder Research", "Department of Energy", "LMI",
                      "Expression Networks", "U.S. General Services Administration", "West 4th Strategy",
                      "IT Resonance Inc", "Artlin Consulting", "Applied Research Associates, Inc.", "CIA", "Fannie Mae",
                      "Analytica", "Piper Enterprise Solutions", "Meridian Knowledge Solutions", "Storyblocks",
                      "The Ashlar Group", "Koch Industries", "Aptive", "Pandera Systems", "Thresher",
                      "Na Ali&amp;#039;i", "Navigant Consulting", "DCS CORPORATION", "University of Maryland",
                      "Pragmatics", "Thomson Reuters Corporation", "World Bank", "Culmen International, LLC", "HRUCKUS",
                      "The Rock Creek Group", "Ollie&amp;#039;s Bargain Outlet", "Ridgeline International",
                      "Cognosante", "Resolvit.com", "1901 Group", "Job Juncture", "Royce Geospatial",
                      "Pivotal Software", "Sprezzatura Management Consulting", "B4Corp", "Knowesis Inc.",
                      "I-Link Solutions", "General Services Admin", "Akima Management Services", "Northrop Grumman",
                      "ALQIMI", "Sierra Nevada Corporation", "Tetra Tech", "Information Gateways", "SAIC",
                      "Office of Inspector General", "TransVoyant", "Hire Velocity",
                      "Carolina Power &amp;amp; Light Co", "Research Innovations", "Tek Leaders",
                      "Valiant Integrated Services", "RTI Consulting", "BlueLabs", "AnaVation LLC", "Latitude, Inc.",
                      "Noblis", "Reveal Global Consulting LLC", "Berico Technologies", "The Aerospace Corporation",
                      "Varen Technologies", "Infinitive Inc", "Axiologic Solutions", "Visionist, Inc.",
                      "Pyramid Systems, Inc.", "Strategic Alliance Consulting, Inc", "1884794",
                      "Lucidus Solutions, LLC", "BlackFern Recruitment", "Leidos", "NT Concepts", "Lockheed Martin",
                      "BCT LLC", "Ops Tech Alliance", "Electronic Consulting Services, Inc.",
                      "Omni Consulting Solutions", "Dezign Concepts LLC", "General Dynamics Information Technology",
                      "ISYS Technologies, Inc.", "Praxis Engineering", "Serry Systems", "Peraton", "Nolij Consulting",
                      "Guidehouse", "Solekai Systems Corp", "Par Government Systems Corporation", "Facebook",
                      "METIS Solutions", "Accenture", "Atlas Research", "Teaching Strategies, LLC", "Ledger Investing",
                      "West Creek Financial", "Tiger Analytics", "NCQA", "Ball Corporation", "Kelly", "CGI", "IEM, Inc",
                      "Discovery Communications, Inc.", "Ball Metal Food Container Corp", "Oracle",
                      "Optimal Solutions Group", "Metaphase Consulting", "IT Resonance Inc.", "nDemand Consulting LLC",
                      "IBM Corporation", "Fors Marsh Group", "Deloitte", "New Light Technologies, Inc.",
                      "The Interface Financial Group", "Ball Corporation / Ball Aerospace",
                      "OnwardPath Technology Solutions LLC", "Premise", "Institute for Justice",
                      "US Department of Treasury", "NVIDIA", "Credence Management Solutions, LLC", "KaiHonua",
                      "CareJourney", "Veracity Engineering", "XOR Security", "Excel Global Solutions", "Resolvit",
                      "Raytheon Intelligence &amp;amp; Space", "Treasury, Departmental Offices", "CICONIX, LLC",
                      "CGI Technologies and Solutions, Inc.", "Cherokee Nation Businesses, LLC", "HUBZone HQ",
                      "Celestar Corporation", "CMCI", "Royce Geospatial Consultants Inc", "Øptimus Consulting",
                      "Metronome, LLC", "SESC", "Computercraft", "Aireon", "Param Solutions", "NIH",
                      "Microsoft Corporation", "CAMRIS International", "NCI Information Systems, Inc.",
                      "22nd Century Technologies", "Discovery Communications", "Huntington Ingalls Industries",
                      "RTI Consulting, LLC", "Mission Intel", "CEDENT", "Cedent Consulting", "Leidos Holdings Inc.",
                      "Lidl", "KPMG", "Systems Planning and Analysis, Inc.", "General Dynamics", "IntegrateIT",
                      "Salient CRGT", "Synertex LLC", "DirectViz, LLC", "NCI Information Systems Inc.",
                      "DirectViz Solutions, LLC", "Jacobs", "Whiteboard Federal",
                      "The Air-Conditioning, Heating, and Refrigeration Institute (AHRI)", "VISUAL SOFT, INC",
                      "Parsons Commercial Technology Group Inc.", "Johns Hopkins University Applied Physics Laboratory",
                      "Geodata IT, LLC", "Parsons Corporation", "DeNOVO Solutions", "Synertex",
                      "S2 Analytical Solutions LLC", "BAE Systems USA", "TENICA and Associates LLC", "HopHR", "IBM",
                      "Blue Compass, LLC", "Trusted Knowledge Options Inc.",
                      "All Native Group The Federal Services Division of Ho-Chunk Inc", "ALL NATIVE GROUP", "Boeing",
                      "Management Decisions, Inc.", "CACI International",
                      "Bluemont Technology &amp;amp; Research, Inc.", "Perspecta", "Nyla Technology Solutions",
                      "Booz Allen Hamilton", "Brinks Home Security", "Health IQ", "Zynga", "Evernote",
                      "Lightspeed Systems", "Bakery Agency", "Oscar Associates Americas LLC", "ThoughtFocus",
                      "Home Depot", "Apple", "Keylent", "Schlumberger", "Robert Half", "Aramco Services Company",
                      "iHeartMedia", "Cytracom", "Alaka`ina Foundation Family of Companies",
                      "Inabia Software &amp;amp; consulting Inc.", "Onica Group", "CGG Veritas",
                      "Next Level Business Services, Inc.", "Dun &amp;amp; Bradstreet", "JPMorgan Chase",
                      "Southwest Business Corporation", "Randstad", "Abbott Laboratories",
                      "Alakaina Family of Companies", "Cloudflare, Inc.", "Horne LLP", "Focus America inc",
                      "Inherent Technologies", "Jabil", "Abbott", "Itbrainiac", "IMG Systems", "Cottonwood Financial",
                      "CGG", "Lorhan", "RMS Computer", "Ke`aki Technologies, LLC", "Sercel", "Cenergy International",
                      "APN Software Services Inc.", "Siri InfoSolutions Inc", "Trinity Industries", "NTT DATA Services",
                      "Geval6 Inc", "Applied Research Laboratories", "Signature Science, LLC", "Energy Cognito",
                      "Levelset", "PriceSenz", "Kairos Technologies", "Frontier Communications", "Vinli",
                      "Whole Foods Market", "Sense Corp", "Onica, a Rackspace Company", "Infosys", "LivaNova", "Humana",
                      "Walmart", "Veear Projects", "Givelify", "ka-hoot", "SEVEN Networks", "Wise Men Consultants",
                      "Rackspace", "Zdaly", "University of Texas Medical Branch", "Parkland Health and Hospital System",
                      "Kinder Morgan", "Cloudflare", "BlockTrace, LLC", "IT First Source", "Cyber Warrior Network",
                      "USAA", "Enbridge", "Alliance Data", "Ava Consulting", "Spectral MD, Inc.", "Neiman Marcus",
                      "AmerisourceBergen", "US Army Network Enterprise Technology Command", "VIVA USA", "Faire",
                      "GovTech", "Triplebyte", "Notion Labs", "Autodesk", "Formation", "Duetto", "Demandbase",
                      "Balyasny Asset Management", "Centraprise", "Upstart", "Nuna", "Strivr", "Aktana", "Unlearn.AI",
                      "Turn/River Capital", "University of California San Francisco", "Descript", "Medidata Solutions",
                      "Divvy Homes", "Ready Responders", "MasterClass", "SoftBank Robotics", "Lilt", "RiskIQ",
                      "Cogitativo", "Brightidea", "Trace Data", "Observable", "Eaze", "Mindstrong", "Mackin", "Appen",
                      "Roblox", "Geli", "Genentech", "Sartorius", "Aclima", "Mentor Graphics", "TECHNOCRAFT Solutions",
                      "PG&amp;amp;E Corporation", "TRM Labs", "Navio", "Entefy", "Canopy Health", "Goodwater Capital",
                      "The Judge Group, Inc.", "Snowflake", "Quantifind", "Landing AI", "Getty Images", "TCG",
                      "Twitter", "The Climate Corporation", "Jobot", "Stitch Fix", "Philo", "PG&amp;amp;E",
                      "Sunvalleytek International Inc.", "Allstate", "ClassDojo", "Chime", "Atlassian",
                      "Motif Investing", "Aetna", "PsiNapse Technology, Ltd.", "Landing", "Tesla Motors",
                      "EDI Specialists, Inc.", "DocuSign", "Thunder", "Tempus Labs", "Vhire", "Slack",
                      "Swinerton Builders", "Sensor Tower", "Center for Sustainable", "Twist Bioscience", "Meraki",
                      "Moloco, Inc.", "Noblr", "Tencent", "Windfall Data", "Denali Therapeutics",
                      "Two95 International Inc.", "Lawrence Berkeley Lab", "Aisera", "DoorDash", "One Concern",
                      "FortressIQ", "VDart, Inc.", "AutoGrid", "insitro", "OneinaMil", "Tesla", "PAVIR",
                      "The Play Station", "Ayata", "Lattice Engines", "GRAIL", "CitiusTech",
                      "Leibniz Center for Psychological", "Vitria Technology", "Rad AI", "The Clorox Company",
                      "QUICKEN INVESTMENT SERVICES, INC.", "Lam Research", "Project Ronin", "Eluvio",
                      "Non Specific Employer", "Electronic Arts", "V3 Talent Partners Inc.", "Crystal Dynamics",
                      "Siemens Healthineers"]

        input_dropdown_company = alt.binding_select(options=companies, labels=use_labels, name='Company Name')
        company_name_selection = alt.selection_single(fields=['Company'], bind=input_dropdown_company,
                                                      name='Company Name')

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
            # size=alt.value(15),
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

    st.markdown('## Data Scientist Salary Statistics Across the United States')
    st.write(
        'Below visualization shows the minimum, maximum and average salaries for various states in the United States.')
    # Min max avg salary:
    with st.spinner(text="Loading data..."):
        # onlyDS = load_ds_salary_data()
        #
        # st.header("Sample Dataset")
        # st.write("Click on the checkbox to see the data for min max avg salary")
        # # if st.checkbox('Show Min Max Avg Data'):
        # #     selected_rows = onlyDS[~onlyDS.isnull()]
        # #     st.dataframe(selected_rows.head(5))
        #
        # # Code starts from here for the interactive graphs
        # st.header("Interactive Graphs")

        # if st.checkbox('Show the graph for Salaries'):
        onlyDS_data = load_ds_salary_data()[
            ['Maximum Salary', 'Job Location', 'usa_state_latitude', 'usa_state_longitude', 'Job Title',
             'Minimum Salary', 'Average Salary', 'State', 'id', 'STATE_NAME']]

        salary = ['Maximum Salary']

        salary_radio = st.radio(
            "Salary Options: ",
            ('Maximum Salary', 'Minimum Salary', 'Average Salary'))

        states = alt.topo_feature(data.us_10m.url, feature='states')

        state_map = alt.topo_feature(data.us_10m.url, 'states')

        map_click = alt.selection_multi(fields=['State'])
        bar_click = alt.selection_multi(fields=['State'], on='mouseover', nearest=True)

        b = alt.Chart(state_map).mark_geoshape(fill='grey').properties(title='Minimum Maximum Average Salaries')

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
            st.altair_chart(b + max_salary_coloured)
            # st.altair_chart(background+max_salary)

        if salary_radio == 'Minimum Salary':
            st.altair_chart(b + min_salary_coloured)
            # st.altair_chart(background+min_salary)

        if salary_radio == 'Average Salary':
            st.altair_chart(b + avg_salary_coloured)
            # st.altair_chart(background+avg_salary)

    # ==============================================================================================================#


    def load_cost_of_living_data():
        df = pd.read_csv(
            "https://raw.githubusercontent.com/CMU-IDS-2022/final-project-thescientists/main/datasets/cost_of_living.csv")
        return df


    def filter_on_salary_slider(df, salary_range):

        labels = pd.Series([1] * len(df), index=df.index)
        if salary_range != None:
            labels &= df['normalized_salaries'] >= (salary_range[0])
            labels &= df['normalized_salaries'] <= (salary_range[1])

        return df[labels]


    cost_of_living_data = load_cost_of_living_data()
    state_map = alt.topo_feature(data.us_10m.url, 'states')

    st.markdown('## United States Salary Equalizer')

    st.write('“Cost of living” is the amount of money you need to sustain a certain lifestyle in a given place. '
             'Because the price of goods and services varies from one city to the next, '
             'calculating the cost of living will determine how affordable it is to live in a certain area.')

    st.write('With the below tool, we can analyze the pay magnitude for the same role across various States in the US.')


    cost_of_living_plot = alt.Chart(state_map).mark_geoshape(tooltip=True) \
        .transform_lookup(
        lookup='id',
        from_=alt.LookupData(cost_of_living_data, 'id', ['cost_of_living_index', 'State'])
    ).encode(
        color=alt.Color('cost_of_living_index:Q', sort="descending", scale=alt.Scale(scheme='plasma')),
        tooltip=['State:N', 'cost_of_living_index:Q']
    ).project(type='albersUsa').properties(width=1000,height=600, title='Cost of Living Index across US States')

    check_emp_norm_salary = st.checkbox('Check your Equivalent Salary in Different States', key="1")

    if check_emp_norm_salary:

        st.markdown("""---""")

        state_living_in = st.selectbox('Select your state of current employment:', cost_of_living_data.State)

        current_salary = st.text_input('Enter current Salary:', '$')
        current_salary = re.sub("[^0-9]", "", current_salary)
        if current_salary is not '':
            current_salary = float(current_salary)

            state_col_index = cost_of_living_data[cost_of_living_data['State'] == state_living_in].iloc[0, 2]

            cost_of_living_data['normalized_salaries'] = (cost_of_living_data[
                                                              'cost_of_living_index'] * current_salary) / state_col_index
            cost_of_living_data['normalized_salaries'] = cost_of_living_data['normalized_salaries'].round(decimals =2)


            min_sal = int(cost_of_living_data['normalized_salaries'].min())
            max_sal = int(cost_of_living_data['normalized_salaries'].max())

            col_salary_range = st.slider('Filter Normalized Salaries:',min_value=min_sal,max_value=max_sal,
                                                                  value=(min_sal,max_sal))



            filtered_col_dataset = filter_on_salary_slider(cost_of_living_data, col_salary_range)

            show_col_data = st.checkbox('Check your Equivalent Salary in Different States', key="2")
            if show_col_data:
                st.write(cost_of_living_data)

            cost_of_living_plot = alt.Chart(state_map).mark_geoshape(tooltip=True) \
                .transform_lookup(
                lookup='id',
                from_=alt.LookupData(filtered_col_dataset, 'id', ['normalized_salaries', 'State'])
            ).encode(
                color=alt.Color('normalized_salaries:Q', sort="descending", scale=alt.Scale(scheme='plasma')),
                tooltip = ['State:N', 'normalized_salaries:Q']
            ).project(type='albersUsa').properties(width=1000,height=600)

        st.markdown("""---""")


    #cost_of_living_data['normalized_salaries'].round(decimals=2)

    #st.write(cost_of_living_data)

    st.write(cost_of_living_plot)

    ####################################################################################################################

elif add_selectbox == 'Industry and Company visualizations':
    ####################################################################################################################

    def load_cleaned_data(fname):
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
    st.title("Industry and Company demand for Data Scientists")

    with st.spinner(text="Loading data..."):
        df = load_cleaned_data(
            "https://raw.githubusercontent.com/CMU-IDS-2022/final-project-thescientists/main/datasets/Final_Data_Analyst2.csv")

    # Creating checkbox for showing the table. Sample Dataset:
    # st.header("Data Analyst Jobs in the US")

    industry_list = list(df['Industry'].unique()) + [None]
    input_dropdown = alt.binding_select(options=industry_list)
    selection = alt.selection_single(fields=['Industry'], bind=input_dropdown, name='New')

    st.header("Headquarters of Companies hiring for Data Science Roles")
    st.write(
        "The headquarters of companies offering data roles in USA are given below. Hover over a location (circle) on the map to view more details.")

    # CHART 1 - USA Map -
    states1 = alt.topo_feature(data.us_10m.url, feature='states')

    background = alt.Chart(states1).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project('albersUsa').properties(
        width=1000,
        height=600
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

    st.markdown("""---""")

    # CHART 2 - grouped salaries, industry wise
    with st.spinner(text="Loading data..."):
        df2 = load_cleaned_data(
            "https://raw.githubusercontent.com/CMU-IDS-2022/final-project-thescientists/main/datasets/DataScientiestsSalaries2021Cleaned.csv")
    st.markdown("## Salaries for Data Roles by Industry")

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

    # Source: https://altair-viz.github.io/gallery/top_k_items.html
    salaryBubbles = alt.Chart(industry_df).transform_filter(industry_brush).mark_point(filled=True).encode(
        alt.X('Avg Salary(K):Q'),
        alt.Y('Company Name:N'),
        alt.Color("Avg Salary(K):Q"),
        size='Avg Salary(K):Q',
        tooltip=[alt.Tooltip('job_title_sim', title="Job Role"), alt.Tooltip('Avg Salary(K)'),
                 alt.Tooltip('Company Name'), alt.Tooltip('Location')]
    ).transform_window(
        rank="rank(Avg Salary(K))",
        sort=[
            alt.SortField("Avg Salary(K)", order="descending"),
        ]
    ).transform_filter(
        (alt.datum.rank <= 30)
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
    ).transform_window(
        rank="rank(Avg Salary(K))",
        sort=[
            alt.SortField("Avg Salary(K)", order="descending"),
        ]
    ).transform_filter(
        (alt.datum.rank <= 30)
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
        rank="rank(Avg Salary(K))",
        sort=[
            alt.SortField("Avg Salary(K)", order="descending"),
        ]
    ).transform_filter(
        (alt.datum.rank <= 30)
    ).add_selection(industry_brush)

    if st.checkbox('Show Employee Ratings for Selected Salaries'):
        st.write(
            'Drag the cursor to select a rectangular area containing companies in the first chart. The second chart will change to display the employee ratings for the selected companies.')
        selection = alt.selection_interval()
        salaryBubblesCopy.add_selection(selection).encode(
            color=alt.condition(selection, "Avg Salary(K)", alt.value("grey"))
        ) | companyRating.transform_filter(selection)

    data = load_data()

    # for i,v in (data.iteritems()):
    #     st.write(i,v.dtype)

    # st.write('Industry/Company charts')
    st.markdown("""---""")
    st.markdown("## Data Science Skills in Demand by Industries")
    industry = list(data.Industry.unique())
    industry_select = st.multiselect("", industry, ['Aerospace & Defense'])

    long_form = data.iloc[:, np.r_[0:3, 5, 11, 17:20, 23:39]]

    long_form = long_form.melt(id_vars=['index', 'Job Title', 'Salary Estimate', 'Company Name', 'Industry',
                                        'Avg Salary(K)', 'Lower Salary', 'Upper Salary'],
                               var_name='Skill', value_name='required')
    long_form.rename(columns={'index': 's_no'}, inplace=True)
    long_form['Skill'] = long_form['Skill'].str.upper()
    df_new_old = long_form.loc[long_form['Industry'].isin(industry_select)]

    df_new_1 = df_new_old[df_new_old.required == 1].iloc[:, :-1]

    l = list(df_new_old.groupby('s_no').filter(lambda x: x['required'].sum() == 0)['s_no'].unique())
    df_new_2 = df_new_old[df_new_old['s_no'].isin(l)].iloc[:, :-1].drop_duplicates('s_no')
    df_new_2.Skill = 'None'

    df_new = pd.concat([df_new_1, df_new_2])

    brush = alt.selection(type="multi", encodings=['y'])

    base = alt.Chart(df_new).transform_joinaggregate(
        Total='count(*)'
    ).transform_calculate(
        PercentOfTotal='1 / datum.Total'
    )

    skill_chart = base.mark_bar().encode(
        alt.X('sum(PercentOfTotal):Q', axis=alt.Axis(format='%', domain=False),
              title='% of job listings requiring the skill'),
        alt.Y("Skill:O", scale=alt.Scale(zero=False), sort='-x'),
        color=alt.condition(brush, alt.value('darkgreen'), alt.value('lightgreen')),
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.4)),
        tooltip=['Skill', 'count()', alt.Tooltip('sum(PercentOfTotal):Q', format='%')]
    )

    skill_text = skill_chart.mark_text(
        align='left',
        baseline='middle',
        dx=3
    ).encode(
        text='count():Q'
    )

    show_data = st.checkbox('Show raw data')
    if show_data:
        st.write(df_new)

    columns = ['Industry:N', 'count:Q', 'mean_sal:Q',
               'max_sal:Q', 'min_sal:Q']

    top_industries = alt.Chart(long_form[long_form.required == 1].iloc[:, :-1]).transform_filter(brush).encode(
        x=alt.X('Industry:N',
                sort=alt.SortField(field='mean_sal', order='descending'), axis=alt.Axis(labelAngle=-30))
    ).transform_aggregate(
        count='count()',
        mean_sal='mean(Avg Salary(K)):Q',
        max_sal='mean(Upper Salary):Q',
        min_sal='mean(Lower Salary):Q',
        groupby=['Industry']
    ).transform_window(
        window=[{'op': 'rank', 'as': 'rank'}],
        sort=[{'field': 'mean_sal', 'order': 'descending'}]
    ).transform_filter(('datum.rank <= 15'))

    selection = alt.selection_single(fields=['Industry'], nearest=True,
                                     on='mouseover', empty='none', clear='mouseout')

    top_industries_1 = top_industries.mark_rule(color='darkgrey').encode(
        opacity=alt.condition(selection, alt.value(0.6), alt.value(0)),
        tooltip=[alt.Tooltip(c) for c in columns]
    ).add_selection(selection)

    error_bar = top_industries.mark_errorbar(opacity=0.4, color='darkgreen').encode(
        alt.Y('max_sal:Q',
              axis=alt.Axis(title='Average Salary (in $1000)', domain=False,
                            tickSize=0, labelPadding=3, format='.0f'), scale=alt.Scale(zero=False)),
        alt.Y2('min_sal:Q'),
        strokeWidth=alt.value(2)
    )

    point_chart = top_industries.mark_point(filled=True, color='darkgreen').encode(
        alt.Y('mean_sal:Q'))

    points = point_chart.mark_point(color='darkgreen').transform_filter(selection)

    top_industries_text = point_chart.mark_text(
        fontSize=10,
        align='center',
        baseline='middle',
        dy=-10,
        dx=15
    ).encode(
        text=alt.Text('mean_sal1:N')
    ).transform_calculate(
        mean_sal1="round(datum.mean_sal) + 'K'"
    )

    eligible = base.mark_text(fontSize=35).encode(
        text=alt.Text('sum(PercentOfTotal):Q', format='.2%'),
        size=alt.Size(legend=None)
    ).transform_filter(brush).properties(
        title=alt.TitleParams(['% of jobs you', ' are eligible for:'], fontSize=20),

    )

    eligibility = base.mark_text(fontSize=35).encode(
        text='count():Q',
        size=alt.Size(legend=None)
    ).transform_filter(brush).properties(
        title=alt.TitleParams(['Number of jobs you', ' are eligible for:'], fontSize=20),

    )

    avg_salary = base.mark_text(fontSize=35).encode(
        text=alt.Text('avg_text:N')
    ).transform_filter(brush).transform_aggregate(
        groupby=["s_no"],
        avg_salary="mean(Avg Salary(K))"
    ).transform_aggregate(
        groupby=[],
        avg_salary1='mean(avg_salary)'
    ).transform_calculate(
        avg_text="round(datum.avg_salary1) + 'K'"
    ).properties(
        title=alt.TitleParams(['Average salary:'], fontSize=20),
        width=40,
        height=40
    )

    lower_salary = base.mark_text(fontSize=35).encode(
        text=alt.Text('low_text:N')
    ).transform_filter(brush).transform_aggregate(
        groupby=["s_no"],
        lower_salary="mean(Lower Salary)"
    ).transform_aggregate(
        groupby=[],
        low_salary='mean(lower_salary)'
    ).transform_calculate(
        low_text="round(datum.low_salary) + 'K'"
    ).properties(
        title=alt.TitleParams(['Minimum salary:'], fontSize=20),
        width=40,
        height=40
    )

    upper_salary = base.mark_text(fontSize=35).encode(
        text=alt.Text('up_text:N'),
    ).transform_filter(brush).transform_aggregate(
        groupby=["s_no"],
        upper_salary="mean(Upper Salary)"
    ).transform_aggregate(
        groupby=[],
        up_salary='mean(upper_salary)'
    ).transform_calculate(
        up_text="round(datum.up_salary) + 'K'"
    ).properties(
        title=alt.TitleParams(['Maximum salary:'], fontSize=20),
        width=40,
        height=40
    )

    # https://stackoverflow.com/questions/67997825/python-altair-generate-a-table-on-selection
    new_df = df_new.groupby(['s_no', 'Job Title', 'Salary Estimate', 'Avg Salary(K)', 'Company Name'])['Skill'].apply(
        ','.join).reset_index()
    new_df.rename(columns={'Skill': 'skill_name'}, inplace=True)
    new_df = new_df.drop_duplicates(subset=['s_no'], keep="first")

    text_title = base.mark_text().properties(
        title=alt.TitleParams(text='Jobs in order of Average salary', align='left', fontSize=20))
    ranked_text = base.mark_text(fontSize=10, align='left').encode(
        y=alt.Y('rank:O', axis=None)
    ).transform_lookup(
        lookup='s_no',
        from_=alt.LookupData(data=new_df, key='s_no',
                             fields=['s_no', 'skill_name'])
    ).transform_filter(
        brush
    ).transform_aggregate(
        groupby=["s_no"],
        job_title="min(Job Title)",
        avg="min(Avg Salary(K))",
        company="min(Company Name)",
        salary="min(Salary Estimate)",
        skills="min(skill_name)"
    ).transform_window(
        rank="rank()",
        sort=[
            alt.SortField("avg", order="descending"),
            alt.SortField("s_no", order="descending")
        ],
        # groupby=["s_no"],
    ).transform_filter(
        'datum.rank < 30'
    )

    ind = ranked_text.encode(text='rank:O').properties(title=alt.TitleParams(text='Rank', align='left'))
    job_title = ranked_text.encode(text='job_title:N').properties(title=alt.TitleParams(text='Job Title', align='left'))
    company = ranked_text.encode(text='company:N').properties(
        title=alt.TitleParams(text='Company Name & Rating', align='left'))
    avg_s = ranked_text.encode(text='avg_sa:N').transform_calculate(
        avg_sa="'$'+round(datum.avg) + 'K'"
    ).properties(title=alt.TitleParams(text='Avg Salary', align='left'))
    salary = ranked_text.encode(text='salary:N').properties(title=alt.TitleParams(text='Salary Estimate', align='left'))
    skill = ranked_text.encode(text='skills:N').properties(title=alt.TitleParams(text='Skill', align='left'))
    row_text = alt.hconcat(ind, job_title, company, avg_s, salary, skill)  # Combine data tables

    skills = (skill_chart.add_selection(brush) + skill_text).properties(
        title=alt.TitleParams('Top Skills in 2021', fontSize=20,
                              subtitle='Select one or more skills'),
        width=450,
        height=400
    )
    top = (alt.layer(error_bar, point_chart, top_industries_1, points).resolve_legend(
        color="independent"
    ).resolve_scale(
        size="independent",
        y='independent'
    ).properties(
        title=alt.TitleParams(text='Top 15 industries by Average Salary', align='center', fontSize=20,
                              subtitle='Mean of Average, Maximum and Minimum'),
        width=450,
        height=400
    ) + top_industries_text).resolve_scale(
        size="independent",
        # y="independent"
    ).resolve_legend(
        color="independent"
    )

    hchart = alt.hconcat(skills, alt.vconcat(eligible, eligibility, avg_salary, upper_salary, lower_salary),
                         top).resolve_scale(
        size="independent",
        y="independent",
        x="independent"
    )
    # Build chart
    table = alt.vconcat(
        hchart,
        text_title,
        row_text
    ).resolve_legend(
        color="independent"
    ).resolve_scale(
        size="independent",
        y="independent",
        x="independent"
    ).configure_view(strokeWidth=0).configure_point(
        size=100
    )

    st.write(table)

    ####################################################################################################################

elif add_selectbox == 'Job Recommendation Dashboard':
    ####################################################################################################################

    api_key = st.secrets["api_key"]
    # client_id = st.secrets["client_id"]
    # secret = st.secrets["secret"]

    filepath_state_code_dict = '/app/final-project-thescientists/datasets/dicts/states_to_codes.txt'
    filepath_state_fips_dict = '/app/final-project-thescientists/datasets/dicts/state_to_fips.txt'
    filepath_skills_to_col_dict = '/app/final-project-thescientists/datasets/dicts/skillname_to_column.txt'

    def get_percentage_match(resume_text, key_words):
        total_key_words = len(key_words)
        matched = 0
        annotated_input = []
        for k in key_words:
            if str(k.lower()) in resume_text:
                matched += 1
                annotated_input.append(("  " + k + "  ", "", "#afa"))
            else:
                annotated_input.append(("  " + k + "  ", "", "#faa"))
        return (matched / total_key_words), annotated_input


    # def get_emi_api_token():
    #     url = "https://auth.emsicloud.com/connect/token"
    #
    #     payload = "client_id=" + client_id + "&client_secret=" + secret + "&grant_type=client_credentials&scope=emsi_open"
    #     headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #
    #     response = requests.request("POST", url, data=payload, headers=headers)
    #     token = json.loads(response.text)['access_token']
    #     return token


    @st.cache
    def get_city_group_by_stats(data):
        gb = data.groupby(['Location'])
        city_groupby_data = gb.agg({'Avg Salary(K)': 'mean', 'Lower Salary': 'mean', 'Upper Salary': 'mean'})
        city_groupby_data.reset_index(inplace=True)
        return city_groupby_data


    def extract_key_words(skills):
        whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        key_words = []
        for s in skills:
            cleaned_skill = ''.join(filter(whitelist.__contains__, s))
            temp_list = cleaned_skill.split()
            for cs in temp_list:
                if cs not in key_words:
                    key_words.append(cs)

        return key_words


    # def extract_skills_from_document(jd):
    #     token = get_emi_api_token()
    #     jd = jd.replace('\n', " ").replace('\t', " ")
    #     jd = re.sub(r'[^A-Za-z0-9 ]+', '', jd)
    #
    #     print("JD: {}".format(jd))
    #
    #     skills_from_doc_endpoint = "https://emsiservices.com/skills/versions/latest/extract"
    #     text = jd
    #     confidence_interval = "0.8"
    #     payload = "{ \"text\": \"... " + text + " ...\", \"confidenceThreshold\": " + confidence_interval + " }"
    #
    #     headers = {
    #         'authorization': "Bearer " + token,
    #         'content-type': "application/json"
    #     }
    #
    #     response = requests.request("POST", skills_from_doc_endpoint, data=payload.encode('utf-8'), headers=headers)
    #
    #     skills_found_in_document_df = pd.DataFrame(pd.json_normalize(response.json()['data']));
    #     skills_found_in_document_df = rename_columns(skills_found_in_document_df)
    #
    #     skills_list = list(skills_found_in_document_df['skill_name'])
    #
    #     return skills_list

    def get_JD_keywords(jd):
        nlp = en_core_web_sm.load()
        doc = nlp(jd)
        key_words = [str(x).lower() for x in doc.ents]
        return key_words


    @st.cache
    def rename_columns(data):
        cols = data.columns
        col_name_mapping = {}
        for x in cols:
            y = x
            x = x.replace(".", "_")
            col_name_mapping[y] = x

        data = data.rename(columns=col_name_mapping)
        return data


    @st.cache
    # file and code referenced from: https://gist.github.com/rogerallen/1583593
    def get_state_code_dict():
        with open(filepath_state_code_dict) as f:
            text_data = f.read()

        dictionary = json.loads(text_data)
        code_to_state = dict(map(reversed, dictionary.items()))
        return code_to_state


    @st.cache
    def get_state_fips():
        with open(filepath_state_fips_dict) as f:
            text_data = f.read()

        dictionary = json.loads(text_data)
        return dictionary


    @st.cache
    def get_skill_col_dict():
        with open(filepath_skills_to_col_dict) as f:
            text_data = f.read()

        dictionary = json.loads(text_data)
        return dict(dictionary)


    def extract_lat_lng(address_or_postalcode, data_type='json'):
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
        params = {"address": address_or_postalcode, "key": api_key}
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)
        if r.status_code not in range(200, 299):
            return {}
        latlng = {}
        try:
            latlng = r.json()['results'][0]['geometry']['location']
        except:
            pass
        return latlng.get("lat"), latlng.get("lng")


    def get_code_for_state(state_name, info_dict):
        key_list = list(info_dict.keys())
        val_list = list(info_dict.values())
        position = val_list.index(state)
        return key_list[position]


    def get_lat_long(data):
        data["latlong"] = data["Location"].map(lambda a: extract_lat_lng(a))
        data["latitude"] = data["latlong"].map(lambda a: a[0])
        data["longitude"] = data["latlong"].map(lambda a: a[1])

        data = data.drop(columns=['latlong'])

        return data


    def data_filter_dashboard(df, code_state_dict, skill_to_col_dict, state, salary_range, skills, industry):
        labels = pd.Series([1] * len(df), index=df.index)

        if skills:
            for skill in skills:
                labels |= df[skill_to_col_dict[skill]] == 1

        if salary_range is not None:
            labels &= df['Lower Salary'] >= (salary_range[0] / 1000)
            labels &= df['Upper Salary'] <= (salary_range[1] / 1000)

        if state is not None and state != 'All':
            #st.write(get_code_for_state(state, code_state_dict))
            labels &= df['Job Location'] == get_code_for_state(state, code_state_dict)

        if industry and industry != 'All':
            labels &= df['Industry'] == industry

        return labels


    def get_resume_text(file):
        text_data = ""
        with pdfplumber.open(file) as pdf:
            pages = pdf.pages
            for p in pages:
                text_data = text_data + " " + p.extract_text()

        whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        answer = ''.join(filter(whitelist.__contains__, text_data))
        # print('#' * 30)
        # print(answer)
        # print('#' * 30)
        # text = "".join(text.split())

        return answer.lower()


    st.title('Job Recommendation Dashboard')

    st.markdown('#### Filter Data Science roles in you preferred US State based on you expected Salary, Skills and preferred Industry of work')

    dataset = load_data()
    dataset = dataset.drop_duplicates()
    dataset = dataset.drop(['index'], axis=1)

    code_to_state_dict = get_state_code_dict()
    skill_col_dict = get_skill_col_dict()
    city_groupby_stats = get_city_group_by_stats(dataset)

    states_plotting = alt.topo_feature(data.us_10m.url, 'states')
    state_fips = get_state_fips()

    unique_states = list(dataset["Job Location"].map(code_to_state_dict).unique())
    unique_states.insert(1, 'All')
    state = st.selectbox('State:', unique_states)

    exp_salary_range = st.slider('Expected Salary Range:',
                                 min_value=int(dataset['Lower Salary'].min() * 1000),
                                 max_value=int(dataset['Upper Salary'].max() * 1000),
                                 value=(
                                     int(dataset['Lower Salary'].min() * 1000),
                                     int(dataset['Upper Salary'].max() * 1000)))

    skills_selected = st.multiselect('Skills Possessed:',
                                     ["Python", "Apache Spark", "AWS", "MS Excel", "SQL", "SAS", "Keras", "PyTorch",
                                      "SciKit",
                                      "Tensorflow", "Hadoop", "Tableau", "Power BI", "Apache Flink", "MongoDB",
                                      "Google Analytics"],
                                     ['Python'])

    ind_unique = list(dataset["Industry"].unique())
    ind_unique.insert(0, 'All')
    industry = st.selectbox('Industry:', ind_unique)

    filtered_data_labels = data_filter_dashboard(dataset, code_to_state_dict, skill_col_dict, state, exp_salary_range,
                                                 skills_selected, industry)

    filtered_data = dataset[filtered_data_labels]

    st.markdown("""---""")

    if len(filtered_data) > 0:
        st.markdown("**Locations of Data Science roles in {}**".format(state))

        loc_counts_df = filtered_data['Location'].value_counts().rename_axis('Location').reset_index(name='Jobs Available')
        plotting_data = get_lat_long(loc_counts_df)
        plotting_data['Jobs Available'] = plotting_data['Jobs Available'].fillna(0).astype(int)

        plotting_data = plotting_data.merge(city_groupby_stats, on='Location', how='left')
        plotting_data[['Avg Salary(K)', 'Lower Salary', 'Upper Salary']] = 1000 * plotting_data[
            ['Avg Salary(K)', 'Lower Salary', 'Upper Salary']]
        plotting_data = plotting_data.rename({'Avg Salary(K)': 'Average Salary'}, axis=1)

        if st.checkbox("Show State/City Job Summary:"):
            st.write(plotting_data[['Location', 'Jobs Available', 'Average Salary', 'Lower Salary', 'Upper Salary']])


        # the base chart
        base = alt.Chart(plotting_data)

        # generate the points
        points = base.mark_point(
            filled=True,
            size=100
        ).encode(
            x=alt.X('Location', ),
            y=alt.Y('Average Salary'),
            color=alt.Color("Location")
        )

        # generate the error bars
        errorbars = base.mark_errorbar().encode(
            x="Location",
            y="Lower Salary",
            y2="Upper Salary",
            color=alt.Color("Location"),
            tooltip=['Location:N', 'Average Salary:Q', 'Lower Salary:Q', 'Upper Salary:Q']
        )

        error_bar_plot = points + errorbars

        pts = alt.Chart(plotting_data).mark_circle(
            tooltip=True,
            color='darkred',
            fill='red',
            size=70
        ).encode(
            latitude='latitude',
            longitude='longitude',
            tooltip=['Location:N', 'Jobs Available:Q']
        )

        if (state != 'All'):
            outline = alt.Chart(states_plotting).mark_geoshape(
                fill='lightseagreen',
                stroke='white'
            ).project(
                'albersUsa'
            ).transform_calculate(
                state_id="(datum.id)"
            ).transform_filter(
                alt.datum.state_id == int(state_fips[get_code_for_state(state, code_to_state_dict)])
            )
        else:
            # US states background
            outline = alt.Chart(states_plotting).mark_geoshape(
                fill='lightgray',
                stroke='white'
            ).properties(
                title='US Data Science roles map'
            ).project('albersUsa')

        state_plot = outline + pts

        st.write(state_plot | error_bar_plot)

        st.markdown("""---""")

        reco_data = filtered_data[['Company Name', 'Job Title', 'Location']]
        reco_data['Company Name'] = reco_data['Company Name'].str.rpartition('\n')[0]
        jobs_list = reco_data.values.tolist()

        jobs_list_joined = []
        for job in jobs_list:
            jobs_list_joined.append(str(job[1]) + '    at    ' + str(job[0]) + '    in    ' + str(job[2]))

        st.markdown(
            '#### Now that you have your options, go ahead and analyze the role and if you fit their requirements ')
        select_job = st.selectbox('Select desired role to view job summary:', jobs_list_joined)
        selected_index = jobs_list_joined.index(select_job)
        sel_job_data = filtered_data.iloc[selected_index, :]

        st.markdown("""---""")

        cols = st.columns((1, 1))
        with cols[0]:
            data_display = sel_job_data['Company Name'].replace("\n", ", ").split(", ")
            st.markdown("**{}** (Glassdoor Rating: {}/5)".format(data_display[0], data_display[1]))
            st.markdown("**Headquarters:** {}".format(sel_job_data['Headquarters']))
            st.markdown("**Industry:** {}".format(sel_job_data['Industry']))
        with cols[1]:
            st.markdown("**Role:** {}".format(sel_job_data['Job Title']))
            st.markdown("**Salary:** {}".format(str(sel_job_data['Salary Estimate']).replace("$", "\$")))
            st.markdown("**Location:** {}".format(sel_job_data['Location']))

        with st.expander("See Job Description"):
            st.write(sel_job_data['Job Description'])

        st.markdown("""---""")

        st.markdown(
            '#### Analyze if your current Resume matches the Job Description for the chosen role')

        # st.markdown("**Preferred Skills/Proficiencies by Recruiter according to Job Description:**")
        # st.markdown(extract_skills_from_document(sel_job_data['Job Description']))

        # skills_list = extract_skills_from_document(sel_job_data['Job Description'])

        skills_list = get_JD_keywords(sel_job_data['Job Description'])

        key_words_updated = extract_key_words(skills_list)

        uploaded_file = st.file_uploader("Upload your Resume to analyze match with Job Description:")

        if uploaded_file is not None:
            resume_text = get_resume_text(uploaded_file)
            # print("resume text: {}".format(resume_text))

            # key_words = get_JD_keywords(sel_job_data['Job Description'])

            percent_match, suggested_key_words = get_percentage_match(resume_text, key_words_updated)

            st.markdown("**Resume Match Percentage:**")
            cols = st.columns((1, 0.1, 2))
            with cols[0]:
                match_percent = percent_match * 100
                if match_percent > 60:
                    feedback = 'Good match! You are ready to apply.'
                elif 60 >= match_percent > 30:
                    feedback = 'Decent match, Improve it by adding suggested key words to resume.'
                else:
                    feedback = 'Low match score.'

                st.markdown("# " + str('{:.2f} %'.format(match_percent)))

            with cols[2]:
                st.markdown("#### " + feedback)

            st.markdown("""---""")

            st.markdown("**Suggested Keywords to improve Resume Matching Percentage:**")
            st.write('The keywords highlighted in Red are missing from your resume. Addign them will improve your chances'
                     ' of being shortlisted by Recruiters. The keywords highlited in Green are already present in your Resume.')
            annotated_text(*suggested_key_words)
    else:
        st.write('No Job roles to display')
####################################################################################################################
