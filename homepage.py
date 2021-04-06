import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from plots import *
from wrangle import *
from dash.dependencies import Input, Output, State
from navbar import *

header = header()
nav = Navbar(page = 'tracker')

covid_df = pd.read_csv('covid_df.csv')
# for col in ['Confirmed', 'Active', 'Recovered', 'Deaths', 'Tests', 'Hospitalizations','Vaccinations']:
#     indicator_barplot(covid_df, count_col=col).to_csv('./data/' + col + '_df.csv')

def get_graph(class_name, **kwargs):
    return html.Div(
        className=class_name + ' plotz-container',
        children=[
            dcc.Graph(**kwargs),
            html.I(className='fa fa-expand'),
        ],
    )

def dropdown_options(col):
    return [{'label': name, 'value': name} for name in col]

about_app = html.Div(
    children=[
        html.Ul([
            html.Li(
                html.A('Our World in Data - COVID-19 Data Explorer', href="https://ourworldindata.org/explorers/coronavirus-data-explorer?zoomToSelection=true&time=2020-03-01..latest&country=USA~GBR~CAN~DEU~ITA~IND&region=World&pickerMetric=location&pickerSort=asc&Metric=Confirmed+cases&Interval=7-day+rolling+average&Align+outbreaks=false&Relative+to+Population=true", style={'font_family':'Arial'})
            ),
            html.Li(
                html.A('John Hopkins - Coronavirus Resource Center', href="https://coronavirus.jhu.edu/", style={'font_family':'Arial'})
            )
        ]),
        html.P('''
        All plots in this dashboard are interactive. Just hit play on the map, hover over bubbles, lines & points 
        for a more detailed look at the data.''',style = {'font_family':'Arial'}),
        html.P('''
        To filter the bottom middle timeline to a country, hover over a horizontal bar displayed
        in the rightmost bottom plot.
        ''',style = {'font_family':'Arial'}),
        html.P('''
        To switch between Confirmed, Active, Recovered, Deaths, Hospitalizations Vaccinations and Per Capita/Actual,
         use the radio buttons in the control panel, top right.''',style = {'font_family':'Arial'}),
        html.P('''
        The data used in this dashboard comes from John Hopkins University and Our World in Data.
        ''',style = {'font_family':'Arial'}),
        html.P('''
        Per Capita numbers are number / Population * 100,000 
        ''', style = {'font_family':'Arial'}),
        html.P('''
        To go back to the Policy Responses tab just click on the back arrow of the browser 
        ''', style = {'font_family':'Arial'}),
    ],
)

modal = html.Div([ # External row
    html.Div([ # External 12-column
        html.Div([ # Internal row
            html.Div([ #header2 pt1
                html.Div([], className = 'col-2'), # Blank 2 columns
                html.Div([
                    dbc.Button(
                        'View details',
                        id='open_modal',
                        outline=True,
                        color='secondary',
                    ),
                    dbc.Modal([
                        dbc.ModalHeader('COVID-19 Tracker'),
                        dbc.ModalBody(
                            children=[
                                about_app,
                            ]
                        ),
                        dbc.ModalFooter(
                            dbc.Button('Close',
                                        id='close',
                                        color='link',
                                        className='ml-auto')
                        ),
                    ],
                    id='modal',
                    size='sm'),
                ],
                style = {'margin-top' : '10px',
                        'margin-bottom' : '5px',
                        'text-align' : 'left',
                        'paddingLeft': 5}),
                html.Div([], className = 'col-2'), # Blank 2 columns
            ],
            className = 'col-4'), # header2 pt1
            html.Div([ # header2 pt2
                html.Div([
                    dbc.Row([
                        dcc.RadioItems(
                            id='count_category',
                            className='radio-group',
                            options=dropdown_options(['Confirmed', 'Active', 'Recovered', 'Deaths', 'Tests', 'Hospitalizations','Vaccinations']),
                            value='Confirmed',
                            labelStyle={'display': 'inline-block'}
                        ),
                        html.H5('  |  '),
                        dcc.RadioItems(
                            id='count_type',
                            className='radio-group',
                            options=[
                                {'label': 'Per Capita', 'value': 'per_capita'},
                                {'label': 'Actual', 'value': 'actual'}
                            ],
                            value='actual',
                            labelStyle={'display': 'inline-block'}
                        ),
                        dcc.Input(
                            id='country_input',
                            placeholder="Search...",
                            type='text',
                            debounce=True,
                        ),
                    ]),
                ],
                style = {'margin-top' : '10px',
                        'margin-bottom' : '5px',
                        'text-align' : 'right',
                        'paddingRight': 5})
            ],
            className = 'col-8'), # header2 pt 2
            # html.Div([], className = 'col-2') # Blank 2 columns
        ], className = 'row') # Internal row
    ],
    className = 'col-12',
    style = filterdiv_borderstyling) # External 12-column
    ], className = 'row sticky-top') # External row


body = html.Div([ # External row
    html.Div([], className = 'col-1'), # Blank 1 column
    html.Div([ # External 10-column
        html.Div([ # Map
            get_graph(
                class_name='div1',
                figure=get_map_plot(covid_df),
                id='map_graph',
                config=plot_config, 
            ),
        ],
        ),
        html.Div([ # Internal row
            html.Div([ # Line graph 1
                html.Div([
                    get_graph(
                        class_name='div3',
                        figure=get_country_timeseries(covid_df),
                        id='country_graph',
                        config=plot_config,
                    ),
                ]),
            ], className = 'col-4'),
            html.Div([ #Line graph 2
                html.Div([
                    get_graph(
                        class_name='div4',
                        figure=get_total_timeseries(covid_df),
                        id='total_graph',
                        config=plot_config,
                    ),
                ]),
            ], className = 'col-4'),
            html.Div([ #Raceplot
                html.Div([
                    get_graph(
                        class_name='div2',
                        figure=get_bar_raceplot(covid_df),
                        id='bar_race_graph',
                        config=plot_config,
                    ),
                ]),
            ], className = 'col-4')
        ], className = 'row') # Internal row
    ], className = 'col-10', style = externalgraph_colstyling), # External 10-column
    html.Div([], className = 'col-1'), # Blank 1 column
    ], className = 'row', style = externalgraph_colstyling) # External row


def Homepage():
    layout = html.Div([
        header,
#         nav,
        modal,
        body
    ])
    return layout
