import os
import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objs as go

from dash.dependencies import Input, Output

from ticker import get_ticker
from revenue import get_revenue
from income import get_income
from stockdata import get_stock_data
from heatmap_close_price import visualize_data

cdw = os.getcwd()
Symbols = get_ticker()
get_stock_data(Symbols)
get_revenue(Symbols)
get_income()
visualize_data()
# Load data
df = pd.read_csv('data/stockdata.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'])
df_financials = pd.read_csv('data/revenue/financials.csv', index_col=0, parse_dates=True)
df_income = pd.read_csv('data/income/income.csv', index_col=0, parse_dates=True)
df_proft_ratio = pd.read_csv('data/profit_ratio/profit_ratio.csv', index_col=0, parse_dates=True)
df_table = pd.read_csv('data/data_table.csv', index_col=0, parse_dates=True)

# Initialise the app
app = dash.Dash(__name__)


# Creates a list of dictionaries, which have the keys 'label' and 'value'.
def get_options(Symbols):
    dict_list = []
    for i, j in Symbols.items():
        dict_list.append({'label': i, 'value': i})
    return dict_list

# Define the app
app.layout = html.Div(children=[
                      html.Div(  
                               children=[
                                  # Define the left element
                                  html.Div(className='four columns', children = [
                                      html.Div(className='title', children = [
                                        html.H2('Company Performance'),
                                        html.H3('''Comparison of Car Manufacturer'''),
                                        ]),
                                       
                                       html.Div(className='graph_box_revenue', children = [                          
                                       dcc.Graph(id='financials', config={'displayModeBar': False}),
                                                            ]),
                                       html.Div(className='graph_box_income', children = [                          
                                       dcc.Graph(id='incomes', config={'displayModeBar': False}),
                                                               ]), 
                                       html.Div(className='graph_box_profit_ratio', children = [                          
                                       dcc.Graph(id='ratio', config={'displayModeBar': False}),
                                                               ]), 
                                       
                                    ]), 
                                  # Define the right element
                                  html.Div(className='eight columns', children = [
                                                  
                                        # Define Dropdown Menu   
                                        html.Div(className='dropdown_box', children = [
                                        html.P('''Pick one or more companies from the dropdown below.'''),
                                        html.Div(className='div-for-dropdown',
                                            children=[
                                                dcc.Dropdown(id='stockselector',
                                                            options=get_options(Symbols),
                                                            placeholder = "Select...",
                                                            multi=True,
                                                            value=[df['name'].sort_values()[0]],
                                                            style={'backgroundColor': '#FFFFFF'},
                                                            className='stockselector')
                                                     ])
                                            ]),
                                               
                                               
                                         html.Div(className='graph_box_corr', children = [                          
                                         dcc.Graph(id='correlation', config={'displayModeBar': False}),
                                         ]),
                                         html.Div(className='graph_box_price', children = [                          
                                         dcc.Graph(id='timeseries', config={'displayModeBar': False}),
                                         ]),
                                         html.Div(className='graph_data_table', children = [                          
                                         dcc.Graph(id='table', config={'displayModeBar': False}),
                                         ]),   
                                       ]),
                    
                                  ])
                                ])
# stockprice chart
@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_timeseries(selected_dropdown_value):
    trace = []  
    df_sub = df
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:
        trace.append(go.Scatter(x=df_sub[df_sub['name'] == stock].index,
                                 y=df_sub[df_sub['name'] == stock]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))  
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_white',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Stock Prices', 'font': {'color': '#F87111'}, 'x': 0.08},
                  yaxis=dict(title=dict(text='Stock Price in USD')),
                  xaxis=dict(
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1,
                                     label="1m",
                                     step="month",
                                     stepmode="backward"),
                                dict(count=6,
                                     label="6m",
                                     step="month",
                                     stepmode="backward"),
                                dict(count=1,
                                     label="YTD",
                                     step="year",
                                     stepmode="todate"),
                                dict(count=1,
                                     label="1y",
                                     step="year",
                                     stepmode="backward"),
                                dict(step="all")
                                        ]), x=0.75,
                                          ),
                          )
                               ),
              }

    return figure

# Revenue chart
@app.callback(Output('financials', 'figure'),
              [Input('stockselector', 'value')])
def update_revenue(selected_dropdown_value):
    trace = []  
    df_sub = df_financials
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:
        stock_data = Symbols[stock]
        trace.append(go.Scatter(x=df_sub[df_sub['stock'] == stock_data].index,
                                 y=df_sub[df_sub['stock'] == stock_data]['Sales/Revenue'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))  
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_white',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  #height=300,
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Sales/Revenue', 'font': {'color': '#F87111'}, 'x': 0.15},
                  yaxis=dict(title=dict(text='Revenue in Billions [USD]')),
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()], },
                               ),
              }

    return figure
# heatmap correlation
@app.callback(Output('correlation', 'figure'),
              [Input('stockselector', 'value')])

def filter_heatmap(selected_dropdown_value):   
    # Create columns names
    df_corr = pd.read_csv('data/df_corr.csv')
    col_names = []
    for col in df_corr.columns:
        col_names.append(col)
    # delete first element    
    col_names.pop(0)
    # clean data from non numerical elements
    arr = df_corr.to_numpy()
    corr = []
    
    for row in arr:
        row = np.delete(row, 0)
        corr.append(row)
    
    corr = np.asarray(corr)
    # Define Figure
    fig = go.Figure(data=go.Heatmap(
        x=col_names,
        y=col_names,
        z=corr,
        colorscale='Viridis',
        hoverongaps = False))
    
    fig.update_layout(
        title='Correlations',
        title_font_color='#F87111',
        autosize=True,
        
       )
    
    return fig
# income chart
@app.callback(Output('incomes', 'figure'),
              [Input('stockselector', 'value')])
def update_income(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    trace = []  
    df_sub = df_income
    print(Symbols)
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:
        stock_data = Symbols[stock]
        trace.append(go.Scatter(x=df_sub[df_sub['stock'] == stock_data].index,
                                 y=df_sub[df_sub['stock'] == stock_data]['Net Income'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))  
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_white',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  #height=300,
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Net Income', 'font': {'color': '#F87111'}, 'x': 0.15},
                  yaxis=dict(title=dict(text='Income in Billions [USD]')),
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()], },
                               ),
              }

    return figure

# profit margin ratio
@app.callback(Output('ratio', 'figure'),
              [Input('stockselector', 'value')])
def update_profit_ratio(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    trace = []  
    df_sub = df_proft_ratio
    print(Symbols)
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:
        stock_data = Symbols[stock]
        trace.append(go.Scatter(x=df_sub[df_sub['stock'] == stock_data].index,
                                 y=df_sub[df_sub['stock'] == stock_data]['ratio'],
                                 mode='markers',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))  
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_white',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  #height=300,
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Profit Ratio', 'font': {'color': '#F87111'}, 'x': 0.15},
                  yaxis=dict(title=dict(text='Profit Ratio in %')),
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()], },
                               ),
              }

    return figure

# bubble map
@app.callback(Output('table', 'figure'),
              [Input('stockselector', 'value')])
def update_data_table(value):
    
    #fig = go.Figure(go.Scattergeo())
    #fig.update_geos(df_table, locations='iso_alpha', color='Company',
                    #size='MarketCapitalization', title='Market Capitalization', projection_type="natural earth")
    #fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
    
    
    fig = px.scatter_geo(df_table, 
                         locations="iso_alpha", 
                         color="Company", 
                         title='Market Capitalization in Billions [USD]', 
                         hover_name="Company", 
                         size='MarketCapitalization', 
                         projection="natural earth",
                         height=300)
    fig.update_geos(showcountries=True)
    fig.update_layout(height=415, margin={"r":0,"t":40,"l":0,"b":10})
    return fig
    

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)