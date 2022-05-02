import dash
#from dash import html
#from dash import dcc
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

# for deployment, pass app.server (which is the actual flask app) to WSGI etc
app = dash.Dash('Analytics Dash',
                external_stylesheets=[dbc.themes.LUX],
                suppress_callback_exceptions=True)

quick_ratio_text = "A measure of a company’s short-term liquidity. It measures a company’s ability to meet its short-term obligations. QR = (CE(Cash & Equivalents) + MS(Marketable Securities) + AR(Accounts Recievable)) / CL (Current Liabilities). A value of 1 indicates that a company can fully meet its short term obligations."

peg_ratio_text = "The price/earnings to growth ratio is the price-to-earnings (P/E) ratio divided by the growth rate of its earnings for a specified time period. Determines a stock's value while also factoring in the company's expected earnings growth. A PEG of 1 is a perfect correlation between its stock price and expected growth. A PEG less than 1 may indicate the stock is undervalued as compared to future growth, greater than one may indicate the stock is overvalued as compared to future growth."

trailing_peg_ratio_text = "In the trailing PEG method, a company's earnings growth rate is calculated using its historical EPS growth rates. The growth rate can be for the past 12 months, 3 years, 5 years, or any other multiple year historical average On the other hand, forward PE ratios are calculated using expected EPS growth rates."

current_ratio_text = "A liquidity ratio that measures a company’s ability to pay short-term obligations due within one year."

short_ratio_text = "The short ratio is a widely-used tool by short selling hedge funds and other portfolio managers in the stock market. The short ratio indicates the number of shares that investors sell short over the average daily volume of the stock on the basis of 1 or 3 months."


def format(x):
    return "${:,.0f}".format(x/1000000)


fig = None
a = None


initial_ticker_val = 'AAPL'
a = yfinance.Ticker(initial_ticker_val)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

page_1_layout = html.Div([

    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("General Equity Analysis", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem(
                        "Individual Equity Data", href="/index"),
                    dbc.DropdownMenuItem("Page 3", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="{Default App}",
        brand_href="#",
        color="primary",
        dark=True,),

    #dcc.Link('Go to index', href='/index'),
    html.Br(),

    html.Div(id='page-1-content', children=[

        # Jupyter Notebooks
        html.H3(children='Equity Analysis'),
        html.A("Equity Variance Analysis",
               href='/static/jupyter_nb/python_class_basics.html', target="_blank"), html.Br(),
        html.A("Equity PE Analysis", href='/static/jupyter_nb/python_class_basics.html',
               target="_blank"), html.Br(),
        html.A("Equity Variance Analysis",
               href='/static/jupyter_nb/python_class_basics.html', target="_blank"), html.Br()


    ], style={'margin-left': '20px', 'margin-right': '20px'}),

])


index_page = html.Div(id='index-content', children=[

    #navbar
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Individual Equity Data", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem(
                        "General Equity Analysis", href="/page-1"),
                    dbc.DropdownMenuItem("Page 3", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="{Default App}",
        brand_href="#",
        color="primary",
        dark=True,),

    html.Br(),
    html.P(id='slow-text', children='Data loaded from yfinance - sometimes API calls are slow =[',
           style={'font-size': '16px', 'color': 'red', 'text-align': 'right', 'margin-right': '30px', 'font-weight': 'bold'}),

    dcc.Loading(id="ls-loading-1",
                children=[html.Div(id="ls-loading-output-1",
                                   style={'position': 'absolute', 'z-index': '-1'})],
                type="default"),

    html.Div(children=[

        html.H3(['Daily Close']),

        dcc.Input(id='tickerInput',
                  placeholder="Stock Symbol",
                  value="AAPL", style={'margin-bottom': '10px'}),

        html.Button('Get Data',
                    id='getStockDataButton',
                    n_clicks=0, style={'margin-bottom': '10px'}),

        html.P(id='loading-text', children='Data loaded from yfinance - sometimes API calls are slow!',
               n_clicks=0,
               style={'font-size': '10px'}),

        # #chart loading
        # dcc.Loading(id="ls-loading-1",
        #             children=[html.Div(id="ls-loading-output-1",
        #                                style={'position': 'absolute','z-index':'-1'})],
        #             type="default"),

        # chart
        dcc.Graph(id='stock-price-over-time',
                  style={'margin-left': '10px',
                         'margin-top': '0px',
                         'height': '500px',
                         'width': '100%',
                         'font-size': '12px',
                         'display': 'none',
                         'position': 'absolute',
                         'z-index': '1'}),

        html.Div(id='balance-sheet-table-div',
                 children=[]),

        html.Br(),
        #html table of stock facts
        html.H3(['Ratios']),

        dbc.Table(id='ratio-table', children=[

            html.Tr([html.Td(['Quick Ratio']),
                     html.Td([quick_ratio_text]),
                     html.Td(id='quickRatio')]),

            html.Tr([html.Td(['PEG Ratio']),
                     html.Td([peg_ratio_text]),
                     html.Td(id='pegRatio')]),

            html.Tr([html.Td(['Trailing PEG Ratio']),
                     html.Td([trailing_peg_ratio_text]),
                     html.Td(id='trailingPegRatio')]),

            html.Tr([html.Td(['Current Ratio']),
                     html.Td([current_ratio_text]),
                     html.Td(id='currentRatio')]),

            html.Tr([html.Td(['Short Ratio']),
                     html.Td([short_ratio_text]),
                     html.Td(id='shortRatio')])

        ], bordered=True, style={'margin-left': '20px', 'width': '70%', 'font-size': '12px', 'display': 'none'}),

    ], style={'margin-left': '20px', 'margin-right': '20px'})

])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/page-1':
        return page_1_layout
    else:
        return index_page


@app.callback(
    Output('loading-text', 'children'),
    State('tickerInput', 'value'),
    Input('getStockDataButton', 'n_clicks'))
def set_loading_text(tickerInput, getStockDataButton):
    load_text = u'Retrieving Data for {}'.format(tickerInput)
    return load_text


@app.callback(
    Output('stock-price-over-time', 'figure'),
    Output('quickRatio', 'children'),
    Output('pegRatio', 'children'),
    Output('balance-sheet-table-div', 'children'),
    Output('trailingPegRatio', 'children'),
    Output('currentRatio', 'children'),
    Output('shortRatio', 'children'),
    Output('stock-price-over-time', 'style'),
    Output('ratio-table', 'style'),
    Output("ls-loading-output-1", "children"),
    State('tickerInput', 'value'),
    Input('loading-text', 'n_clicks'),
    Input('getStockDataButton', 'n_clicks'))
def update_output(tickerInput, loading_text_clicks, getStockDataButton):

    if getStockDataButton == 0:
        print('initial load')
        aa = a
    else:
        print('secondary load')
        aa = yfinance.Ticker(tickerInput)

    queVal = '1y'
    dff = aa.history(period=queVal)
    dff['SMA30'] = dff['Close'].rolling(30).mean()
    dff['SMA90'] = dff['Close'].rolling(90).mean()
    dff['Min'] = dff['Close'].tail(365).min()
    dff['Max'] = dff['Close'].tail(365).max()
    dff['YearMean'] = dff['Close'].mean()

    new_fig = go.Figure()
    new_fig.add_trace(go.Scatter(x=dff.index,
                                 y=dff['Close'],
                                 name='Daily Close'
                                 ))
    new_fig.add_trace(go.Scatter(x=dff.index,
                                 y=dff['SMA90'],
                                 name="90 Day Moving Average",
                                 line=dict(color='green',
                                           width=.85,
                                           dash='dot'),
                                 ))
    new_fig.add_trace(go.Scatter(x=dff.index,
                                 y=dff['SMA30'],
                                 name="30 Day Moving Average",
                                 line=dict(color='orange',
                                           width=.85,)))
    new_fig.add_trace(go.Scatter(x=dff.index,
                                 y=dff['Min'],
                                 name="52W Min",
                                 line=dict(color='black',
                                           width=.85),
                                 ))
    new_fig.add_trace(go.Scatter(x=dff.index,
                                 y=dff['Max'],
                                 name="52W Max",
                                 line=dict(color='black',
                                           width=.85),
                                 ))
    new_fig.add_trace(go.Scatter(x=dff.index,
                                 y=dff['YearMean'],
                                 name="52W Mean",
                                 line=dict(color='gray',
                                           width=.85,
                                           dash='dash'),
                                 ))

    new_fig.update_layout(
        margin=dict(l=45, r=45, t=20, b=50),
        paper_bgcolor="WhiteSmoke")

    fig_out = new_fig

    #show graph
    stock_chart_style = {'margin-top': '-10px',
                         'height': '500px',
                         'width': '100%',
                         'font-size': '12px',
                         'border': '1px solid #E8E8E8'}

    #build tables

    # balance sheet tables
    df_bs = aa.balance_sheet.transpose()
    df_bs.index = df_bs.index.strftime('%Y-%m-%d')
    df_bs = df_bs.transpose()
    df_bs = df_bs.drop(index=['Other Stockholder Equity',
                       'Net Receivables', 'Treasury Stock', 'Inventory'])

    for col in df_bs.columns:
        df_bs[col] = df_bs[col].apply(format)

    # assets table
    df_bs_assets = df_bs.loc[['Total Assets', 'Other Assets', 'Cash', 'Total Current Assets',
                              'Property Plant Equipment', 'Net Tangible Assets', 'Long Term Investments', 'Retained Earnings']]
    df_bs_assets.reset_index(inplace=True)

    # equity table
    df_bs_equity = df_bs.loc[['Total Stockholder Equity', 'Common Stock']]
    df_bs_equity.reset_index(inplace=True)

    # liabilities table
    df_bs_liab = df_bs.loc[['Total Liab', 'Other Current Liab',
                            'Total Current Liabilities', 'Accounts Payable', 'Short Long Term Debt']]
    df_bs_liab.reset_index(inplace=True)

    df_bs.reset_index(inplace=True)

    balance_sheet_table_div = html.Div([
        #html.Br(),
        html.Br(),
        html.Br(),
        html.H3(['Balance Sheet']),
        html.Div([
            html.H4(['Assets']),
            dash.dash_table.DataTable(
                columns=[{'name': i, 'id': i} for i in df_bs.columns],
                data=df_bs_assets.to_dict('records'),
                style_header=dict(backgroundColor="paleturquoise")
            ),
            html.Br(),
            html.H4(['Equity']),
            dash.dash_table.DataTable(
                columns=[{'name': i, 'id': i} for i in df_bs.columns],
                data=df_bs_equity.to_dict('records'),
                style_header=dict(backgroundColor="paleturquoise")
            ),
            html.Br(),
            html.H4(['Liabilities']),
            dash.dash_table.DataTable(
                columns=[{'name': i, 'id': i} for i in df_bs.columns],
                data=df_bs_liab.to_dict('records'),
                style_header=dict(backgroundColor="paleturquoise"),
            )
            # html.Br(),
            # html.H4(['Full Table']),
            # dash.dash_table.DataTable(
            # columns = [{'name': i, 'id': i} for i in df_bs.columns],
            # data = df_bs.to_dict('records'))

        ],style={'margin':'20px 0px 0px 30px'}
        )
    ]),

    #style={'margin-left':'20px'}

    # sometimes the dict returned does not have the data,
    # so you need to check if the key exists in the dict
    # before you populate
    quickRatio = ''
    pegRatio = ''
    trailingPegRatio = ''
    currentRatio = ''
    shortRatio = ''

    if 'quickRatio' in aa.info:
        quickRatio = aa.info['quickRatio']

    if 'pegRatio' in aa.info:
        pegRatio = aa.info['pegRatio']

    if 'trailingPegRatio' in aa.info:
        trailingPegRatio = aa.info['trailingPegRatio']

    if 'currentRatio' in aa.info:
        currentRatio = aa.info['currentRatio']

    if 'shortRatio' in aa.info:
        shortRatio = aa.info['shortRatio']

    ratio_table_style = {'margin-left': '20px',
                         'width': '70%', 'font-size': '12px'}

    loading_done = ''

    return fig_out, quickRatio, pegRatio, balance_sheet_table_div, trailingPegRatio, currentRatio, shortRatio, stock_chart_style, ratio_table_style, loading_done


if __name__ == '__main__':
    app.run_server()
