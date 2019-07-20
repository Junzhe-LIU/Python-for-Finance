# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 10:25:19 2019

@author: Liu
"""
import numpy as np
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime

start=datetime.datetime(2018,1,1)
end=datetime.datetime(2019,6,30)
ge=web.DataReader('GE','yahoo',start,end)

ge_close=ge.Close
priceChg=ge_close-ge_close.shift(1)
priceChg=priceChg.dropna()
up=pd.Series(0,index=priceChg.index)
up[priceChg>0]=priceChg[priceChg>0]
down=pd.Series(0,index=priceChg.index)
down[priceChg<0]=-priceChg[priceChg<0]
rsidata=pd.concat([ge_close,priceChg,up,down],axis=1)
rsidata.columns=['Close','PriceChange','Up','Down']
rsidata=rsidata.dropna()

SUMUP=[]
SUMDOWN=[]
for i in range(len(rsidata)-5):
    SUMUP.append(np.mean(up.values[i:(i+6)],dtype=np.float))
    SUMDOWN.append(np.mean(down.values[i:(i+6)],dtype=np.float))
rsi6=[100*SUMUP[i]/(SUMUP[i]+SUMDOWN[i]) for i in range(len(SUMUP))]
RSI6=pd.Series(rsi6,index=rsidata.index[5:])
RSI6.tail()

plt.subplot(211)
plt.plot(ge_close,'k')
plt.xlabel('Date')
plt.ylabel('Close')

plt.subplot(212)
plt.plot(RSI6,'g')
plt.xlabel('Date')
plt.ylabel('RSI6')


