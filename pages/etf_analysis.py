# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:17:16 2022
@author: Korey
"""
import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
import yfinance
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import time
from datetime import datetime
import os
from pathlib import Path

fig = None
a = None

dirname = os.path.dirname(os.path.dirname(__file__))
print(dirname)

# get current sp500 data
rel_path = Path(dirname + "/" + "batch/sp500/sp500pickle.pickle")
fileo = open(rel_path, 'rb')
datao = pickle.load(fileo)

# get current etf data
rel_path = Path(dirname + "/" + "batch/sp500/etfpickle.pickle")
etf_fileo = open(rel_path, 'rb')
etf_datao = pickle.load(etf_fileo)

# get initial stock data
initial_ticker_val = 'AAPL'
a = yfinance.Ticker(initial_ticker_val)


etf_analysis_layout = html.Div([

    # Navbar Content
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("ETF & Macro Analysis", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    #dbc.DropdownMenuItem("ETF & Macro Analysis", href="/etf_analysis"),
                    dbc.DropdownMenuItem("SP500 Distributions", href="/sp500_distributions"),
                    dbc.DropdownMenuItem("SP500 Summary Table", href="/sp500_analysis"),
                    dbc.DropdownMenuItem("Individual Equity Data", href="/index"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="Equity Trends",
        brand_href="#",
        color="primary",
        dark=True),

    # Page Content
    html.Div(id='etf_page_container', children=[
        dcc.Loading(id="ls-etf-loading-1",
                    children=[html.Div(id="ls-etf-loading-output-1",
                                       style={'position': 'absolute', 'z-index': '-1'})],
                    type="default"),
        html.H3(['Spyder Sector ETFs'], style={'color': 'gray'}),
        dcc.Interval(
            id="etf_load_interval",
            n_intervals=0,
            max_intervals=0,  # <-- only run once
            interval=1
        ),
        html.Div(id='etf-graph-container',
                 children=[
                 ]),
    ],
        style={'padding': '20px',
               #'background': 'rgb(17, 17, 17)',
               'height': '1500px'})
])


@callback(
    Output("ls-etf-loading-output-1", "children"),
    Output("etf-graph-container", "children"),
    Input(component_id="etf_load_interval", component_property="n_intervals"),
)
def update_etf_layout(n_intervals: int):

    # get etf figures by iterating through ticker info from script load
    fig_store = {}
    for t in etf_datao['data'].keys():
        #temp_dict = {'info':yinfo,'historical':yhist}
        #datao['data'][s] = temp_dict
        #df_close = tickers.tickers[t].history(period="1y")
        df_close = etf_datao['data'][t]['historical']
        fig_daily_close = px.line(df_close['Close'])
        fig_daily_close.update_layout(
            title=t,
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False
        )

        #df_holding = pd.DataFrame.from_dict(tickers.tickers[t].info['holdings'])
        df_holding = pd.DataFrame.from_dict(
            etf_datao['data'][t]['info']['holdings'])
        df_holding = df_holding.rename(
            columns={'holdingPercent': 'Holding Percent', 'symbol': 'ETF Symbol'})
        fig_etf_holdings = px.bar(df_holding, x='ETF Symbol', y='Holding Percent', text_auto=True)
        fig_etf_holdings.update_layout(
            title='Top Holdings',
            xaxis_title=None,
            yaxis_title=None,
        )

        fig_store[t] = {'daily_close': fig_daily_close,
                        'etf_holdings': fig_etf_holdings}

    etf_graph_div = html.Div([

        #etf_tickers_str = 'XLK XLE XLY XLF'
        html.Br(),
        html.Div([
            #html.P(['Temp']),
            #xlk graphs
            dcc.Graph(id='xlk_daily_close',
                      figure=fig_store['XLK']['daily_close'],
                      style={'height': 300}),
            dcc.Graph(id='xlk_holdings',
                      figure=fig_store['XLK']['etf_holdings'],
                      style={'height': 300}),

        ], style={'width': '47%',
                  'display': 'inline-block'}),

        html.Div([
            #xle graphs
            #html.P(['Temp']),
            dcc.Graph(id='xle_daily_close',
                      figure=fig_store['XLE']['daily_close'],
                      style={'height': 300}),
            dcc.Graph(id='xle_holdings',
                      figure=fig_store['XLE']['etf_holdings'],
                      style={'height': 300}),
        ], style={'width': '47%',
                  'display': 'inline-block'}),

        html.Div([
            #xly graphs
            #html.P(['Temp']),
            dcc.Graph(id='xly_daily_close',
                      figure=fig_store['XLY']['daily_close'],
                      style={'height': 300}),
            dcc.Graph(id='xly_holdings',
                      figure=fig_store['XLY']['etf_holdings'],
                      style={'height': 300}),
        ], style={'width': '47%',
                  'display': 'inline-block'}),

        html.Div([
                 #html.P(['Temp']),
                 dcc.Graph(id='xlf_daily_close',
                           figure=fig_store['XLF']['daily_close'],
                           style={'height': 300}),
                 dcc.Graph(id='xlf_holdings',
                           figure=fig_store['XLF']['etf_holdings'],
                           style={'height': 300}),
                 ], style={'width': '47%',
                           'display': 'inline-block'})

    ])

    loaded = True

    return loaded, etf_graph_div