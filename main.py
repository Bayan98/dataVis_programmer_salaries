import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
import numpy as np

countries = ["Russian Federation", "Romania", "Costa Rica", "Zimbabwe", "Bangladesh", "Bolivia", "Netherlands", "Austria", "Argentina", "Saudi Arabia", "Pakistan", "Kenya", "Spain", "Switzerland", "Colombia", "Czech Republic", "Italy", "Finland", "El Salvador", "Tajikistan", "Latvia", "Kyrgyzstan", "Portugal", "Uzbekistan", "Republic of Moldova", "Brazil", "Israel", "Canada", "Georgia", "Ethiopia", "Poland", "Taiwan", "Iran",
"Cuba", "Kazakhstan", "Singapore", "Australia", "Denmark", "United Arab Emirates", "United Kingdom", "Japan", "Belarus", "Iraq", "Ireland", "Turkmenistan", "Monaco", "Indonesia", "Philippines", "Sweden", "Greece", "Bulgaria", "India", "South Korea", "Nigeria", "Afghanistan", "Norway", "Ukraine", "United States", "Luxembourg", "Hong Kong (S.A.R.)", "Peru", "Slovakia", "China", "Chile", "Iceland", "Estonia", "Swaziland", "Honduras", "Mexico", "Viet Nam", "France", "Malaysia", "Mongolia", "New Zealand", "South Africa", "Sudan", "Belgium", "Morocco", "Albania", "Maldives", "Egypt", "Germany", "Turkey",
"Thailand"]
educations = ["I never completed any formal education", "Some college/university study without earning a degree", "Bachelor’s degree (B.A., B.S., B.Eng., etc.)", "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)", "Professional degree (JD, MD, etc.)", "Other doctoral degree (Ph.D., Ed.D., etc.)", "Associate degree (A.A., A.S., etc.)"]
employments = ["Independent contractor, freelancer, or self-employed", "Employed full-time", "Employed part-time"]
positions = ["Data or business analyst", "Data scientist or machine learning specialist", "Database administrator", "Developer, back-end", "Developer, desktop or enterprise applications", "Developer, embedded applications or devices", "Developer, front-end", "Developer, full-stack", "Developer, game or graphics", "Developer, mobile", "Developer, QA or test", "DevOps specialist", "Educator", "Engineer, data", "Engineer, site reliability", "Engineering manager", "Scientist", "System administrator"]
programmingLanguages = ["Assembly", "Bash/Shell/PowerShell", "C", "C++", "C#", "Go", "HTML/CSS", "Java", "JavaScript", "Kotlin", "Objective-C", "Perl", "PHP", "Python", "Ruby", "Rust", "Scala", "SQL", "Swift"]

countries.sort()

app = dash.Dash(__name__)

app.title = 'Visualization Tool'
app.layout = html.Div([
    html.H1(children="Tool For Analyzing Programmers Salaries"),
    html.H2(children="Customization"),

    html.H3(children="Select by which option you want to compare"),
    dcc.Dropdown(

        options=[
            {'label': 'by Country', 'value': 'Country'},
            {'label': 'by Education Level', 'value': 'EdLevel'},
            {'label': 'by Employment Status', 'value': 'Employment'},
            {'label': 'by Position', 'value': 'DevType'},
            {'label': 'by Programming Language', 'value': 'LanguageWorkedWith'}

        ],
        id='dropdownCompare',
        value='EdLevel',
        clearable=False
    ),

    html.H3(children="Select Countries"),
    dcc.Dropdown(
        options=[
            {'label': i, 'value': i}
            for i in countries
        ],
        id='dropdownCountries',
        value=['United States', 'South Korea', 'Russian Federation', 'United Kingdom'],
        multi=True
    ),
    
    html.H3(children="Select Education Levels"),
    dcc.Checklist(
        options=[
            {'label': i, 'value': i}
            for i in educations
        ],
        id='checklistEducation',
        value=["Bachelor’s degree (B.A., B.S., B.Eng., etc.)", "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)"],
        labelStyle={'display': 'table'}
    ),
    
    html.H3(children="Select Employment Type"),
    dcc.Checklist(
        options=[
            {'label': i, 'value': i}
            for i in employments
        ],
        id='checklistEmployment',
        value=["Employed full-time", "Independent contractor, freelancer, or self-employed"],
        labelStyle={'display': 'table'}
    ),

    html.H3(children="Select Positions"),
    dcc.Dropdown(
        options=[
            {'label': i, 'value': i}
            for i in positions
        ],
        id='dropdownPositions',
        value=["Developer, front-end", "Developer, back-end", "Developer, full-stack", "Data scientist or machine learning specialist", "Developer, mobile"],
        multi=True
    ),

    html.H3(children="Select Programming Languages"),
    dcc.Dropdown(
        options=[
            {'label': i, 'value': i}
            for i in programmingLanguages
        ],
        id='dropdownLanguages',
        value=["C++", "Python", "Java", "HTML/CSS", "JavaScript", "PHP", "SQL"],
        multi=True
    ),

    html.H3(children="Select Years of Coding Experience"),
    dcc.RangeSlider(
        id='rangeCode',
        min=0,
        max=31,
        step=1,
        marks = {
                0: "0",
                1: "1",
                2: "2",
                3: "3",
                4: "4",
                5: "5",
                10: "10",
                15: "15",
                20: "20",
                25: "25",
                30: "30",
                31: ">30"
                    },
        value=[4, 12]
    ),

    html.H3(children="Select Work Experience"),
    dcc.RangeSlider(
        id='rangeWork',
        min=0,
        max=31,
        step=1,
        marks = {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        10: "10",
        15: "15",
        20: "20",
        25: "25",
        30: "30",
        31: ">30"
            },
        value=[0, 5]
    ),

    html.H2(children="Data Visualization"),
    
    dcc.Graph(
        id='graph',
        style={'height': 600},
        ),
        
    html.H3(children="Average Values"),
    html.Table(
        id='table',
        children =
        [html.Tr(["", "Average Values"])] +
        [html.Tr([
            html.Td("1"),
            html.Td("asd")
        ])]
    )
])

data = pd.read_csv('assets/data/survey_results_public.csv')

data = data[["ConvertedComp", "Country", "DevType", "EdLevel", "Employment", "LanguageWorkedWith", "YearsCode", "YearsCodePro"]]

data = data[~data["ConvertedComp"].isin(["NaN"])]
data = data[data["Country"].isin(countries)]
data = data[data["EdLevel"].isin(educations)]
data = data[data["Employment"].isin(employments)]

def change_year(year):
    if type(year) is not str:
        return 1
    if "More" in year:
        year = 31
    elif "Less" in year:
        year = 0
    year = int(year)
    if year > 30:
        year = 31
    return year

@app.callback(
    Output(component_id='graph', component_property='figure'),
    Output(component_id='table', component_property='children'),
    Input(component_id='dropdownCompare', component_property='value'),
    Input(component_id='dropdownCountries', component_property='value'),
    Input(component_id='checklistEducation', component_property='value'),
    Input(component_id='checklistEmployment', component_property='value'),
    Input(component_id='dropdownPositions', component_property='value'),
    Input(component_id='dropdownLanguages', component_property='value'),
    Input(component_id='rangeCode', component_property='value'),
    Input(component_id='rangeWork', component_property='value'),
)
def update_graph(compare, countries, educations, employments, positions, languages, rangeCode, rangeWork):
    datas = []
    temp_x = []
    temp_y = []
    avg = {}
    for i in range(0, 500000, 2000):
        temp_x.append(i)
        temp_y.append(0)
    if compare == 'Country':
        for country in countries:
            datas.append({'x': temp_x.copy(), 'y': temp_y.copy(), 'type': 'scatter', 'name': country})
    if compare == 'EdLevel':
        for education in educations:
            datas.append({'x': temp_x.copy(), 'y': temp_y.copy(), 'type': 'scatter', 'name': education})
    if compare == 'Employment':
        for employment in employments:
            datas.append({'x': temp_x.copy(), 'y': temp_y.copy(), 'type': 'scatter', 'name': employment})
    if compare == 'DevType':
        for position in positions:
            datas.append({'x': temp_x.copy(), 'y': temp_y.copy(), 'type': 'scatter', 'name': position})
    if compare == 'LanguageWorkedWith':
        for language in languages:
            datas.append({'x': temp_x.copy(), 'y': temp_y.copy(), 'type': 'scatter', 'name': language})
            
    test = 0
    for index, row in data.iterrows():
        #check if this row is ok
        if row["Country"] not in countries:
            continue
        if row["EdLevel"] not in educations:
            continue
        if row["Employment"] not in employments:
            continue
        check = False
        if type(row["DevType"]) is str:
            for dev in row["DevType"].split(';'):
                if dev in positions:
                    check = True
                    break
            if not check:
                continue
        else:
            continue
        check = False
        if type(row["LanguageWorkedWith"]) is str:
            for language in row["LanguageWorkedWith"].split(';'):
                if language in languages:
                    check = True
                    break
            if not check:
                continue
        else:
            continue
        code = row["YearsCode"]
        code = change_year(code)
        work = row["YearsCodePro"]
        work = change_year(work)
        if code < rangeCode[0] or code > rangeCode[1]:
            continue
        if work < rangeWork[0] or work > rangeWork[1]:
            continue
        
        #update datas
        if compare == 'Country':
            for edit_data in datas:
                if edit_data['name'] == row["Country"]:
                    salary = int(row["ConvertedComp"])
                    if salary > 496000:
                        salary = 499000
                    edit_data['y'][salary//2000] += 1
        if compare == 'EdLevel':
            for edit_data in datas:
                if edit_data['name'] == row["EdLevel"]:
                    salary = int(row["ConvertedComp"])
                    if salary > 496000:
                        salary = 499000
                    edit_data['y'][salary//2000] += 1
        if compare == 'Employment':
            for edit_data in datas:
                if edit_data['name'] == row["Employment"]:
                    salary = int(row["ConvertedComp"])
                    if salary > 496000:
                        salary = 499000
                    edit_data['y'][salary//2000] += 1
        if compare == 'DevType':
            for edit_data in datas:
                if type(row["DevType"]) is str:
                    for dev in row["DevType"].split(';'):
                        if dev == edit_data['name']:
                            salary = int(row["ConvertedComp"])
                            if salary > 496000:
                                salary = 499000
                            edit_data['y'][salary//2000] += 1
        if compare == 'LanguageWorkedWith':
            for edit_data in datas:
                if type(row["LanguageWorkedWith"]) is str:
                    for dev in row["LanguageWorkedWith"].split(';'):
                        if dev == edit_data['name']:
                            salary = int(row["ConvertedComp"])
                            if salary > 496000:
                                salary = 499000
                            edit_data['y'][salary//2000] += 1

    
    #change for percents
    for edit_data in datas:
        amount = 0
        avg[edit_data['name']] = 0
        for y in edit_data['y']:
            amount += y;
        if amount == 0:
            continue
        for i in range(len(edit_data['y'])):
            avg[edit_data['name']] += edit_data['y'][i] * edit_data['x'][i]
            edit_data['y'][i] = edit_data['y'][i] / amount * 100
        edit_data['y'].pop()
        edit_data['x'].pop()
        avg[edit_data['name']] //= amount
    
    
    fig = {
        'data' : datas,
        'layout': {
                'xaxis': {'title':{'text':'Salary Amount in USD by Year'}},
                'yaxis': {'title':{'text':'Percent of People'}},
        }
    }
    
    child = []
    
    for key, value in avg.items():
        child.append(html.Tr([
            html.Td(key),
            html.Td(value)]))
        
    return fig, child


if __name__ == '__main__':
    app.run_server(debug=True)
