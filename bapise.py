import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from guide_recommendation import recommend_guides

# Load the Excel data into the 'electives' DataFrame
electives = pd.read_excel("new_oe_pe.xlsx")

# Define parent-child relationships for 'electives'
parent_technology2 = {
    'Business Analytics with Python': 'Data Science/Analytics',
    'Block chain Technology and Applications': 'Blockchain',
    'Big Data Analytics': 'Data Science/Analytics',
    'Ethical Hacking': 'Cybersecurity',
    'Machine Learning': 'ML',
    'Natural Language Processing': 'NLP',
    'Cloud Computing': 'Cloud Computing',
    'Consumer electronics': 'DEV',
    'Cyber Security & Digital Forensics': 'Cybersecurity',
    'Data Analytics': 'Data Science/Analytics',
    'Human Machine Interaction': 'UX',
    'Software testing': 'DEV',
    'UED': 'UX',
}

# Map the subjects to parent technologies for 'electives'
electives['Parent2'] = electives['Subject'].map(parent_technology2)
electives['Parent2'] = electives['Parent2'].fillna('all')

# Sample data for charts (already defined in your existing code)
data = {
    'Domain': ['AIML', 'NLP', 'Computer vision', 'Deep Learning', 'Data Science/Analytics', 'Cloud Computing',
               'Generative AI', 'Image and video processing', 'Blockchain', 'Cybersecurity', 'UX', 'DEV'],
    'total row': [53, 35, 26, 28, 43, 23, 12, 28, 3, 7, 18, 21]
}

df = pd.DataFrame(data)

# Calculate total projects (already defined in your existing code)
df['num_projects'] = df['total row']

# Define a dictionary mapping each domain to its parent technology (already defined in your existing code)
parent_technology = {
    'AIML': 'AI/ML',
    'NLP': 'AI/ML',
    'Deep Learning': 'AI/ML',
    'Computer vision': 'AI/ML',
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







# Sample data for project details (already defined in your existing code)
project_data = pd.read_excel("./output (1).xlsx")

df_details = pd.DataFrame(project_data)

# Convert 'Domain' column to lowercase (already defined in your existing code)
df_details['Domain'] = df_details['Domain'].str.lower()


# last update-------------------------


mini_csv = pd.read_csv("./cleaned_mini_project_data.csv")
mini = mini_csv['Domain1'].value_counts().reset_index()
mini.columns = ['Domain', 'Num_projects']
mini_dict = dict(zip(mini['Domain'], mini['Num_projects']))
df_dict = dict(zip(df['Domain'], df['num_projects']))



parent_technology = {
    'AIML': 'AI/ML',
    'NLP': 'AI/ML',
    'Deep Learning': 'AI/ML',
    'Computer vision': 'AI/ML',
    'Cybersecurity': 'Cybersecurity',
    'Data Science/Analytics': 'Data Science/Analytics',
    'UX': 'UX',
    'DEV': 'DEV'
}

# Add a new column for parent technology
mini['Parent Technology'] = mini['Domain'].map(parent_technology)




# Combine the dictionaries
combined_dict = {}
all_domains = set(mini_dict.keys()) | set(df_dict.keys())
for domain in all_domains:
    combined_dict.setdefault('Domain', []).append(domain)
    combined_dict.setdefault('Mini', []).append(mini_dict.get(domain, 0))
    combined_dict.setdefault('Major', []).append(df_dict.get(domain, 0))

# Calculate the 'Total' column
combined_dict['Total'] = [mini + major for mini, major in zip(combined_dict['Mini'], combined_dict['Major'])]

# Create the combined DataFrame
combined = pd.DataFrame(combined_dict)




#-------------------------






# Create the Dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
# Define the layout of the app
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Projects', value='tab-1'),
        dcc.Tab(label='Electives', value='tab-3'),  # Added a new tab for Electives
        dcc.Tab(label='OE/PE Recommendations', value='tab-2'),
        dcc.Tab(label='Guide Recommendation', value='tab-4')
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
        ),
        html.Hr(),  # Horizontal line
        dcc.Graph(
            id='scatter-plot',
            figure=px.scatter(mini, x='Domain', y='Num_projects', title='Number of Projects vs. Domain',
                            labels={'Num_projects': 'Number of Projects', 'Domain': 'Domain'})
        ),
        dcc.Graph(
            id='treemap-2',
            figure=px.treemap(mini, path=['Parent Technology', 'Domain'], values='Num_projects',
                              title='Hierarchical Distribution of Projects by Domain',
                              color='Num_projects', hover_data=['Num_projects'],
                              color_continuous_scale='tealgrn')
        ),
        html.Hr(),  # Horizontal line
        dcc.Graph(
            id='bar-chart-2',
            figure=px.bar(combined, x='Domain', y=['Mini', 'Major'],
                          title='Number of Mini and Major Projects per Domain',
                          labels={'value': 'Number of Projects', 'variable': 'Project Type'}, barmode='group')
        ),
        ],
            id='tab-1-content'
        )
    elif tab == 'tab-2':
        return html.Div([
            html.Label('Select a domain:', style={'marginBottom': '10px'}),
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
                style={'width': '300px', 'marginBottom': '20px'}
            ),
            html.Div(id='output-table',
                     style={'backgroundColor': 'white', 'padding': '10px', 'border': '1px solid #ddd'})
        ],
            id='tab-2-content'
        )
    elif tab == 'tab-3':  # Added tab for Electives
        return html.Div([
            html.H1("OE and PE analysis"),
            dcc.Graph(
                id='electives-bar',
                figure=px.bar(electives, x='Subject', y='students', title='Number of Students Enrolled in Each Subject')
            ),
            dcc.Graph(
                id='electives-treemap',
                figure=px.treemap(electives, path=['Parent2', 'Subject'], values='students',
                                  hover_data=['Subject'], title='Technology Treemap Visualization')
            ),
            dcc.Graph(
                id='electives-sunburst',
                figure=px.sunburst(electives, path=['gParent', 'Subject'], values='students',
                                   title='Hierarchical Structure of Subjects')
            )

        ],
            id='tab-3-content'
        )
    elif tab == 'tab-4':
        return html.Div([
            html.H1("Guide Recommendation"),
            html.Label('Enter Project Title:',
                       style={'marginBottom': '10px', 'fontSize': '20px', 'fontWeight': 'semibold'}),
            dcc.Input(id='project-title', type='text',
                      style={'width': '300px', 'margin': '40px', 'padding': '10px', 'border': '1px solid #ddd',
                             'borderRadius': '5px'}),
            html.Button('Submit', id='submit-title', n_clicks=0,
                        style={'padding': '10px', 'border': '1px solid #ddd', 'borderRadius': '5px',
                               'backgroundColor': '#007bff', 'color': 'white'}),
            html.Div(id='output-guide', style={'background-color': 'white', 'padding': '10px', })
        ],
            id='tab-4-content',
            style={'padding': '30px'}
        )


# Define callback to update the table based on the selected domain (already defined in your existing code)
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
                            html.Th('Recommended PE and OE', style={'text-align': 'left'})
                        ]
                    )
                ]
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(filtered_data['Domain'].iloc[i],
                                    style={'border': '1px solid #ddd', 'padding': '8px'}),
                            html.Td(filtered_data['Project Title'].iloc[i],
                                    style={'border': '1px solid #ddd', 'padding': '8px'}),
                            html.Td(filtered_data['Recommended Subjects'].iloc[i],
                                    style={'border': '1px solid #ddd', 'padding': '8px'})
                        ]
                    ) for i in range(len(filtered_data))
                ]
            )
        ],
        style={'border-collapse': 'collapse', 'width': '100%'}
    )
    return table


# Define callback to update the guide recommendation based on the project title
@app.callback(
    Output('output-guide', 'children'),
    [Input('submit-title', 'n_clicks')],
    [dash.dependencies.State('project-title', 'value')]
)
def update_guide(n_clicks, project_title):
    if n_clicks > 0:
        recommended_guides = recommend_guides(project_title)
        print('-------------------------------------------------------------------------------')
        print(recommended_guides)
        # Display the recommended/ guides table with similarity scores
        return html.Div([
            html.P(f"Project Title: {project_title}", style={'fontSize': '20px', 'fontWeight': 'semibold'}),
            html.H3("Guides Recommended for Project:", style={'marginBottom': '10px'}),
            html.Table([
                html.Thead([
                    html.Tr([html.Th("Guide"), html.Th("Similarity Score")],
                            style={'border': '1px solid #ddd', 'padding': '8px'})
                ]),
                html.Tbody([
                    html.Tr([html.Td(recommended_guides['Guide'].iloc[i], style={
                        'border': '1px solid #ddd', 'paddingLeft': '30px',
                    }), html.Td(recommended_guides['Similarity Score'].iloc[i], style={
                        'border': '1px solid #ddd', 'paddingLeft': '30px',
                    }), ], style={'border': '1px solid #ddd', 'padding': '8px'}) for i in range(len(recommended_guides))
                ])
            ],
                style={'borderCollapse': 'collapse', 'width': '100%', 'border': '1px solid #ddd', 'padding': '8px'}
            )

        ])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
