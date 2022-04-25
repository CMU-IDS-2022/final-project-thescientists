# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 21:15:23 2022

@author: kriti
"""

import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

st.set_page_config(layout="wide")

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
    data=load_data()
    
    # for i,v in (data.iteritems()):
    #     st.write(i,v.dtype)
        
    st.write('Industry/Company charts')
    st.header("Skill demand by industry")
    industry=list(data.Industry.unique())
    industry_select=st.multiselect("",industry,['Aerospace & Defense'])
    
    long_form=data.iloc[:,np.r_[0:3,5,11,17:20,23:39]]
    
    
    long_form=long_form.melt(id_vars=['index','Job Title','Salary Estimate','Company Name','Industry',
                                      'Avg Salary(K)','Lower Salary','Upper Salary'], 
                             var_name='Skill', value_name='required')
    long_form.rename(columns = {'index':'s_no'}, inplace = True)
    long_form['Skill']=long_form['Skill'].str.upper()
    df_new_old=long_form.loc[long_form['Industry'].isin(industry_select)]
    

    df_new_1=df_new_old[df_new_old.required==1].iloc[:,:-1]
    
    l=list(df_new_old.groupby('s_no').filter(lambda x : x['required'].sum() ==0)['s_no'].unique())
    df_new_2=df_new_old[df_new_old['s_no'].isin(l)].iloc[:,:-1].drop_duplicates('s_no')
    df_new_2.Skill='None'
    
    df_new=pd.concat([df_new_1,df_new_2])
    
    
    brush = alt.selection(type="multi", encodings=['y'])
    
    
    base = alt.Chart(df_new).transform_joinaggregate(
            Total='count(*)'
        ).transform_calculate(
            PercentOfTotal='1 / datum.Total'
        )
        
            
        
    skill_chart=base.mark_bar().encode(
        alt.X('sum(PercentOfTotal):Q', axis=alt.Axis(format='%',domain=False),title='% of job listings requiring the skill'),
        alt.Y("Skill:O", scale=alt.Scale(zero=False), sort='-x'),
        color=alt.condition(brush, alt.value('darkgreen'),alt.value('lightgreen')),
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.4)),
        tooltip=['Skill', 'count()',alt.Tooltip('sum(PercentOfTotal):Q',format='%')]
    )
    
    skill_text=skill_chart.mark_text(
        align='left',
        baseline='middle',
        dx=3
    ).encode(
        text='count():Q'
    )
       

    
    show_data=st.checkbox('Show raw data')
    if show_data:
        st.write(df_new)
    
    
    columns=['Industry:N','count:Q','mean_sal:Q',
             'max_sal:Q','min_sal:Q']
    
    top_industries=alt.Chart(long_form[long_form.required==1].iloc[:,:-1]).transform_filter(brush).encode(
        x=alt.X('Industry:N',
                sort=alt.SortField(field='mean_sal', order='descending'))
    ).transform_aggregate(
        count='count()',
        mean_sal='mean(Avg Salary(K)):Q',
        max_sal='mean(Upper Salary):Q',
        min_sal='mean(Lower Salary):Q',
        groupby=['Industry']
    ).transform_window(
        window=[{'op': 'rank', 'as': 'rank'}],
        sort=[{'field': 'mean_sal', 'order': 'descending'}]
    ).transform_filter(('datum.rank <= 20'))
    

    selection = alt.selection_single(fields=['Industry'], nearest=True, 
                on='mouseover', empty='none', clear='mouseout')

        
    top_industries_1=top_industries.mark_rule(color='darkgrey').encode(
        opacity=alt.condition(selection, alt.value(0.6), alt.value(0)),
        tooltip=[alt.Tooltip(c) for c in columns]
    ).add_selection(selection)
    

    error_bar=top_industries.mark_errorbar(opacity=0.4, color='darkgreen').encode(
    alt.Y('max_sal:Q', 
          axis=alt.Axis(title='Salary difference (in $1000)',domain=False,
                        tickSize=0, labelPadding=3, format='.0f'),scale=alt.Scale(zero=False)),
    alt.Y2('min_sal:Q'),
    strokeWidth=alt.value(2)
    )
    
    
    point_chart = top_industries.mark_point(filled=True,color='darkgreen').encode(
    alt.Y('mean_sal:Q'))

    points = point_chart.mark_point(color='darkgreen').transform_filter(selection)

    top_industries_text=point_chart.mark_text(
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

    
    eligible=base.mark_text(fontSize=35).encode(
        text=alt.Text('sum(PercentOfTotal):Q',format='.2%'),
        size=alt.Size(legend=None)
    ).transform_filter(brush).properties(
        title=alt.TitleParams(['% of jobs you',' are eligible for:'],fontSize=20),
        
    )
    
    eligibility=base.mark_text(fontSize=35).encode(
        text='count():Q',
        size=alt.Size(legend=None)
    ).transform_filter(brush).properties(
        title=alt.TitleParams(['Number of jobs you',' are eligible for:'],fontSize=20),
        
    )
        
    avg_salary=base.mark_text(fontSize=35).encode(
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
        title=alt.TitleParams(['Average salary:'],fontSize=20),
        width=40,
        height=40
    )
            
        
    lower_salary=base.mark_text(fontSize=35).encode(
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
        title=alt.TitleParams(['Minimum salary:'],fontSize=20),
        width=40,
        height=40
    )
        
    upper_salary=base.mark_text(fontSize=35).encode(
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
        title=alt.TitleParams(['Maximum salary:'],fontSize=20),
        width=40,
        height=40
    )
    
    
    #https://stackoverflow.com/questions/67997825/python-altair-generate-a-table-on-selection
    new_df=df_new.groupby(['s_no','Job Title','Salary Estimate','Avg Salary(K)','Company Name'])['Skill'].apply(','.join).reset_index()
    new_df.rename(columns = {'Skill':'skill_name'}, inplace = True)
    new_df=new_df.drop_duplicates(subset=['s_no'],keep="first")
    
    text_title=base.mark_text().properties(title=alt.TitleParams(text='Jobs in order of Average salary', align='left',fontSize=20))
    ranked_text = base.mark_text(fontSize=10,align='left').encode(
    y=alt.Y('rank:O',axis=None)
    ).transform_lookup(
        lookup='s_no',
        from_=alt.LookupData(data=new_df, key='s_no',
                          fields=['s_no','skill_name'])
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
        #groupby=["s_no"],
    ).transform_filter(
        'datum.rank < 30'
    )
        
    
    ind = ranked_text.encode(text='rank:O').properties(title=alt.TitleParams(text='Rank', align='left'))
    job_title = ranked_text.encode(text='job_title:N').properties(title=alt.TitleParams(text='Job Title', align='left'))
    company = ranked_text.encode(text='company:N').properties(title=alt.TitleParams(text='Company Name & Rating', align='left'))
    avg_s=ranked_text.encode(text='avg_sa:N').transform_calculate(
        avg_sa="'$'+round(datum.avg) + 'K'"
    ).properties(title=alt.TitleParams(text='Avg Salary', align='left'))
    salary = ranked_text.encode(text='salary:N').properties(title=alt.TitleParams(text='Salary Estimate', align='left'))
    skill = ranked_text.encode(text='skills:N').properties(title=alt.TitleParams(text='Skill', align='left'))
    row_text = alt.hconcat(ind,job_title,company,avg_s,salary,skill) # Combine data tables
    

    
    skills=(skill_chart.add_selection(brush)+skill_text).properties(
        title=alt.TitleParams('Top Skills in 2021',fontSize=20,
                              subtitle='Select one or more skills'),
        width=450,
        height=400
    )
    top=(alt.layer(error_bar,point_chart,top_industries_1,points).resolve_legend(
        color="independent"
    ).resolve_scale(
        size="independent",
        y = 'independent'
    ).properties(
        title=alt.TitleParams(text=['Salary difference ','with top industries'], align='center',fontSize=15),
        width=450,
        height=400
    )+top_industries_text).resolve_scale(
        size="independent",
        #y="independent"
    ).resolve_legend(
        color="independent"
    )
    
    hchart=alt.hconcat(skills,alt.vconcat(eligible,eligibility,avg_salary,upper_salary,lower_salary),top).resolve_scale(
        size="independent",
        y="independent",
        x="independent"
    )
    # Build chart
    table=alt.vconcat(
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

    st.write('Job reco charts')

    ####################################################################################################################
