import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
import yfinance
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import time
from datetime import datetime
import os
from pathlib import Path
from pages import equity_search,sp500_distributions,etf_analysis,jupyter_analysis
from pages import sp500_summary_table, wine_scrapper

#from pages import sp500_summary_table,sp500_distributions,etf_analysis,equity_search#,jupyter_analysis

''' Features To Add:    
    Biggest losers per day and how are they doing now - utilize the python now batch job feature.
    PEs over time - start in Jupyter but then integrate into web app
    Split pages into individual modules    
    
    sp500
        How much cash was added to or left the sp500
        The distribution of % changes for the week
    
    Macro
        Fed funds data
        Unemployment
        
    '''

# for deployment, pass app.server (which is the actual flask app) to WSGI etc
app = dash.Dash('Analytics Dash',
                external_stylesheets=[dbc.themes.LUX],
                suppress_callback_exceptions=True)

#server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/sp500_distributions':
             return sp500_distributions.sp500_distribution_layout
    if pathname == '/etf_analysis':
             return etf_analysis.etf_analysis_layout
    if pathname == '/jupyter_analysis':
            return jupyter_analysis.jupyter_layout  
    if pathname == '/sp500_analysis':
             return sp500_summary_table.sp500_analysis_layout
    if pathname == '/wine_data':
             return wine_scrapper.wine_layout       
    if pathname == '/index':
            return equity_search.equity_search_layout        
    else:
        return equity_search.equity_search_layout


# def display_page(pathname):          
#     if pathname == '/etf_analysis':
#         return etf_analysis.etf_analysis_layout 
#    # if pathname == '/jupyter_analysis':
#         #return jupyter_analysis.jupyter_layout    
#     if pathname == '/sp500_analysis':
#         return sp500_summary_table.sp500_analysis_layout        
#     #if pathname == '/sp500_distributions':
#         #return sp500_distributions.sp500_distribution_layout     
#     else:
#         return equity_search.equity_search_layout

if __name__ == '__main__':
    app.run_server(debug=True)
