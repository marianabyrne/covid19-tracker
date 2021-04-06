import os
import pandas as pd
import numpy as np
import plotly
import plotly.io as pio
import plotly.graph_objects as go
from plotly import express as px
from wrangle import *
plot_config = {
    'modeBarButtonsToRemove': [
        'lasso2d',
        'hoverClosestCartesian',
        'hoverCompareCartesian',
        'toImage',
        'sendDataToCloud',
        'hoverClosestGl2d',
        'hoverClosestPie',
        'toggleHover',
        'resetViews',
        'toggleSpikelines',
        'resetViewMapbox'
    ]
}

plot_palette = [
    '#185d6a',
    '#385e4c',
    '#597043',
    '#7a8339',
    '#9b9530',
    '#bca727',
    '#ddb91e',
    '#ffcc14',
]
# Plotly mapbox public token
mapbox_token = "pk.eyJ1IjoicjIwMTY3MjciLCJhIjoiY2s1Y2N4N2hoMDBrNzNtczBjN3M4d3N4diJ9.OrgK7MnbQyOJIu6d60j_iQ"
mapbox_cofig = dict(accesstoken=mapbox_token, style='light')

bggolor = '#24252A'
# bggolor ='#FFFFFF'
default_layout = {
    'font_family': 'Arial Black',
    'font_color':'#24252A',
    'margin': {'r': 5, 't': 20, 'l': 5, 'b': 30},
    'paper_bgcolor': 'rgb(221, 237, 234)',#'rgb(62, 64, 76)',
    'plot_bgcolor':'rgb(221, 237, 234)',
    'xaxis':{'autorange':True},
    'yaxis':{'autorange':True}
}

plot_threshold = 35
empty_plot = px.line(template='plotly_dark')

def get_default_color(count_col='Confirmed'):
    if count_col == 'Confirmed': return '#71489B'
    if count_col == 'Active': return '#E3D344'
    if count_col == 'Recovered': return '#239B56'
    if count_col == 'Deaths': return '#861909'
    if count_col == 'Tests': return '#1B30B2'
    if count_col == 'Vaccinations': return '#F7DC6F'
    if count_col == 'Hospitalizations': return '#DB5400'

def get_map_plot(covid_df, count_col='Confirmed'):
    df = covid_df[covid_df[count_col]>0].copy()
    df.Date = pd.to_datetime(df.Date)
    values = df['logCumConf' if count_col == 'Confirmed' else count_col]
    fig = px.scatter_mapbox(
        mapbox_style='carto-darkmatter',
        lat=df['Latitude'],
        lon=df['Longitude'],
        hover_name=df['Description'],
        size=values,
        opacity=0.5,
        size_max=50,
        zoom=1,
        animation_frame=df['Date'].dt.strftime('%d/%m/%y'),
        center=go.layout.mapbox.Center(lat=14, lon=21),
        color_discrete_sequence=[get_default_color(count_col)]
        )

    if mapbox_token:
        fig.update_layout(mapbox=mapbox_cofig)

    fig.update_layout(
        **default_layout,
    )
    fig.update_traces(
        marker=go.scattermapbox.Marker(
            color='rgb(255, 0, 0)',
            opacity=0.7,
            sizeref=.5,
        ),
        selector=dict(geo='geo')
    )
    return fig

def get_total_timeseries(covid_df, country=None, per_capita=False):
    title = country if country else 'All Countries'
    covid_df = covid_df.assign(Date=covid_df['Date'].astype(np.datetime64))
    suffix = 'PerCapita' if per_capita else ''
    df = covid_df.groupby(['Date']).sum() \
        .reset_index() \
        .melt(id_vars='Date',
              value_vars=[
                  'Confirmed' + suffix,
                  'Recovered' + suffix,
                  'Active' + suffix,
                  'Deaths' + suffix,
                  'Tests' + suffix,
                  'Vaccinations' + suffix,
                  'Hospitalizations' + suffix
              ]) \
        .sort_values('Date')
    fig = px.line(
        df,
        x='Date',
        y='value',
        labels={
            'Date': 'Date',
            'value': 'Count',
        },
        color='variable',
        line_shape='spline',
        render_mode='svg',
        title=title,
        template='plotly_dark',
        color_discrete_sequence=plot_palette,
    )
    fig.update_layout(
        hovermode='x',
        **default_layout,
        width=500,
    )
    return fig

def get_country_timeseries(covid_df, count_col='Confirmed'):
    last_df = covid_df[covid_df['Date'] == covid_df['Date'].max()]
    top_countries = last_df \
        .nlargest(plot_threshold, count_col) \
        .reset_index()['Country'].unique()

    df = covid_df[covid_df['Country'].isin(top_countries)] \
        .groupby(['Date', 'Country']) \
        .sum().reset_index() \
        .sort_values(['Date', 'Country'])

    fig = px.line(
        x=df['Date'],
        y=df[count_col],
        color=df['Country'],
        labels={
            'y': count_col,
            'x': 'Date',
        },
        hover_name=df['Country'],
        line_shape='spline',
        render_mode='svg',
        template='plotly_dark',
        color_discrete_sequence=plot_palette,
    )
    fig.update_layout(
        hovermode='x',
        legend_title='',
        **default_layout,
        width=500,
    )
    return fig


def get_bar_raceplot(covid_df, count_col='Confirmed'):
    if count_col == 'Vaccinations':
        dict_keys=['one','two','three','four','five', 'six']
    else:
        dict_keys=['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen',
           'fourteen','fifteen']
    bar_df = pd.read_csv('./data/' + count_col + '_df.csv')
    years=[date for date in bar_df.Month.unique()]
    n_frame={}
    for y, d in zip(years, dict_keys):
        dataframe=bar_df[bar_df['Month']==y]
        dataframe=dataframe.sort_values(by=['Month', count_col])
        n_frame[d]=dataframe
    fig = go.Figure(
        data=[
            go.Bar(
            x=n_frame['one'][count_col], y=n_frame['one']['Country'],orientation='h',
            text=n_frame['one'][count_col], texttemplate='%{text:.3s}',
            textfont={'size':15}, textposition='inside', insidetextanchor='middle',
            width=0.9)
        ],
        layout=go.Layout(
            xaxis=dict(range=[0, bar_df[bar_df['Month']==bar_df['Month'].values[0]][count_col].max()], autorange=False),
            title=dict(text=count_col+': '+str(bar_df['Month'].values[0]),font=dict(size=20),x=0.5,xanchor='center'),
            # Add button
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                            method="animate",
                            args = [None, {"frame": {"duration": 500, "redraw": True},
                                    "fromcurrent": True, "transition": {"duration": 300,
                                                                        "easing": "quadratic-in-out"}}]),
                        dict(label="Pause",
                            method="animate",
                            args = [[None], {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}])
                ],
                # xanchor = 'left',
                yanchor = 'bottom'
            )],
        ),
        frames=[
                go.Frame(
                    data=[
                            go.Bar(x=value[count_col], y=value['Country'],
                            orientation='h',text=value[count_col])
                        ],
                    layout=go.Layout(
                            xaxis=dict(range=[0, value[count_col].max()], autorange=False),
                            title=dict(text=count_col+': '+str(value['Month'].values[0]),
                            font=dict(size=20))
                        )
                )
            for key, value in n_frame.items()
        ]
    )
    fig.update_layout(
        **default_layout,
        width=500
    )
    return fig


def get_sunburst(policy = 'Stay-at-Home Requirements'):
    sunburst_data = pd.read_csv('./data/'+ policy+'.csv')
    fig = px.sunburst(sunburst_data, path=[policy, 'continent', 'Entity'], hover_data=['Day'])
    fig.update_layout(
        **default_layout,
        width=500
    )
    return fig

def get_line_plot(df, country_name = 'World'):
    fig = px.line(df[df['Entity']==country_name], x="Day", y=["retail_and_recreation", "grocery_and_pharmacy", "residential", "transit_stations", "parks", "workplaces"])
    fig.update_layout(
        **default_layout,
        width=500
    )
    return fig
