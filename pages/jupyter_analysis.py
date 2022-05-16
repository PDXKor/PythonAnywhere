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
                    dbc.DropdownMenuItem("Individual Equity Data", href="/index"),
                    #dbc.DropdownMenuItem("Jupyter Analysis", href="/jupyter_analysis"),
                    dbc.DropdownMenuItem("Wine Ratings by Price", href="/wine_data"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],        
        color="primary",
        dark=True,),
    
    html.Br(),
    #html.Div(id='html_iframe', children=[html.H3('HELLO')]),
    #dcc.Link('link to google', href='http://www.google.com', target='_blank'),
    #html.A("Link to external site", href='https://plot.ly', target="_blank"),

    dbc.Table(children=[
        html.Tr([
            html.Td(
                dcc.Link('Home Price Correlation', 
                         href='https://kmstaffo.pythonanywhere.com/static/jupyter_nb/home_price_correlation.html', 
                         target='_blank'),
                style={'width':'30%',
                       'border':'none'}),
            html.Td('Using data from the Fred to determine if a correlation exists between various pieces of macro economic data, like unemployment rate, and housing prices.')
            ],style={'border':'.5px solid whitesmoke'}
        ),
        html.Tr([
            html.Td(
                dcc.Link('S&P 500 PE Average', 
                         href='https://kmstaffo.pythonanywhere.com/static/jupyter_nb/SP500_pe_history.html', 
                         target='_blank'),
                style={'width':'30%',
                       'border':'none'}),
            html.Td('Using data from the alphavantage and yfinance to determine the historical PE of the S&P 500.')
            ],style={'border':'.5px solid whitesmoke'}
        ),
        html.Tr([
            html.Td(
                dcc.Link('Income Statement Analysis', 
                         href='https://kmstaffo.pythonanywhere.com/static/jupyter_nb/income_statement_analysis.html', 
                         target='_blank'),
                style={'width':'30%',
                       'border':'none'}),
            html.Td('Using data from the alphavantage and yfinance try - attempt to determine a pattern between changes in income sheet items like net income and EBITDA and the corresponding three month stock change.')
            ],style={'border':'.5px solid whitesmoke'}
        ),
        html.Tr([
            html.Td(
                dcc.Link('Advanced Python', 
                         href='https://kmstaffo.pythonanywhere.com/static/jupyter_nb/advanced_python.html', 
                         target='_blank'),
                style={'width':'30%',
                       'border':'none'}),
            html.Td('Just a refresher on some advanced python topics.')
            ],style={'border':'.5px solid whitesmoke'}
        ),
        # html.Tr([
        #     html.Td(
        #         dcc.Link('Home Price Correlation', 
        #                  href='https://kmstaffo.pythonanywhere.com/static/jupyter_nb/home_price_correlation.html', 
        #                  target='_blank'),
        #         style={'width':'30%',
        #                'border':'none'}),
        #     html.Td('Using data from the Fred to determine if a correlation exists between various pieces of macro economic data, like unemployment rate, and housing prices.')
        #     ],style={'border':'.5px solid whitesmoke'}
        # ),
        # html.Tr([
        #     html.Td(
        #         dcc.Link('Home Price Correlation', 
        #                  href='https://kmstaffo.pythonanywhere.com/static/jupyter_nb/home_price_correlation.html', 
        #                  target='_blank'),
        #         style={'width':'30%',
        #                'border':'none'}),
        #     html.Td('Using data from the Fred to determine if a correlation exists between various pieces of macro economic data, like unemployment rate, and housing prices.')
        #     ],style={'border':'.5px solid whitesmoke'}
        # ),
        
        
        ],
        bordered=False,
        striped=False,
        style={'margin-left':'5%',
               'margin-top':'20px',
               'border':'.5px solid whitesmoke',
               'width':'70%'})

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
