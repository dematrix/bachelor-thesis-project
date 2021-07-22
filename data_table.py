import pandas as pd
import yfinance as yf
from ticker import get_ticker

symbols = get_ticker()

def data_table():
    
    employees = ()
    market_cap = ()
    country = ()
    ticker = ''
    # create df
    df = pd.DataFrame()

    
    for name, ticker in symbols.items():
    
        # load data from yahoo finance
        stock = yf.Ticker(ticker)
        data = list(stock.info.items())
        
        employees = ()
        market_cap = ()
        country = ()
        
        for i in range(len(data)):
            if data[i][0] == 'fullTimeEmployees':
                employees = data[i]
            elif data[i][0] == 'marketCap':
                market_cap = data[i]
            elif data[i][0] == 'country':
                country = data[i]
        # create sub df
        df_sub = pd.DataFrame()
        df_sub['Employees'] = employees
        df_sub['Country'] = country
        df_sub['Market Capitalization'] = market_cap
        df_sub['stock'] = ticker
        
        df.append(df_sub)
        print('yes')
        #df.to_csv("data/data_table/data_table_" + ticker + ".csv")
        
    # delete first row
    df = df.iloc[1:]
        
        
    #save file
    df.to_csv("data/data_table/data_table.csv")

data_table()