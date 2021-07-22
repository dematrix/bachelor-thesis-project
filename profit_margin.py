# revenue vs. income
import pandas as pd

class Profit_ratio:
    
    def __init__(self):
        self.data_income = pd.read_csv('data/income/income.csv', index_col=0, parse_dates=True)
        self.data_financials = pd.read_csv('data/revenue/financials.csv', index_col=0, parse_dates=True)
               

    def calculate_margin(self):
        self.income = self.data_income[['Net Income']]
        self.sales = self.data_financials[['Sales/Revenue', 'stock']]
        
        self.income['Sales/Revenue'] = self.sales['Sales/Revenue']
        self.income['stock'] = self.sales['stock']
        self.ratio = self.income
        self.ratio['ratio'] = self.income['Net Income'] / self.sales['Sales/Revenue'] * 100
        
        print(self.ratio)
        
        self.ratio.to_csv("data/profit_ratio/profit_ratio.csv")
        

if __name__ == "__main__":
    c = Profit_ratio()
    c.calculate_margin()
    
    