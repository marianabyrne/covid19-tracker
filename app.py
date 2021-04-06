import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from plots import *
from wrangle import *
from dash.dependencies import Input, Output, State
from navbar import Navbar
# from policyresponse import *
from homepage import *



template = 'plotly_light'
default_layout = {
    'autosize': True,
    'xaxis': {'title': None},
    'yaxis': {'title': None},
    'margin': {'l': 40, 'r': 20, 't': 40, 'b': 10},
    'paper_bgcolor': '#B1B1B1', 
    'plot_bgcolor': '#B1B1B1', 
    'hovermode': 'x',
}

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.1/css/all.min.css',
]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED],)
server = app.server
app.config.suppress_callback_exceptions = True
app.index_string = open('index.html', 'r').read()

app.layout = html.Div([
#     dcc.Location(id='url', refresh = False),
    Homepage(),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == 'https://covid19-policy-responses.herokuapp.com/':
        return 'https://covid19-policy-responses.herokuapp.com/'
#     else:
#         return PolResponse()

@app.callback(
    Output('modal', 'is_open'),
    [Input('open_modal', 'n_clicks'), Input('close', 'n_clicks')],
    [State('modal', 'is_open')],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('country_input', 'value'),
    [
        Input('bar_race_graph', 'hoverData'),
    ])
def update_x_timeseries(hoverData):
    return hoverData['points'][0]['y'] if hoverData else ''

@app.callback(
    Output('map_graph', 'figure'),
    [
        Input('count_type', 'value'),
        Input('count_category', 'value'),
    ])
def update_map_plot(count_type, count_category):
    count_col = count_category if count_type == 'actual' else count_category + 'PerCapita'
    return get_map_plot(covid_df, count_col)


@app.callback(
    Output('bar_race_graph', 'figure'),
    [
        Input('count_type', 'value'),
        Input('count_category', 'value')
    ]) 
def update_bar_raceplot(count_type, count_category):
    count_col = count_category if count_type == 'actual' else count_category + 'PerCapita'
    return get_bar_raceplot(covid_df, count_col=count_category)


@app.callback(
    Output('country_graph', 'figure'),
    [
        Input('count_type', 'value'),
        Input('count_category', 'value'),
    ])
def update_bar_plot(count_type, count_category):
    count_col = count_category if count_type == 'actual' else count_category + 'PerCapita'
    return get_country_timeseries(covid_df, count_col)


@app.callback(
    Output('total_graph', 'figure'),
    [
        Input('country_input', 'value'),
        Input('count_type', 'value')
    ])
def update_x_timeseries(country_input, count_type):
    df = covid_df[covid_df['Country'] == country_input] \
        if country_input \
        else covid_df
    return get_total_timeseries(df, country=country_input, per_capita=count_type == 'per_capita')

## Policy response tab
# @app.callback(
#     Output('modal_policy', 'is_open'),
#     [Input('policy_button', 'n_clicks'), Input('close_policy', 'n_clicks')],
#     [State('modal_policy', 'is_open')],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open

# # To try and link sunburst to line plot
# @app.callback(
#     Output('count_policy_input', 'value'),
#     [
#         Input('sunburst', 'hoverData'),
#     ])
# def update_lineplot(hoverData):
#     return hoverData['points'][0]['y'] if hoverData else ''


# @app.callback(
#     Output('sunburst', 'figure'),
#     [
#         Input('policy', 'value'),
#     ])
# def update_sunburst(policy):
#     return get_sunburst(policy)

# @app.callback(
#     Output('trends_plot', 'figure'),
#     [
#         Input('country', 'value')
#     ])
# def update_mobility_trends(country):
#     return get_line_plot(trends, country_name = country)

if __name__ == '__main__':
    app.run_server(debug=True)
