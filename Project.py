#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 19:14:28 2022

@author: theju
"""

import pandas as pd

df = pd.read_excel( "/Users/theju/Desktop/USD/Business Analytics Fund./Portfolio.xlsx")

import requests
from bs4 import BeautifulSoup
from datetime import date
import schedule
import time

mystocks = list(df.Tickr)
stockdata = []

def getData (symbol) :

    headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    url= f'https://finance.yahoo.com/quote/{symbol}' 
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    t = time.localtime()
    stock = {
    'Current Date' : date.today(), 
    'Current Time' : time.strftime("%H:%M:%S", t) , 
    'Tickr': symbol,
    'Closing_Price': soup.find('div', {'class': 'D(ib) Mend(20px)'}) .find_all('fin-streamer')[0].text,
    'Change': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[1].text,
    'Difference': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[2].text,
    }
    return stock

for tickr in mystocks:
    stockdata.append(getData(tickr))
    print ("Getting: ", tickr)

print(stockdata)

schedule.every().day.at("16:00").do(getData)

dfoutput = pd.DataFrame (stockdata, columns = ['Current Date', 'Current Time', 'Tickr', 'Closing_Price', 'Change', 'Difference'])
df_join = pd.merge(df, dfoutput, how = 'inner', on='Tickr')
df_join['Closing_Price'] = pd.to_numeric(df_join['Closing_Price'], errors='coerce')
df_join['Change'] = pd.to_numeric(df_join['Change'], errors='coerce')

df_join ['Market Value']= df_join ['Number_of_Shares']* df_join ['Closing_Price']
 
df_join.to_excel("/Users/theju/Desktop/USD/Business Analytics Fund./Output.xlsx", sheet_name = "Stock Prices") 

import datetime as dt
from matplotlib import pyplot as plt
from matplotlib import style
from pandas_datareader import data as pd

start = dt.datetime(2022, 1, 1)
end = dt. datetime (2022 ,12, 30)

Apple = pd.DataReader("AAPL", "yahoo", start, end)
Google = pd.DataReader("GOOG", "yahoo", start, end)
Microsoft = pd.DataReader("MSFT", "yahoo", start, end)
Disney = pd.DataReader("DIS", "yahoo", start, end)
Tesla = pd.DataReader("TSLA", "yahoo", start, end)

style.use('ggplot')
Apple['Close'].plot(figsize = (8,8), label= "Apple")
Google['Close'].plot(figsize = (8,8), label= "Google")
Microsoft['Close'].plot(figsize = (8,8), label= "Microsoft")
Disney['Close'].plot(figsize = (8,8), label= "Disney")
Tesla['Close'].plot(figsize = (8,8), label= "Tesla")
plt.title('Portfolio Stocks Chart')
plt.legend (loc= 'lower right')
plt.ylabel("Closing Price $", fontsize =10)
plt.xlabel("Date", fontsize =10)
# plt.grid(color= 'black', linestyle= '--', linewidth = 1)
plt.show()

