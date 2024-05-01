import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


# Sample data for charts
data = {
    'Domain': ['AIML', 'NLP', 'Computer vision', 'Deep Learning', 'Data Science/Analytics', 'Cloud Computing',
               'Generative AI', 'Image and video processing', 'Blockchain', 'Cybersecurity', 'UX', 'DEV'],
    'total row': [53, 35, 26, 28, 43, 23, 12, 28, 3, 7, 18, 21]
}

df = pd.DataFrame(data)

# Calculate total projects
df['num_projects'] = df['total row']

# Define a dictionary mapping each domain to its parent technology
parent_technology = {
    'AIML': 'AI/ML',
    'NLP': 'AI/ML',
    'Deep Learning': 'AI/ML',
    'Computer vision': 'Image Processing',
    'Image and video processing': 'Image Processing',
    'Blockchain': 'Blockchain',
    'Cybersecurity': 'Cybersecurity',
    'Cloud Computing': 'Cloud Computing',
    'Generative AI': 'AI/ML',
    'Data Science/Analytics': 'Data Science/Analytics',
    'UX': 'UX',
    'DEV': 'DEV'
}

df['Parent Technology'] = df['Domain'].map(parent_technology)

# Sample data for project details
project_data = pd.read_excel("./output.xlsx")

df_details = pd.DataFrame(project_data)

# Convert 'Domain' column to lowercase
df_details['Domain'] = df_details['Domain'].str.lower()

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Charts', value='tab-1'),
        dcc.Tab(label='Project Details', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

# Define callback to update the tab content
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H1("Project Distribution by Domain"),
            dcc.Graph(
                id='bar-chart',
                figure=px.bar(df, x='Domain', y='num_projects', title='Number of Projects per Domain')
            ),
            dcc.Graph(
                id='pie-chart',
                figure=px.pie(df, names='Domain', values='num_projects', title='Distribution of Projects by Domain')
            ),
            dcc.Graph(
                id='treemap',
                figure=px.treemap(df, path=['Parent Technology', 'Domain'], values='num_projects',
                                  title='Hierarchical Distribution of Projects by Domain')
            )
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Label('Select a domain:', style={'margin-bottom': '10px'}),
            dcc.Dropdown(
                id='domain-dropdown',
                options=[
                    {'label': 'AIML', 'value': 'aiml'},
                    {'label': 'NLP', 'value': 'nlp'},
                    {'label': 'Computer Vision', 'value': 'computer vision'},
                    {'label': 'Deep Learning', 'value': 'deep learning'},
                    {'label': 'Data Science/Analytics', 'value': 'data science/analytics'},
                    {'label': 'Cloud Computing', 'value': 'cloud computing'},
                    {'label': 'Generative AI', 'value': 'generative ai'},
                    {'label': 'Image and Video Processing', 'value': 'image and video processing'},
                    {'label': 'Blockchain', 'value': 'blockchain'},
                    {'label': 'Cybersecurity', 'value': 'cybersecurity'},
                    {'label': 'UX', 'value': 'ux'},
                    {'label': 'DEV', 'value': 'dev'}
                ],
                value='aiml',
                style={'width': '300px', 'margin-bottom': '20px'}
            ),
            html.Div(id='output-table', style={'background-color': 'white', 'padding': '10px', 'border': '1px solid #ddd'})
        ])

# Define callback to update the table based on the selected domain
@app.callback(
    Output('output-table', 'children'),
    [Input('domain-dropdown', 'value')]
)
def update_table(selected_domain):
    filtered_data = df_details[df_details['Domain'].str.contains(selected_domain)]
    table = html.Table(
        [
            html.Thead(
                [
                    html.Tr(
                        [
                            html.Th('Domain', style={'text-align': 'left'}),
                            html.Th('Project Title', style={'text-align': 'left'}),
                            html.Th('Recommended PE', style={'text-align': 'left'})
                        ]
                    )
                ]
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(filtered_data['Domain'].iloc[i], style={'border': '1px solid #ddd', 'padding': '8px'}),
                            html.Td(filtered_data['Project Title'].iloc[i], style={'border': '1px solid #ddd', 'padding': '8px'}),
                            html.Td(filtered_data['Recommended Subjects'].iloc[i], style={'border': '1px solid #ddd', 'padding': '8px'})
                        ]
                    ) for i in range(len(filtered_data))
                ]
            )
        ],
        style={'border-collapse': 'collapse', 'width': '100%'}
    )
    return table


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
