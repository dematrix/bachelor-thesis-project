import os
import copy
import glob
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from pathlib import Path
from ticker import get_ticker
from currency_converter import Currency_convertor

# ACCESS KEY FROM fixer.io'
url = str.__add__('http://data.fixer.io/api/latest?access_key=', '0545ca7fa1e9e8ce58879344306e41db')  
# Covert foreign currency to USD
c = Currency_convertor(url)
krw = c.convert('KRW', 'USD', 1)
jpy = c.convert('JPY', 'USD', 1)
eur = c.convert('EUR', 'USD', 1)

cdw = os.getcwd()

# Get ticker
Symbols = get_ticker()
symbols_copy = copy.deepcopy(Symbols)

def get_revenue(Symbols):
    
    for name, ticker in Symbols.items():

        try:
            url='https://www.marketwatch.com/investing/stock/'+ticker+'/financials'
            
            # Make a GET request to fetch the raw HTML content
            html_content = requests.get(url).text
            
            # Parse the html content
            soup = BeautifulSoup(html_content, "lxml")
            #print(soup.prettify()) # print the parsed data of html
            
            pe_table = soup.select_one('table.table.table--overflow.align--right')
            #print(pe_table)
            
            pe_table_head = pe_table.find("thead")
            pe_table_data = pe_table.tbody.find_all("tr")
            
            # Get all the years of Lists
            years = []
            for th in pe_table_head.find_all("th"):
                # remove any newlines and extra spaces from left and right
                years.append(th.text.replace('\n', ' ').strip())
             
            years.pop()
            years.pop(0)
        
            # Create value table
            res = []
            for tr in pe_table_data:
                td = tr.find_all('td')
                row = [tr.text.strip() for tr in td if tr.text.strip()]
                row[0] = row[0].split('\n').pop()
                # Convert Sales/Revenue to USD if needed
                if row[0] == 'Sales/Revenue':
                    for i in range(len(row)-1):
                        row[i+1] = row[i+1].replace('T', '').replace('B', '')
                        row[i+1] = float(row[i+1])
                        if ticker == 'HYMTF':
                            row[i+1] *= krw*1000
                            row[i+1] = round(row[i+1], 2)
                        elif ticker in ['TM', 'NSANY', 'HMC']:
                            row[i+1] *= jpy*1000
                            row[i+1] = round(row[i+1], 2)
                        elif ticker in ['VLKPF', 'DDAIF', 'BAMXF', 'STLA']:
                            row[i+1] *= eur
                            row[i+1] = round(row[i+1], 2)

                    #print(ticker, ': ', row)
                if row:
                    res.append(row)
            # Transpose table       
            res = np.asarray(res).T
            # extract first row for heading
            heading = res[0]
            years = np.asarray(years)
            stock = np.asarray([ticker for i in range(len(years))])
            # remove first row
            res = np.delete(res, 0, axis=0)
            # Add 'Years' and ticker to heading
            heading = np.insert(heading, 0, 'Year', axis=0)
            heading = np.insert(heading, len(heading), ticker, axis= 0)
            # Add year and stock name to column
            res = np.insert(res, 0, years, axis=1)
            res = np.insert(res, len(heading)-1, stock, axis=1)
            # Create df 
            df = pd.DataFrame(res, columns=heading)
            df.index = pd.to_datetime(df['Year'])
            df.to_csv("data/revenue/revenue_" + ticker + ".csv")
        
        except:
            symbols_copy.pop(name)
            
    # remove file if file exists
    file  = Path('data/revenue/financials.csv')
    if file.is_file():
        os.remove('data/revenue/financials.csv')
    # search and merge csv files  
    os.chdir('data/revenue')
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    print(all_filenames)
    #combine all files in the list
    financials = pd.concat([pd.read_csv(f) for f in all_filenames ])
    
    symbols_list = symbols_copy.values()
    symbols_list = list(symbols_list)
    #for i in range(len(symbols_list)-1):
    financials['TM'].update(financials.pop('F'))
    financials['TM'].update(financials.pop('VLKPF'))
    financials['TM'].update(financials.pop('DDAIF'))
    financials['TM'].update(financials.pop('HMC'))
    financials['TM'].update(financials.pop('BAMXF'))
    financials['TM'].update(financials.pop('GM'))
    financials['TM'].update(financials.pop('HYMTF'))
    financials['TM'].update(financials.pop('NSANY'))
    financials['TM'].update(financials.pop('STLA'))
    financials.rename(columns = {'TM': 'stock'}, inplace=True)
    #export to csv
    financials.to_csv( "financials.csv", index=False, encoding='utf-8-sig')
    os.chdir(cdw)
    
#get_revenue(Symbols)