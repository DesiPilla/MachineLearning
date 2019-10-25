import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import time as t
import pandas_datareader as pdr
from pandas_datareader import data as wb


def getTickers(step):
    url = 'http://www.stockpup.com/data/'
    site = BeautifulSoup(requests.get(url).text, "html.parser")
    files = site.findAll('a')[22:-1][::step]
    
    tickers = []
    for f in files:
        if f['href'][-3:] == 'csv':
            tickers.append(f['href'][6:].split('_')[0])
    return tickers


def getPriceData(ticker):  
    stockData = pd.DataFrame()
    
    try:
        startDate = '1980-01-01'
        dataSource = 'yahoo'

        ticker_data= wb.DataReader(ticker, data_source = dataSource, start = startDate)
        stockData = pd.DataFrame(ticker_data)[['Close', 'Volume']]
        stockData['Ticker'] = ticker
    except:
        pass
    
    return stockData.reset_index()

def getAllData(tickers):
   
    url = 'http://www.stockpup.com/data/'
    filePath = '_quarterly_financial_data.csv'
    
    print('Fetching data... (this may take up to 60 seconds or more)')
    t1 = t.time()
    
    allData = pd.DataFrame()
    for tick in tickers:
        print(tick)
        try:
            fData = pd.read_csv(url + tick + filePath)
        except:
            continue
        
        # Get fundamentals data for stock
        fData = fData[['Quarter end',
                       'Cash at end of period',
                       'Shares split adjusted',
                       'Cash from operating activities',
                       'Capital expenditures',
                       'Assets',
                       'Liabilities',
                       'EPS basic']]
        fData['Ticker'] = tick
        fData['Cash from operating activities'] = pd.to_numeric(fData['Cash from operating activities'], errors = 'corece')
        fData['EPS basic'] = pd.to_numeric(fData['EPS basic'], errors = 'coerce')
        fData['Quarter end'] = pd.to_datetime(fData['Quarter end'])
        fData = fData.reset_index().drop(columns = ['index']).sort_values(by = 'Quarter end', ascending = True)
        
        # Get price data for stock
        pData = getPriceData(tick)
        
        # Merge price and fundamentals data and build attributes
        stockData = pd.merge_asof(pData, fData, left_on = 'Date', right_on = 'Quarter end', by = 'Ticker', direction = 'backward', allow_exact_matches = False)
        stockData['Market / Book Ratio'] = stockData['Close'] / (stockData['Assets'] - stockData['Liabilities']) * stockData['Shares split adjusted']
        stockData['P/E'] = stockData['Close'] / stockData['EPS basic']
        stockData['Debt / Equity Ratio'] = stockData['Liabilities'] / (stockData['Assets'] - stockData['Liabilities'])
        stockData['Free Cash Flow Yield'] = (stockData['Cash from operating activities'] - stockData['Capital expenditures']) / (stockData['Shares split adjusted']*stockData['Close'] + stockData['Liabilities'] - stockData['Cash at end of period'])
        stockData = stockData[['Ticker',
                               'Date', 
                               'Close',
                               'Volume',
                               'Volume',
                               'Market / Book Ratio',
                               'P/E',
                               'Debt / Equity Ratio',
                               'Free Cash Flow Yield']]
        
        allData = pd.concat([allData, stockData])
    t2 = t.time()
    print('Done fetching! (%d seconds to complete)\n' % (t2 - t1))
    return allData .dropna()               



if True:
    allData = getAllData(getTickers(300))



# Later, check if stock price data looks right
if False:
    stock = allData[allData['ticker'] == 'AMZN']
    if False:
        stock = stock.reindex(index = stock.index[::-1])
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(stock['Quarter end'], stock['Price'])
        ax.set(xticks = stock['Quarter end'][::10])
        fig.autofmt_xdate()    
