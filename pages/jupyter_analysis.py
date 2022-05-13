# -*- coding: utf-8 -*-
"""
Created on Fri May 13 10:54:49 2022

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
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import pandas as pd
import time
from datetime import datetime
import os
from pathlib import Path

jupyter_layout = html.Div(id='index-content', children=[
    
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Jupyter Analysis", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("ETF & Macro Analysis", href="/etf_analysis"),
                    dbc.DropdownMenuItem("SP500 Distributions", href="/sp500_distributions"),
                    dbc.DropdownMenuItem("SP500 Summary Table", href="/sp500_analysis"),
                    #dbc.DropdownMenuItem("JupyterAnalysis", href="/jupyter_analysis"),
                    dbc.DropdownMenuItem("Individual Equity Data", href="/index"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],        
        color="primary",
        dark=True,),
    
    html.Br(),
    html.Div(id='html_iframe',children=[html.H3('HELLO')]),
    dcc.Link('link to google', href='http://www.google.com',target='_blank'),
    html.A("Link to external site", href='https://plot.ly', target="_blank")
       
    
])
    #dbc.Table(id='ratio-table',
    #children=[html.Tr([html.Td(['Quick Ratio']))]),

# @callback(Output('html_iframe', 'children'),
#           Input('link', 'children'))
# def set_iframe(link): 
    
#     ifrm = html.Iframe(
#             src="html_output/home_price_correlation.html",
#             style={"height": "1067px", "width": "100%"},
#         )
    
#     return ifrm
