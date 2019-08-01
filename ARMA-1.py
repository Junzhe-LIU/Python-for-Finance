# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 12:46:05 2019

@author: Liu
"""

import numpy as np
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime

start=datetime.datetime(2018,1,1)
end=datetime.datetime(2019,6,30)
nasdaq=web.DataReader('^IXIC','yahoo',start,end)
nasdaq=nasdaq.dropna()
nasdaq=pd.DataFrame(nasdaq['Adj Close'].values,index=pd.to_datetime(nasdaq.index),columns=['Price'])
nasdaq=(nasdaq-nasdaq.shift(1))/nasdaq.shift(1)
nasdaq=nasdaq.dropna()
nasdaq.columns=['Return']
nasdaq.tail(3)
traindata=nasdaq[:-3]

from arch.unitroot import ADF
result=ADF(traindata.Return,max_lags=10)
print(result.summary().as_text())

from statsmodels.tsa import stattools
LjungBox=stattools.q_stat(stattools.acf(traindata)[1:12],len(traindata))
LjungBox[1][-1]

import statsmodels.graphics.tsaplots as ts
ts.plot_acf(traindata,use_vlines=True, lags=30)