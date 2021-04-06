import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from plots import *
from wrangle import *
from navbar import *
from homepage import get_graph, dropdown_options
header = header()
nav = Navbar(page = 'response')


trends = pd.read_csv('./data/mobility_trends.csv')
policy_response_df = pd.read_csv('./data/policy_responses.csv')
policy_response_df.drop(columns=policy_response_df.columns[0], inplace = True)
continents = pd.read_csv('./data/continents.csv')
continents.drop(columns=continents.columns[0], inplace = True)

modal_policy = html.Div([ # External row
    html.Div([ # External 12-column
        html.Div([ # Internal row
            html.Div([ #header2 pt1
                html.Div([], className = 'col-2'), # Blank 2 columns
                html.Div([
                    dbc.Button(
                        'View details',
                        id='policy_button',
                        outline=True,
                        color='secondary',
                    ),
                    dbc.Modal([
                        dbc.ModalHeader('Policy Responses to the COVID-19 Pandemic'),
                        dbc.ModalBody(
                            children=[
                                html.Div([
                                    html.Ul([
                                        html.Li(
                                            html.A('Our World in Data - Policy Responses to the Coronavirus Pandemic', href="https://ourworldindata.org/policy-responses-covid", style={'font_family':'Arial'})
                                        ),
                                    ]),
                                    html.P("""In this section of the dashboard it is possible to see the measures taken by each country regarding things like travel restrictions, the use of masks, stay-at-home requirements, and school and workplace closures. In order to see each of these individually just click on the dropdown menu. Additionaly, it is also possible to analyse the mobility trends around the world for the year 2020."""),
                                    html.P("""The data concerning the measures taken regarding the aforementioned policies is from 13th of March. Furthermore, when hovering over each country, it is possible to see the date when the country implemented the respective measure.""")
                                ]),
                            ]
                        ),
                        dbc.ModalFooter(
                            dbc.Button('Close',
                                        id='close_policy',
                                        color='link',
                                        className='ml-auto')
                        ),
                    ],
                    id='modal_policy',
                    size='sm'),
                ],
                style = {'margin-top' : '10px',
                        'margin-bottom' : '5px',
                        'text-align' : 'left',
                        'paddingLeft': 5}),
                html.Div([], className = 'col-2'), # Blank 2 columns
            ],
            className = 'col-4'), # header2 pt1
        ], className = 'row') # Internal row
    ],
    className = 'col-12',
    style = filterdiv_borderstyling) # External 12-column
],
className = 'row sticky-top') # External row




body_policy = html.Div([ # External row
    html.Div([], className = 'col-1'), # Blank 1 column
    html.Div([ # External 10-column
        html.Div([ # Internal row
            html.Div([ # Sunburst
                html.P("""Policy Response"""),
                dcc.Dropdown(
                    id='policy',
                    className='dropdown',
                    options=dropdown_options(['Stay-at-Home Requirements', 'Use of Masks', 'International Travel Controls', 'School Closures', 'Workplace Closures']),
                    value='Stay-at-Home Requirements',
                ),
                get_graph(
                    class_name='',
                    figure=get_sunburst(),
                    id='sunburst',
                    config=plot_config, 
                ),
            ], className = 'col-6'),
            html.Div([ #Line plot trends
                html.P("""Mobility Trends"""),
                html.Div([
                    # html.P('Search: '),
                    dcc.Input(
                        id='country',
                        placeholder="World",
                        type='text',
                        debounce=True,
                    )
                ]),
                get_graph(
                    class_name='',
                    figure=get_line_plot(trends),
                    id='trends_plot',
                    config=plot_config, 
                ),
            ], className = 'col-6'),
        ], className = 'row') # Internal row
    ], className = 'col-10', style = externalgraph_colstyling), # External 10-column
    html.Div([], className = 'col-1'), # Blank 1 column
], className = 'row', style = externalgraph_colstyling) # External row

def PolResponse():
    layout = html.Div([
        header,
        nav,
        modal_policy,
        body_policy
    ])
    return layout
