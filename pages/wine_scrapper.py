# -*- coding: utf-8 -*-
"""
Created on Sun May 15 16:38:55 2022

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

dirname = os.path.dirname(os.path.dirname(__file__))
#print(dirname)

# # get current sp500 data
rel_path = Path(dirname + "/" + "pages/oregon_red_list.pkl")
#print(rel_path)

df = pd.read_pickle(rel_path)

df['JS'] = pd.to_numeric(df['JS'])
df['WS'] = pd.to_numeric(df['WS'])
df['WE'] = pd.to_numeric(df['WE'])
df['wine_price'] = pd.to_numeric(df['wine_price'])

df = df[df['wine_price']<300]

fig_js = px.scatter(df,x='wine_price',y='JS',hover_name='wine_name',color='origin')
fig_js.update_xaxes(title_text='Price')
fig_js.update_yaxes(title_text='Rating')

fig_we = px.scatter(df,x='wine_price',y='WE',hover_name='wine_name',color='origin')
fig_we.update_xaxes(title_text='Price')
fig_we.update_yaxes(title_text='Rating')

fig_ws = px.scatter(df,x='wine_price',y='WS',hover_name='wine_name',color='origin')
fig_we.update_xaxes(title_text='Price')
fig_ws.update_yaxes(title_text='Rating')


wine_layout = html.Div([
    
    # Navbar Content
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("SP500 Distributions", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("ETF & Macro Analysis", href="/etf_analysis"),
                    #dbc.DropdownMenuItem("SP500 Distributions", href="/sp500_distributions"),
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
    html.Br(),
    html.Br(),    
    html.Div([    
     html.H1('Wine Ratings by Cost'),
     html.Br(),        
     html.H3('James Suckling'),
     dcc.Graph(id='JS_wine_ranking',
              figure=fig_js,
              style={'height':'600px'}),    
     html.H3('Wine Enthusiast'),
     dcc.Graph(id='WE_wine_ranking',
              figure=fig_we,
              style={'height':'600px'}),    
     html.H3('Wine Spectator'),
     dcc.Graph(id='WS_wine_ranking',
              figure=fig_ws,
              style={'height':'600px'}),    
    ],
        style={'margin-left':'20px'})
    
    ])

























