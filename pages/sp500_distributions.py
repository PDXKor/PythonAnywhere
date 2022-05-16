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
#initial_ticker_val = 'AAPL'
#a = yfinance.Ticker(initial_ticker_val)

sp500_distribution_layout = html.Div([
    
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
                    dbc.DropdownMenuItem("Jupyter Analysis", href="/jupyter_analysis"),
                    dbc.DropdownMenuItem("Wine Ratings by Price", href="/wine_data"),
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
            id="sp500_dist_load_interval",
            n_intervals=0,
            max_intervals=0,  # <-- only run once
            interval=1
        ),
        html.Br(),
        html.Div([], id='sp500-distirbution-container',
                 style={'width': '98%',
                        'margin-left':'20px'})

    ], id='sp500-page-content',)

])
@callback(
    Output("sp500-distirbution-container", "children"),
    Input(component_id="sp500_dist_load_interval",
          component_property="n_intervals"),
)
def update_sp_dist_layout(n_intervals: int):
    
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
    
    #drop rows w/o values
    sp500_summary_df = sp500_summary_df.drop(sp500_summary_df[sp500_summary_df['Trailing PE'] == 'N/A'].index)
    sp500_summary_df = sp500_summary_df.drop(sp500_summary_df[sp500_summary_df['Forward PE'] == 'N/A'].index)
    
    #drop outliers
    sp500_summary_df = sp500_summary_df.drop(sp500_summary_df[sp500_summary_df['Trailing PE'] > 300].index)
    sp500_summary_df = sp500_summary_df.drop(sp500_summary_df[sp500_summary_df['Forward PE'] > 300].index)
    
    # Seven Day Change % Distribution
    seven_day_chng_fig = px.histogram(sp500_summary_df, 
                                      x='7 Day Change %',
                                      marginal="box",
                                      nbins=60)     
    seven_day_chng_fig.update_yaxes(title_text=None)
        
    # Seven Day Change % Distribution vs Sigma 
    seven_day_chng_v_thirty = px.scatter(sp500_summary_df, 
                                         x='7 Day Change %',
                                         y='30 Day Change %',
                                         hover_name="Stock")
    
    
    #seven_day_chng_v_thirty.update_yaxes(title_text=None)
    seven_day_chng_v_thirty.update_yaxes(title_standoff =100,
                                         ticks="inside",
                                         tickfont={'size':8},
                                         dtick=.2)
    
    
    thirty_day_chng_fig = px.histogram(sp500_summary_df, 
                       x='30 Day Change %',
                       marginal="box",
                       color_discrete_sequence=['indianred'], # color of histogram bars
                       nbins=60)
    
    thirty_day_chng_fig.update_yaxes(title_text=None)
    
    # Trailing PE vs Forward PE
    trl_pe_v_fwd_pe = px.scatter(sp500_summary_df, 
                                 x='Trailing PE',
                                 y='Forward PE',
                                 marginal_x="violin",
                                 marginal_y="violin",
                                 color_discrete_sequence=['indianred'],
                                 hover_name="Stock")
    
    
    # Trailing PE vs Forward PE
    trl_pe_v_fwd_pe.update_yaxes(title_standoff =100,
                                         ticks="inside",
                                         tickfont={'size':8})   
   

    trailing_pe_fig = px.histogram(sp500_summary_df, 
                       x='Trailing PE',
                       marginal="box",
                       nbins=60)
        
    trailing_pe_fig.update_yaxes(title_text=None)
    trailing_pe_fig.update_xaxes(ticks="inside",                                
                                 #tick0=0,
                                 tickvals=[0, 10, 25, 50, 75, 100, 125, 200, 250]
                                 #dtick=25
                                 )
    trailing_pe_fig.update_layout(xaxis_range=[0,175])
    
    
    forward_pe_fig = px.histogram(sp500_summary_df, 
                       x='Forward PE',
                       marginal="box",
                       nbins=60)
    
    forward_pe_fig.update_yaxes(title_text=None)
    forward_pe_fig.update_xaxes(ticks="inside",                                
                                 #tick0=0,
                                 tickvals=[0, 10, 25, 50, 75, 100, 125, 200, 250]
                                 #dtick=25
                                 )
    forward_pe_fig.update_layout(xaxis_range=[0,175])
    
    seven_day_chng_dist_descr = 'Indicates S&P 500 percentage movement over the last seven days. Distribution type may indicate broad market moves vs sector moves.'
    
    seven_day_vs_thirty_day_descr = 'Scatter plot of seven day vs thirty day percentage change of individual stocks in the S&P 500. Outliers could help indicate stocks that have changed course in the last seven days.'
    
    thirty_day_chng_dist_descr = 'Indicates S&P 500 percentage movement over the last thirty days.'
    
    trl_v_fwd_pe_descr = 'Plots forward PE vs trailing PE for S&P 500 stocks, this can help indicate stocks with future upside on EPS.'
    
    chart = html.Div([
        
        #html.H3(['S&P 500 Distributions'])
        
        html.Div([

            html.Div([
                
                dcc.Graph(id='seven_day_chng_dist',
                          figure=seven_day_chng_fig),
                html.P([seven_day_chng_dist_descr],
                       style={'margin-left': '80px',
                              'margin-top': '-5px'}),
            ],
                style={'width': '47%',
                       'display': 'inline-block'}),

            html.Div([
                
                dcc.Graph(id='seven_day_chng_dist_2',
                          figure=seven_day_chng_v_thirty),
                html.P([seven_day_vs_thirty_day_descr],
                       style={'margin-left': '80px',
                              'margin-top': '-5px'}),
            ],
                style={'width': '47%',
                       'display': 'inline-block', }),

        ]),

        html.Div([

            html.Div([
                
                dcc.Graph(id='thirty_day_chng_dist',
                          figure=thirty_day_chng_fig),
                html.P([thirty_day_chng_dist_descr],
                       style={'margin-left': '80px',
                              'margin-top': '-5px'}),
            ],
                style={'width': '47%',                       
                       'display': 'inline-block'}),
            
            html.Div([
                
                dcc.Graph(id='trl_v_fwd_pe_dist',
                          figure=trl_pe_v_fwd_pe),
                html.P([trl_v_fwd_pe_descr ],
                       style={'margin-left': '80px',
                              'margin-top': '-5px'}),
            ],
                style={'width': '47%',
                       'display': 'inline-block', }),

        ]),
        
        
        #dcc.Graph(id='thirty_day_chng_dist',figure=thirty_day_chng_fig),
                      
        dcc.Graph(id='trailing_pe_dist',figure=trailing_pe_fig),
                      
        dcc.Graph(id='forward_pe_dist',figure=forward_pe_fig),
                      
        ])
    
    return chart