import pandas as pd

def data_table():
    
    df = pd.DataFrame()
    df['Company'] = ['Toyota', 'Volkswagen', 'Daimler', 'Ford', 'Honda', 'BMW',
                     'General Motors', 'Stellantis', 'Hyunday', 'Nissan']
    df['Country'] = ['Japan', 'Germany', 'Germany', 'USA (Mi)', 'Japan', 'Germany', 
                     'USA (Mi)', 'Netherlands', 'South Korea', 'Japan']
    df['iso_alpha'] = ['JPN', 'DEU', 'DEU', 'USA', 'JPN', 'DEU', 'USA', 'NLD', 'KOR', 'JPN']
    df['Employees'] = [366283, 662653, 288064, 186000, 211374, 120726, 155000, 204000, 70388, 136134]
    df['MarketCapitalization'] = [247.484, 154.409, 99.237, 57.958, 55.318, 70.837, 85.241, 60.809, 48.913, 19.305]

    
    #save file
    df.to_csv("data/data_table.csv")
    
    print(df)
    return df

data_table()