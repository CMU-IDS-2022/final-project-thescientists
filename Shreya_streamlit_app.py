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
        
        job_type = list(jobs['Job_Type'].unique())  + [None]
        
        company_names = list(jobs['Company'].unique()) + [None]
        st.write(company_names)
        #company_names.insert(1, 'All')
                    
       # input_dropdown_job = alt.binding_select(options=job_type, name='Job Type')
        input_dropdown_job = alt.binding_select(options=[None,'FULL_TIME','PART_TIME','CONTRACTOR','INTERN','TEMPORARY'],labels=['All','FULL_TIME','PART_TIME','CONTRACTOR','INTERN','TEMPORARY'])
        job_type_selection = alt.selection_single(fields=['Job_Type'], bind=input_dropdown_job, name='Job Type')
        
        
        
        companies =[None,"ManTech" ,"GEICO" ,"Tecolote Research" ,"Systems &amp;amp; Technology Research" ,"Booz Allen Hamilton Inc." ,"Novetta" ,"The Knot Worldwide" ,"Amazon" ,"Seen by Indeed" ,"MITRE" ,"Mathematica Policy Research" ,"CyberCoders" ,"Elder Research" ,"Department of Energy" ,"LMI" ,"Expression Networks" ,"U.S. General Services Administration" ,"West 4th Strategy" ,"IT Resonance Inc" ,"Artlin Consulting" ,"Applied Research Associates, Inc." ,"CIA" ,"Fannie Mae" ,"Analytica" ,"Piper Enterprise Solutions" ,"Meridian Knowledge Solutions" ,"Storyblocks" ,"The Ashlar Group" ,"Koch Industries" ,"Aptive" ,"Pandera Systems" ,"Thresher" ,"Na Ali&amp;#039;i" ,"Navigant Consulting" ,"DCS CORPORATION" ,"University of Maryland" ,"Pragmatics" ,"Thomson Reuters Corporation" ,"World Bank" ,"Culmen International, LLC" ,"HRUCKUS" ,"The Rock Creek Group" ,"Ollie&amp;#039;s Bargain Outlet" ,"Ridgeline International" ,"Cognosante" ,"Resolvit.com" ,"1901 Group" ,"Job Juncture" ,"Royce Geospatial" ,"Pivotal Software" ,"Sprezzatura Management Consulting" ,"B4Corp" ,"Knowesis Inc." ,"I-Link Solutions" ,"General Services Admin" ,"Akima Management Services" ,"Northrop Grumman" ,"ALQIMI" ,"Sierra Nevada Corporation" ,"Tetra Tech" ,"Information Gateways" ,"SAIC" ,"Office of Inspector General" ,"TransVoyant" ,"Hire Velocity" ,"Carolina Power &amp;amp; Light Co" ,"Research Innovations" ,"Tek Leaders" ,"Valiant Integrated Services" ,"RTI Consulting" ,"BlueLabs" ,"AnaVation LLC" ,"Latitude, Inc." ,"Noblis" ,"Reveal Global Consulting LLC" ,"Berico Technologies" ,"The Aerospace Corporation" ,"Varen Technologies" ,"Infinitive Inc" ,"Axiologic Solutions" ,"Visionist, Inc." ,"Pyramid Systems, Inc." ,"Strategic Alliance Consulting, Inc" ,"1884794" ,"Lucidus Solutions, LLC" ,"BlackFern Recruitment" ,"Leidos" ,"NT Concepts" ,"Lockheed Martin" ,"BCT LLC" ,"Ops Tech Alliance" ,"Electronic Consulting Services, Inc." ,"Omni Consulting Solutions" ,"Dezign Concepts LLC" ,"General Dynamics Information Technology" ,"ISYS Technologies, Inc." ,"Praxis Engineering" ,"Serry Systems" ,"Peraton" ,"Nolij Consulting" ,"Guidehouse" ,"Solekai Systems Corp" ,"Par Government Systems Corporation" ,"Facebook" ,"METIS Solutions" ,"Accenture" ,"Atlas Research" ,"Teaching Strategies, LLC" ,"Ledger Investing" ,"West Creek Financial" ,"Tiger Analytics" ,"NCQA" ,"Ball Corporation" ,"Kelly" ,"CGI" ,"IEM, Inc" ,"Discovery Communications, Inc." ,"Ball Metal Food Container Corp" ,"Oracle" ,"Optimal Solutions Group" ,"Metaphase Consulting" ,"IT Resonance Inc." ,"nDemand Consulting LLC" ,"IBM Corporation" ,"Fors Marsh Group" ,"Deloitte" ,"New Light Technologies, Inc." ,"The Interface Financial Group" ,"Ball Corporation / Ball Aerospace" ,"OnwardPath Technology Solutions LLC" ,"Premise" ,"Institute for Justice" ,"US Department of Treasury" ,"NVIDIA" ,"Credence Management Solutions, LLC" ,"KaiHonua" ,"CareJourney" ,"Veracity Engineering" ,"XOR Security" ,"Excel Global Solutions" ,"Resolvit" ,"Raytheon Intelligence &amp;amp; Space" ,"Treasury, Departmental Offices" ,"CICONIX, LLC" ,"CGI Technologies and Solutions, Inc." ,"Cherokee Nation Businesses, LLC" ,"HUBZone HQ" ,"Celestar Corporation" ,"CMCI" ,"Royce Geospatial Consultants Inc" ,"Øptimus Consulting" ,"Metronome, LLC" ,"SESC" ,"Computercraft" ,"Aireon" ,"Param Solutions" ,"NIH" ,"Microsoft Corporation" ,"CAMRIS International" ,"NCI Information Systems, Inc." ,"22nd Century Technologies" ,"Discovery Communications" ,"Huntington Ingalls Industries" ,"RTI Consulting, LLC" ,"Mission Intel" ,"CEDENT" ,"Cedent Consulting" ,"Leidos Holdings Inc." ,"Lidl" ,"KPMG" ,"Systems Planning and Analysis, Inc." ,"General Dynamics" ,"IntegrateIT" ,"Salient CRGT" ,"Synertex LLC" ,"DirectViz, LLC" ,"NCI Information Systems Inc." ,"DirectViz Solutions, LLC" ,"Jacobs" ,"Whiteboard Federal" ,"The Air-Conditioning, Heating, and Refrigeration Institute (AHRI)" ,"VISUAL SOFT, INC" ,"Parsons Commercial Technology Group Inc." ,"Johns Hopkins University Applied Physics Laboratory" ,"Geodata IT, LLC" ,"Parsons Corporation" ,"DeNOVO Solutions" ,"Synertex" ,"S2 Analytical Solutions LLC" ,"BAE Systems USA" ,"TENICA and Associates LLC" ,"HopHR" ,"IBM" ,"Blue Compass, LLC" ,"Trusted Knowledge Options Inc." ,"All Native Group The Federal Services Division of Ho-Chunk Inc" ,"ALL NATIVE GROUP" ,"Boeing" ,"Management Decisions, Inc." ,"CACI International" ,"Bluemont Technology &amp;amp; Research, Inc." ,"Perspecta" ,"Nyla Technology Solutions" ,"Booz Allen Hamilton" ,"Brinks Home Security" ,"Health IQ" ,"Zynga" ,"Evernote" ,"Lightspeed Systems" ,"Bakery Agency" ,"Oscar Associates Americas LLC" ,"ThoughtFocus" ,"Home Depot" ,"Apple" ,"Keylent" ,"Schlumberger" ,"Robert Half" ,"Aramco Services Company" ,"iHeartMedia" ,"Cytracom" ,"Alaka`ina Foundation Family of Companies" ,"Inabia Software &amp;amp; consulting Inc." ,"Onica Group" ,"CGG Veritas" ,"Next Level Business Services, Inc." ,"Dun &amp;amp; Bradstreet" ,"JPMorgan Chase" ,"Southwest Business Corporation" ,"Randstad" ,"Abbott Laboratories" ,"Alakaina Family of Companies" ,"Cloudflare, Inc." ,"Horne LLP" ,"Focus America inc" ,"Inherent Technologies" ,"Jabil" ,"Abbott" ,"Itbrainiac" ,"IMG Systems" ,"Cottonwood Financial" ,"CGG" ,"Lorhan" ,"RMS Computer" ,"Ke`aki Technologies, LLC" ,"Sercel" ,"Cenergy International" ,"APN Software Services Inc." ,"Siri InfoSolutions Inc" ,"Trinity Industries" ,"NTT DATA Services" ,"Geval6 Inc" ,"Applied Research Laboratories" ,"Signature Science, LLC" ,"Energy Cognito" ,"Levelset" ,"PriceSenz" ,"Kairos Technologies" ,"Frontier Communications" ,"Vinli" ,"Whole Foods Market" ,"Sense Corp" ,"Onica, a Rackspace Company" ,"Infosys" ,"LivaNova" ,"Humana" ,"Walmart" ,"Veear Projects" ,"Givelify" ,"ka-hoot" ,"SEVEN Networks" ,"Wise Men Consultants" ,"Rackspace" ,"Zdaly" ,"University of Texas Medical Branch" ,"Parkland Health and Hospital System" ,"Kinder Morgan" ,"Cloudflare" ,"BlockTrace, LLC" ,"IT First Source" ,"Cyber Warrior Network" ,"USAA" ,"Enbridge" ,"Alliance Data" ,"Ava Consulting" ,"Spectral MD, Inc." ,"Neiman Marcus" ,"AmerisourceBergen" ,"US Army Network Enterprise Technology Command" ,"VIVA USA" ,"Faire" ,"GovTech" ,"Triplebyte" ,"Notion Labs" ,"Autodesk" ,"Formation" ,"Duetto" ,"Demandbase" ,"Balyasny Asset Management" ,"Centraprise" ,"Upstart" ,"Nuna" ,"Strivr" ,"Aktana" ,"Unlearn.AI" ,"Turn/River Capital" ,"University of California San Francisco" ,"Descript" ,"Medidata Solutions" ,"Divvy Homes" ,"Ready Responders" ,"MasterClass" ,"SoftBank Robotics" ,"Lilt" ,"RiskIQ" ,"Cogitativo" ,"Brightidea" ,"Trace Data" ,"Observable" ,"Eaze" ,"Mindstrong" ,"Mackin" ,"Appen" ,"Roblox" ,"Geli" ,"Genentech" ,"Sartorius" ,"Aclima" ,"Mentor Graphics" ,"TECHNOCRAFT Solutions" ,"PG&amp;amp;E Corporation" ,"TRM Labs" ,"Navio" ,"Entefy" ,"Canopy Health" ,"Goodwater Capital" ,"The Judge Group, Inc." ,"Snowflake" ,"Quantifind" ,"Landing AI" ,"Getty Images" ,"TCG" ,"Twitter" ,"The Climate Corporation" ,"Jobot" ,"Stitch Fix" ,"Philo" ,"PG&amp;amp;E" ,"Sunvalleytek International Inc." ,"Allstate" ,"ClassDojo" ,"Chime" ,"Atlassian" ,"Motif Investing" ,"Aetna" ,"PsiNapse Technology, Ltd." ,"Landing" ,"Tesla Motors" ,"EDI Specialists, Inc." ,"DocuSign" ,"Thunder" ,"Tempus Labs" ,"Vhire" ,"Slack" ,"Swinerton Builders" ,"Sensor Tower" ,"Center for Sustainable" ,"Twist Bioscience" ,"Meraki" ,"Moloco, Inc." ,"Noblr" ,"Tencent" ,"Windfall Data" ,"Denali Therapeutics" ,"Two95 International Inc." ,"Lawrence Berkeley Lab" ,"Aisera" ,"DoorDash" ,"One Concern" ,"FortressIQ" ,"VDart, Inc." ,"AutoGrid" ,"insitro" ,"OneinaMil" ,"Tesla" ,"PAVIR" ,"The Play Station" ,"Ayata" ,"Lattice Engines" ,"GRAIL" ,"CitiusTech" ,"Leibniz Center for Psychological" ,"Vitria Technology" ,"Rad AI" ,"The Clorox Company" ,"QUICKEN INVESTMENT SERVICES, INC." ,"Lam Research" ,"Project Ronin" ,"Eluvio" ,"Non Specific Employer" ,"Electronic Arts" ,"V3 Talent Partners Inc." ,"Crystal Dynamics" ,"Siemens Healthineers"]
        use_labels =["All","ManTech" ,"GEICO" ,"Tecolote Research" ,"Systems &amp;amp; Technology Research" ,"Booz Allen Hamilton Inc." ,"Novetta" ,"The Knot Worldwide" ,"Amazon" ,"Seen by Indeed" ,"MITRE" ,"Mathematica Policy Research" ,"CyberCoders" ,"Elder Research" ,"Department of Energy" ,"LMI" ,"Expression Networks" ,"U.S. General Services Administration" ,"West 4th Strategy" ,"IT Resonance Inc" ,"Artlin Consulting" ,"Applied Research Associates, Inc." ,"CIA" ,"Fannie Mae" ,"Analytica" ,"Piper Enterprise Solutions" ,"Meridian Knowledge Solutions" ,"Storyblocks" ,"The Ashlar Group" ,"Koch Industries" ,"Aptive" ,"Pandera Systems" ,"Thresher" ,"Na Ali&amp;#039;i" ,"Navigant Consulting" ,"DCS CORPORATION" ,"University of Maryland" ,"Pragmatics" ,"Thomson Reuters Corporation" ,"World Bank" ,"Culmen International, LLC" ,"HRUCKUS" ,"The Rock Creek Group" ,"Ollie&amp;#039;s Bargain Outlet" ,"Ridgeline International" ,"Cognosante" ,"Resolvit.com" ,"1901 Group" ,"Job Juncture" ,"Royce Geospatial" ,"Pivotal Software" ,"Sprezzatura Management Consulting" ,"B4Corp" ,"Knowesis Inc." ,"I-Link Solutions" ,"General Services Admin" ,"Akima Management Services" ,"Northrop Grumman" ,"ALQIMI" ,"Sierra Nevada Corporation" ,"Tetra Tech" ,"Information Gateways" ,"SAIC" ,"Office of Inspector General" ,"TransVoyant" ,"Hire Velocity" ,"Carolina Power &amp;amp; Light Co" ,"Research Innovations" ,"Tek Leaders" ,"Valiant Integrated Services" ,"RTI Consulting" ,"BlueLabs" ,"AnaVation LLC" ,"Latitude, Inc." ,"Noblis" ,"Reveal Global Consulting LLC" ,"Berico Technologies" ,"The Aerospace Corporation" ,"Varen Technologies" ,"Infinitive Inc" ,"Axiologic Solutions" ,"Visionist, Inc." ,"Pyramid Systems, Inc." ,"Strategic Alliance Consulting, Inc" ,"1884794" ,"Lucidus Solutions, LLC" ,"BlackFern Recruitment" ,"Leidos" ,"NT Concepts" ,"Lockheed Martin" ,"BCT LLC" ,"Ops Tech Alliance" ,"Electronic Consulting Services, Inc." ,"Omni Consulting Solutions" ,"Dezign Concepts LLC" ,"General Dynamics Information Technology" ,"ISYS Technologies, Inc." ,"Praxis Engineering" ,"Serry Systems" ,"Peraton" ,"Nolij Consulting" ,"Guidehouse" ,"Solekai Systems Corp" ,"Par Government Systems Corporation" ,"Facebook" ,"METIS Solutions" ,"Accenture" ,"Atlas Research" ,"Teaching Strategies, LLC" ,"Ledger Investing" ,"West Creek Financial" ,"Tiger Analytics" ,"NCQA" ,"Ball Corporation" ,"Kelly" ,"CGI" ,"IEM, Inc" ,"Discovery Communications, Inc." ,"Ball Metal Food Container Corp" ,"Oracle" ,"Optimal Solutions Group" ,"Metaphase Consulting" ,"IT Resonance Inc." ,"nDemand Consulting LLC" ,"IBM Corporation" ,"Fors Marsh Group" ,"Deloitte" ,"New Light Technologies, Inc." ,"The Interface Financial Group" ,"Ball Corporation / Ball Aerospace" ,"OnwardPath Technology Solutions LLC" ,"Premise" ,"Institute for Justice" ,"US Department of Treasury" ,"NVIDIA" ,"Credence Management Solutions, LLC" ,"KaiHonua" ,"CareJourney" ,"Veracity Engineering" ,"XOR Security" ,"Excel Global Solutions" ,"Resolvit" ,"Raytheon Intelligence &amp;amp; Space" ,"Treasury, Departmental Offices" ,"CICONIX, LLC" ,"CGI Technologies and Solutions, Inc." ,"Cherokee Nation Businesses, LLC" ,"HUBZone HQ" ,"Celestar Corporation" ,"CMCI" ,"Royce Geospatial Consultants Inc" ,"Øptimus Consulting" ,"Metronome, LLC" ,"SESC" ,"Computercraft" ,"Aireon" ,"Param Solutions" ,"NIH" ,"Microsoft Corporation" ,"CAMRIS International" ,"NCI Information Systems, Inc." ,"22nd Century Technologies" ,"Discovery Communications" ,"Huntington Ingalls Industries" ,"RTI Consulting, LLC" ,"Mission Intel" ,"CEDENT" ,"Cedent Consulting" ,"Leidos Holdings Inc." ,"Lidl" ,"KPMG" ,"Systems Planning and Analysis, Inc." ,"General Dynamics" ,"IntegrateIT" ,"Salient CRGT" ,"Synertex LLC" ,"DirectViz, LLC" ,"NCI Information Systems Inc." ,"DirectViz Solutions, LLC" ,"Jacobs" ,"Whiteboard Federal" ,"The Air-Conditioning, Heating, and Refrigeration Institute (AHRI)" ,"VISUAL SOFT, INC" ,"Parsons Commercial Technology Group Inc." ,"Johns Hopkins University Applied Physics Laboratory" ,"Geodata IT, LLC" ,"Parsons Corporation" ,"DeNOVO Solutions" ,"Synertex" ,"S2 Analytical Solutions LLC" ,"BAE Systems USA" ,"TENICA and Associates LLC" ,"HopHR" ,"IBM" ,"Blue Compass, LLC" ,"Trusted Knowledge Options Inc." ,"All Native Group The Federal Services Division of Ho-Chunk Inc" ,"ALL NATIVE GROUP" ,"Boeing" ,"Management Decisions, Inc." ,"CACI International" ,"Bluemont Technology &amp;amp; Research, Inc." ,"Perspecta" ,"Nyla Technology Solutions" ,"Booz Allen Hamilton" ,"Brinks Home Security" ,"Health IQ" ,"Zynga" ,"Evernote" ,"Lightspeed Systems" ,"Bakery Agency" ,"Oscar Associates Americas LLC" ,"ThoughtFocus" ,"Home Depot" ,"Apple" ,"Keylent" ,"Schlumberger" ,"Robert Half" ,"Aramco Services Company" ,"iHeartMedia" ,"Cytracom" ,"Alaka`ina Foundation Family of Companies" ,"Inabia Software &amp;amp; consulting Inc." ,"Onica Group" ,"CGG Veritas" ,"Next Level Business Services, Inc." ,"Dun &amp;amp; Bradstreet" ,"JPMorgan Chase" ,"Southwest Business Corporation" ,"Randstad" ,"Abbott Laboratories" ,"Alakaina Family of Companies" ,"Cloudflare, Inc." ,"Horne LLP" ,"Focus America inc" ,"Inherent Technologies" ,"Jabil" ,"Abbott" ,"Itbrainiac" ,"IMG Systems" ,"Cottonwood Financial" ,"CGG" ,"Lorhan" ,"RMS Computer" ,"Ke`aki Technologies, LLC" ,"Sercel" ,"Cenergy International" ,"APN Software Services Inc." ,"Siri InfoSolutions Inc" ,"Trinity Industries" ,"NTT DATA Services" ,"Geval6 Inc" ,"Applied Research Laboratories" ,"Signature Science, LLC" ,"Energy Cognito" ,"Levelset" ,"PriceSenz" ,"Kairos Technologies" ,"Frontier Communications" ,"Vinli" ,"Whole Foods Market" ,"Sense Corp" ,"Onica, a Rackspace Company" ,"Infosys" ,"LivaNova" ,"Humana" ,"Walmart" ,"Veear Projects" ,"Givelify" ,"ka-hoot" ,"SEVEN Networks" ,"Wise Men Consultants" ,"Rackspace" ,"Zdaly" ,"University of Texas Medical Branch" ,"Parkland Health and Hospital System" ,"Kinder Morgan" ,"Cloudflare" ,"BlockTrace, LLC" ,"IT First Source" ,"Cyber Warrior Network" ,"USAA" ,"Enbridge" ,"Alliance Data" ,"Ava Consulting" ,"Spectral MD, Inc." ,"Neiman Marcus" ,"AmerisourceBergen" ,"US Army Network Enterprise Technology Command" ,"VIVA USA" ,"Faire" ,"GovTech" ,"Triplebyte" ,"Notion Labs" ,"Autodesk" ,"Formation" ,"Duetto" ,"Demandbase" ,"Balyasny Asset Management" ,"Centraprise" ,"Upstart" ,"Nuna" ,"Strivr" ,"Aktana" ,"Unlearn.AI" ,"Turn/River Capital" ,"University of California San Francisco" ,"Descript" ,"Medidata Solutions" ,"Divvy Homes" ,"Ready Responders" ,"MasterClass" ,"SoftBank Robotics" ,"Lilt" ,"RiskIQ" ,"Cogitativo" ,"Brightidea" ,"Trace Data" ,"Observable" ,"Eaze" ,"Mindstrong" ,"Mackin" ,"Appen" ,"Roblox" ,"Geli" ,"Genentech" ,"Sartorius" ,"Aclima" ,"Mentor Graphics" ,"TECHNOCRAFT Solutions" ,"PG&amp;amp;E Corporation" ,"TRM Labs" ,"Navio" ,"Entefy" ,"Canopy Health" ,"Goodwater Capital" ,"The Judge Group, Inc." ,"Snowflake" ,"Quantifind" ,"Landing AI" ,"Getty Images" ,"TCG" ,"Twitter" ,"The Climate Corporation" ,"Jobot" ,"Stitch Fix" ,"Philo" ,"PG&amp;amp;E" ,"Sunvalleytek International Inc." ,"Allstate" ,"ClassDojo" ,"Chime" ,"Atlassian" ,"Motif Investing" ,"Aetna" ,"PsiNapse Technology, Ltd." ,"Landing" ,"Tesla Motors" ,"EDI Specialists, Inc." ,"DocuSign" ,"Thunder" ,"Tempus Labs" ,"Vhire" ,"Slack" ,"Swinerton Builders" ,"Sensor Tower" ,"Center for Sustainable" ,"Twist Bioscience" ,"Meraki" ,"Moloco, Inc." ,"Noblr" ,"Tencent" ,"Windfall Data" ,"Denali Therapeutics" ,"Two95 International Inc." ,"Lawrence Berkeley Lab" ,"Aisera" ,"DoorDash" ,"One Concern" ,"FortressIQ" ,"VDart, Inc." ,"AutoGrid" ,"insitro" ,"OneinaMil" ,"Tesla" ,"PAVIR" ,"The Play Station" ,"Ayata" ,"Lattice Engines" ,"GRAIL" ,"CitiusTech" ,"Leibniz Center for Psychological" ,"Vitria Technology" ,"Rad AI" ,"The Clorox Company" ,"QUICKEN INVESTMENT SERVICES, INC." ,"Lam Research" ,"Project Ronin" ,"Eluvio" ,"Non Specific Employer" ,"Electronic Arts" ,"V3 Talent Partners Inc." ,"Crystal Dynamics" ,"Siemens Healthineers"]
        
        input_dropdown_company = alt.binding_select(options=companies, labels = use_labels, name='Company Name')
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
    
