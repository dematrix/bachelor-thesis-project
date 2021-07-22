import pandas as pd
from currency_converter import Currency_convertor

# ACCESS KEY FROM fixer.io'
url = str.__add__('http://data.fixer.io/api/latest?access_key=', '0545ca7fa1e9e8ce58879344306e41db')  
# Covert foreign currency to USD
c = Currency_convertor(url)
krw = c.convert('KRW', 'USD', 1)
jpy = c.convert('JPY', 'USD', 1)
eur = c.convert('EUR', 'USD', 1)

#currency rate to USD
#krw = 0.00089679162
#jpy = 0.009268832
#eur = 1.2099787


def get_income():

    # dataframe
    df_income = pd.read_csv('data/revenue/financials.csv')
    
    # create sup df 'net income'
    income = df_income[['Year.1', 'Net Income', 'stock']]
    income.rename(columns={'Year.1': 'Year'}, inplace=True)
    
    
    for i in range(len(income)):
        # remove brackets and put a minus sign
        income.loc[i, 'Net Income'] = income.loc[i, 'Net Income'].replace('-', '0').replace('(', '-').replace(')', '')
        # Convert values to billions
        if 'T' in income.loc[i, 'Net Income']:
            income.loc[i, 'Net Income'] = float(income.loc[i, 'Net Income'].replace('T', ''))*1000
        elif 'B' in income.loc[i, 'Net Income']:
            income.loc[i, 'Net Income'] = float(income.loc[i, 'Net Income'].replace('B', ''))
        elif 'M' in income.loc[i, 'Net Income']:
            income.loc[i, 'Net Income'] = float(income.loc[i, 'Net Income'].replace('M', ''))/1000
            
    for i in range(len(income)):
        # Convert values to USD if needed
        if income.loc[i, 'stock'] in ['TM', 'NSANY', 'HMC']:
            income.loc[i, 'Net Income'] *= jpy
        elif income.loc[i, 'stock'] == 'HYMTF':
            income.loc[i, 'Net Income'] *= krw
        elif income.loc[i, 'Net Income'] in ['VLKPF', 'DDAIF', 'BAMXF', 'STLA']:
            income.loc[i, 'Net Income'] *= eur
            
    
    income.index = income['Year']
    income.to_csv("data/income/income.csv")


    #print(income)

get_income()