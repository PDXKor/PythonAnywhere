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

sp500_analysis_layout = html.Div([    
    # Navbar Content
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("SP500 Summary Table", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("ETF & Macro Analysis", href="/etf_analysis"),
                    dbc.DropdownMenuItem("SP500 Distributions", href="/sp500_distributions"),
                    #dbc.DropdownMenuItem("SP500 Summary Table", href="/sp500_analysis"),
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
    html.Div([

        dcc.Interval(
            id="sp500_load_interval",
            n_intervals=0,
            max_intervals=0,  # <-- only run once
            interval=1
        ),
        html.Br(),
        html.Div([], id='sp500-summary-table-container',
                 style={'width': '70%',
                        'margin-left':'20px'})

    ], id='sp500-page-content',)

])


@callback(
    Output("sp500-summary-table-container", "children"),
    Input(component_id="sp500_load_interval",
          component_property="n_intervals"),
)
def update_sp_summary_tbl_layout(n_intervals: int):

    tmp_lst = []
    for t in datao['data'].keys():
        #print(t,datao['data'][t]['historical'])
        lst_cls = datao['data'][t]['historical']['Close']
        if not lst_cls.empty:
            #print(datao['data'][t]['info'])
            trl_pe = 0
            fwd_pe = 0
            div_rt = 0

            if 'trailingPE' in datao['data'][t]['info']:
                trl_pe = datao['data'][t]['info']['trailingPE']
                if isinstance(trl_pe, float):
                    trl_pe = np.round(trl_pe, 2)

            if 'forwardPE' in datao['data'][t]['info']:
                fwd_pe = datao['data'][t]['info']['forwardPE']
                if isinstance(fwd_pe, float):
                    fwd_pe = np.round(fwd_pe, 2)

            if 'dividendRate' in datao['data'][t]['info']:
                if isinstance(datao['data'][t]['info']['dividendRate'], float):
                    div_rt = np.round(
                        datao['data'][t]['info']['dividendRate']/lst_cls[-1], 3)

            mnth_chg = np.round(lst_cls[-1]-lst_cls[-30], 2)
            mnth_chg_pct = np.round((lst_cls[-1]-lst_cls[-30])/lst_cls[-30], 2)

            wk_chg = np.round(lst_cls[-1]-lst_cls[-7], 2)
            wk_chg_pct = np.round((lst_cls[-1]-lst_cls[-7])/lst_cls[-7], 2)

            tmp_lst.append({'Stock': t,
                            'Last Close': np.round(lst_cls[-1], 2),
                            '52 Week High': np.round(lst_cls.max()),
                            '52 Week Avg': np.round(lst_cls.mean()),
                            '52 Week Sigma': np.round(lst_cls.std()),
                            '7 Day Value': np.round(lst_cls[-7], 2),
                            '7 Day Change': wk_chg,
                            '7 Day Change %': wk_chg_pct,
                            '30 Day Value': np.round(lst_cls[-30], 2),
                            '30 Day Change': mnth_chg,
                            '30 Day Change %': mnth_chg_pct,
                            'Trailing PE': trl_pe,
                            'Forward PE': fwd_pe,
                            'Dividend Yield': div_rt
                            })

    sp500_summary_df = pd.DataFrame.from_dict(tmp_lst)    
    summary_tbl = [html.H3('SP500 Summary Table'),
                   dash.dash_table.DataTable(
        columns=[{'name': i, 'id': i} for i in sp500_summary_df.columns],
        data=sp500_summary_df.to_dict('records'),
        style_header=dict(backgroundColor="paleturquoise"),
        filter_action='native',
        sort_action='native'
    )]

    return summary_tbl