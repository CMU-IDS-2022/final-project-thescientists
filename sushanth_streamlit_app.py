from urllib.parse import urlencode

import altair as alt
import en_core_web_sm
import pandas as pd
import streamlit as st
from PyPDF2 import PdfFileReader
from annotated_text import annotated_text
from vega_datasets import data
import requests
import json
import re

# Google API
api_key = "AIzaSyBOZHZGEENiTf07_MvnS3gQ3uyCFKzHg_U"
client_id = "0o4dtm0b55wk5o5b"
secret = "fKqeC4uG"


def get_emi_api_token():
    url = "https://auth.emsicloud.com/connect/token"

    payload = "client_id="+client_id+"&client_secret="+secret+"&grant_type=client_credentials&scope=emsi_open"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, data=payload, headers=headers)
    token = json.loads(response.text)['access_token']
    return token


@st.cache
def get_city_group_by_stats(data):
    gb = data.groupby(['Location'])
    city_groupby_data = gb.agg({'Avg Salary(K)': 'mean', 'Lower Salary': 'mean', 'Upper Salary': 'mean'})
    city_groupby_data.reset_index(inplace=True)
    return city_groupby_data


def extract_skills_from_document(jd):
    # token = get_emi_api_token()
    # jd = jd.replace('\n', " ").replace('\t', " ")
    # jd = re.sub(r'[^A-Za-z0-9 ]+', '', jd)
    #
    # print("JD: {}".format(jd))
    #
    # skills_from_doc_endpoint = "https://emsiservices.com/skills/versions/latest/extract"
    # text = jd
    # confidence_interval = "0.8"
    # payload = "{ \"text\": \"... " + text + " ...\", \"confidenceThreshold\": " + confidence_interval + " }"
    #
    # headers = {
    #     'authorization': "Bearer " + token,
    #     'content-type': "application/json"
    # }
    #
    # response = requests.request("POST", skills_from_doc_endpoint, data=payload.encode('utf-8'), headers=headers)
    #
    # skills_found_in_document_df = pd.DataFrame(pd.json_normalize(response.json()['data']));
    # skills_found_in_document_df = rename_columns(skills_found_in_document_df)
    #
    # skills_list = list(skills_found_in_document_df['skill_name'])

    skills_list = ['Predictive Modeling', 'Business Continuity Planning', 'Exploratory Data Analysis', 'Data Collection', 'Analytical Skills', 'Data Mining', 'Distributed Computing', 'Unstructured Data', 'Security Awareness', 'Data Architecture', 'Customer Retention', 'Phishing', 'Python (Programming Language)', 'Dashboard', 'Support Vector Machine', 'Data Science', 'D3.js', 'Machine Learning Algorithms', 'Machine Learning', 'Random Forest Algorithm', 'Financial Data', 'Gradient Boosting', 'Statistical Modeling', 'SQL (Programming Language)', 'Data Modeling', 'SAS (Software)', 'Query Languages', 'Budget Support', 'Data Visualization', 'Matplotlib', 'Apache Hive', 'Social Engineering', 'Computer Science', 'Big Data Analytics', 'Big Data', 'Forecasting', 'Data Warehousing', 'Apache Spark', 'Statistics', 'Microsoft Excel', 'R (Programming Language)', 'Mathematical Optimization']

    return skills_list


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
def load_data():
    data = pd.read_csv(
        "https://raw.githubusercontent.com/CMU-IDS-2022/final-project-thescientists/main/datasets/DataScientiestsSalaries2021.csv")
    return data


@st.cache
# file and code referenced from: https://gist.github.com/rogerallen/1583593
def get_state_code_dict():
    with open('states_to_codes.txt') as f:
        text_data = f.read()

    dictionary = json.loads(text_data)
    code_to_state = dict(map(reversed, dictionary.items()))
    return code_to_state


@st.cache
def get_state_fips():
    with open('state_to_fips.txt') as f:
        text_data = f.read()

    dictionary = json.loads(text_data)
    return dictionary


@st.cache
def get_skill_col_dict():
    with open('skillname_to_column.txt') as f:
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

    if salary_range is not None:
        labels &= df['Lower Salary'] >= (salary_range[0] / 1000)
        labels &= df['Upper Salary'] <= (salary_range[1] / 1000)

    if state is not None and state != 'All':
        labels &= df['Job Location'] == get_code_for_state(state, code_state_dict)

    if skills:

        # print(skills)
        # print(skill_to_col_dict)

        for skill in skills:
            labels &= df[skill_to_col_dict[skill]] == 1

    if industry and industry != 'All':
        labels &= df['Industry'] == industry

    return labels


def get_resume_text(file):
    pdfReader = PdfFileReader(uploaded_file)

    num_pages = pdfReader.numPages
    count = 0
    text = ""

    # Extract text from every page on the file
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count += 1
        text += pageObj.extractText()

    text = "".join(text.split())

    return text.lower()


add_selectbox = st.sidebar.selectbox("Select a view to explore:",
                                     ('US Data Science Jobs visualizations',
                                      'Industry and Company visualizations',
                                      'Job Recommendation Dashboard'))

dataset = load_data()
dataset = dataset.drop_duplicates()
dataset = dataset.drop(['index'], axis=1)

code_to_state_dict = get_state_code_dict()
skill_col_dict = get_skill_col_dict()
city_groupby_stats = get_city_group_by_stats(dataset)

states_plotting = alt.topo_feature(data.us_10m.url, 'states')
state_fips = get_state_fips()


def get_JD_keywords(jd):
    nlp = en_core_web_sm.load()
    doc = nlp(jd)
    key_words = [str(x).lower() for x in doc.ents]
    return key_words


def get_percentage_match(resume_text, key_words):
    total_key_words = len(key_words)
    matched = 0
    unmatched_keys_words = []
    for k in key_words:
        if str(k) in resume_text:
            matched += 1
        else:
            unmatched_keys_words.append(k)
    return (matched / total_key_words), unmatched_keys_words


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

    st.write(state)
    st.write(exp_salary_range)
    st.write(skills_selected)
    st.write(industry)

    st.write(filtered_data)

    st.markdown("""---""")

    st.markdown("**Locations of Data Science roles in {}**".format(state))

    #unique_loc_array = filtered_data['Location'].unique()
    loc_counts_df = filtered_data['Location'].value_counts().rename_axis('Location').reset_index(name='Jobs Available')
    # plotting_loc_df = pd.DataFrame(unique_loc_array, columns=['Location'])
    plotting_data = get_lat_long(loc_counts_df)
    plotting_data['Jobs Available'] = plotting_data['Jobs Available'].fillna(0).astype(int)

    plotting_data = plotting_data.merge(city_groupby_stats, on='Location', how='left')
    plotting_data[['Avg Salary(K)','Lower Salary','Upper Salary']] = 1000 * plotting_data[['Avg Salary(K)','Lower Salary','Upper Salary']]
    plotting_data = plotting_data.rename({'Avg Salary(K)': 'Average Salary'}, axis=1)
    st.write(plotting_data)

    # city_selector = alt.selection_single()

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
        tooltip = ['Location:N', 'Average Salary:Q', 'Lower Salary:Q', 'Upper Salary:Q']
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
    #
    # output_list = ['    |   '.join(map(str, job)) for job in jobs_list]

    select_job = st.selectbox('Select desired role to view job summary:', jobs_list_joined)
    selected_index = jobs_list_joined.index(select_job)

    # print("selected index: {}".format(selected_index))
    # print("selected index: {}".format(selected_index))
    sel_job_data = filtered_data.iloc[selected_index, :]
    # print(sel_job_data)

    st.markdown("""---""")

    cols = st.columns((1, 1))
    with cols[0]:
        data_display = sel_job_data['Company Name'].replace("\n", ", ").split(", ")
        st.markdown("**{}** (Glassdoor Rating: {}/5)".format(data_display[0], data_display[1]))
        st.markdown("**Headquarters:** {}".format(sel_job_data['Headquarters']))
        st.markdown("**Industry:** {}".format(sel_job_data['Industry']))
    with cols[1]:
        st.markdown("**Role:** {}".format(sel_job_data['Job Title']))
        #print("{}".format(str(sel_job_data['Salary Estimate'])))
        st.markdown("**Salary:** {}".format(str(sel_job_data['Salary Estimate']).replace("$", "\$")))
        st.markdown("**Location:** {}".format(sel_job_data['Location']))

    with st.expander("See Job Description"):
        st.write(sel_job_data['Job Description'])

    st.markdown("""---""")

    st.markdown("**Preferred Skills/Proficiencies by Recruiter according to Job Description:**")
    st.markdown(extract_skills_from_document(sel_job_data['Job Description']))

    st.markdown("""---""")

    uploaded_file = st.file_uploader("Upload your Resume to analyze match with Job Description:")

    if uploaded_file is not None:
        resume_text = get_resume_text(uploaded_file)
        print(resume_text)

        key_words = get_JD_keywords(sel_job_data['Job Description'])
        print(key_words)

        percent_match, suggested_key_words = get_percentage_match(resume_text, key_words)

        cols = st.columns((1, 0.1, 2))
        with cols[0]:
            st.metric("Resume Match Percentage:", str('{:.2f} %'.format(percent_match * 100)))
        with cols[2]:
            st.markdown(suggested_key_words)

    ####################################################################################################################
