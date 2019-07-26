# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:32:50 2019

@author: Liu

"""
import numpy as np
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime

start=datetime.datetime(2018,1,1)
end=datetime.datetime(2019,6,30)
apple=web.DataReader('AAPL','yahoo',start,end)
apple=apple.dropna()
apple=pd.DataFrame(apple['Adj Close'].values,index=pd.to_datetime(apple.index),columns=['Price'])
apple=np.log(apple/apple.shift(1))
apple=apple.dropna()
apple.columns=['Return']
apple.tail(3)
traindata=apple[:-3]
apple.plot()


from arch.unitroot import ADF
result=ADF(traindata.Return,max_lags=10)
print(result.summary().as_text())


from statsmodels.tsa import stattools
LjungBox=stattools.q_stat(stattools.acf(traindata)[1:12],len(traindata))
LjungBox[1][-1]


import statsmodels.graphics.tsaplots as ts
ts.plot_acf(traindata,use_vlines=True, lags=30)

