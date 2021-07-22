import os
import pandas as pd
import yfinance as yf
import datetime

from ticker import get_ticker


Symbols = get_ticker()
#os.chdir("bachelorthesis")

def get_stock_data(Symbols):
    
    # timeframe - 10 years
    end = datetime.datetime.today()
    start = datetime.datetime(end.year-10,1,1)
    
    
    # create empty dataframe
    stockdata = pd.DataFrame()
    # iterate over each symbol
    for j,i in Symbols.items():  
        
        # print the symbol which is being downloaded
        print(' ' + j + str(' : ') + i, sep=',', end=',', flush=True)  
        
        try:
            # download the stock price 
            stock = []
            stock = yf.download(i,start=start, end=end, progress=False)
            # append the individual stock prices 
            if len(stock) == 0:
                None
            else:
                stock['stock'] = i
                stock['name'] = j
                stock['value'] = stock['Close']
                stock['change'] = stock['Close']
                stock['change'] = stock['change'].pct_change(periods=1)
                stock.to_csv("data/stock_dfs/" + i + ".csv")
                stockdata = stockdata.append(stock,sort=False)
        except Exception:
            None
     
    stockdata = stockdata.reset_index()
    
    return stockdata.to_csv("data/stockdata.csv")

#get_stock_data(Symbols)
