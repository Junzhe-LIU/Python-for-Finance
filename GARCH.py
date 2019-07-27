# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:47:02 2019

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
traindata=nasdaq

plt.subplot(211)
plt.plot(traindata**2)
plt.xticks([])

plt.subplot(212)
plt.plot(np.abs(traindata))

from statsmodels.tsa import stattools
LjungBox=stattools.q_stat(stattools.acf(traindata**2)[1:13],len(traindata))
LjungBox[1][-1]

from arch import arch_model
am=arch_model(traindata)
model=am.fit(update_freq=0)
print(model.summary())



