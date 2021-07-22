import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from ticker import get_ticker
import numpy as np

style.use('ggplot')

Symbols = get_ticker()


def compile_data(symbols):
    
    tickers = Symbols.items()
        
    main_df = pd.DataFrame()
    
    for label, ticker in tickers:
        df = pd.read_csv('data/stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)
        
        print(ticker)
        df.rename(columns={'Adj Close': label}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'name', 'change', 'stock', 'value'], 1, inplace=True)
        
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

    print(main_df.head())
    main_df.to_csv('data/ticker_joined_closes.csv')
    
    
#compile_data(Symbols)


def visualize_data():
    
    compile_data(Symbols)
    
    df = pd.read_csv('data/ticker_joined_closes.csv')
    df_corr = df.corr()
    
    print(df_corr.head())
    
    df_corr.to_csv('data/df_corr.csv')
    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlBu)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    
    column_labels = df_corr.columns
    row_labels = df_corr.index
    
    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.yticks(rotation=90)
    heatmap.set_clim(-1, 1)
    plt.tight_layout()
    plt.show()


# visualize_data()
