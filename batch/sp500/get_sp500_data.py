# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:47:10 2022
@author: Korey
"""

import pickle
import pandas as pd
import yfinance as yf
from datetime import datetime

#read file

#fileo = open('sp500pickle.pickle', 'rb')
#datao = pickle.load(fileo)
#print(datao)

month_day = datetime.now().strftime("%m-%d")
df = pd.read_csv('sp500_tickers.csv')
symbols = df['Symbol'].values

#save_dict = {'last_update_date':month_day,'data':{}}
# with open('sp500pickle.pickle', 'wb') as f:
#     pickle.dump(save_dict, f)

for s in symbols:
    
    print('checking data for ',s)
    
    # open file
    fileo = open('sp500pickle.pickle', 'rb')
    
    # get dict
    datao = pickle.load(fileo)
    #print(datao)
    print(len(datao['data'].keys()))
    
    # check dict date
    read_month_day = datao['last_update_date']
          
    # if stock data exists and current month day not equal to current month day, replace stock info
    if s in datao['data'] and month_day != read_month_day:
        print(month_day,read_month_day)
        print('data is stale - refreshing for ',s)
        ydata = yf.Ticker(s)
        yinfo = ydata.info
        yhist = ydata.history(period='1y')
        temp_dict = {'info':yinfo,'historical':yhist}
        datao['data'][s] = temp_dict
    
    elif datao['data'].get(s) is None:
        print('data does not exist for - getting new for',s)
        ydata = yf.Ticker(s)
        yinfo = ydata.info
        yhist = ydata.history(period='1y')
        temp_dict = {'info':yinfo,'historical':yhist}
        datao['data'][s] = temp_dict    
        
    else:
        print('data is current for ',s)
    
    with open('sp500pickle.pickle', 'wb') as f:
        pickle.dump(datao, f)
      
       
  
