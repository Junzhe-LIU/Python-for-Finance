# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 08:12:43 2019

@author: Liu
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime

start=datetime.datetime(2019,1,1)
end=datetime.datetime(2019,6,30)
nasdaq=web.DataReader('^IXIC','yahoo',start,end)
apple=web.DataReader('AAPL','yahoo',start,end)

nasdaq=nasdaq.dropna()
apple=apple.dropna()

mart=pd.Series(nasdaq['Adj Close'].values, index=pd.to_datetime(nasdaq.index))
stock=pd.Series(apple['Adj Close'].values, index=pd.to_datetime(apple.index))

mart.name='Market'
stock.name='Stock'
mart=np.log(mart/mart.shift(1))
stock=np.log(stock/stock.shift(1))

mart=mart.dropna()
stock=stock.dropna()

ret=pd.merge(pd.DataFrame(mart),pd.DataFrame(stock),left_index=True, right_index=True, how='inner')
ret.head()

rf=1.03**(1/360)-1

Eret=ret-rf
Eret.head()

import statsmodels.api as sm
model=sm.OLS(Eret.Stock,sm.add_constant(Eret.Market))

result=model.fit()
result.summary()
