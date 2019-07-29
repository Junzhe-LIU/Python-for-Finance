# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 11:34:17 2019

@author: Liu
"""
# Raw Stochastic Value (RSV) application, period= 9 days # 

import pandas as pd
import pandas_datareader as web
import datetime
import matplotlib.pyplot as plt

start=datetime.datetime(2018,1,1)
end=datetime.datetime(2019,6,30)
costco=web.DataReader('COST','yahoo',start,end)

close=costco.Close
high=costco.High
low=costco.Low

HIGH=pd.Series(0.0, index=costco.index)
LOW=pd.Series(0.0,index=costco.index)
RSV=pd.Series(0.0,index=costco.index)

for i in range(8,len(costco)):
    HIGH[i]=high[(i-8):(i+1)].max()
    LOW[i]=low[(i-8):(i+1)].min()
    RSV[i]=100*(close[i]-LOW[i])/(HIGH[i]-LOW[i])
    
RSV=RSV[8:]
plt.plot(RSV)

