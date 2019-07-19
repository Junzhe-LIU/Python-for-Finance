# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 08:40:46 2019

@author: Liu
"""
import numpy as np
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime

start=datetime.datetime(2018,1,1)
end=datetime.datetime(2019,6,30)
ford=web.DataReader('F','yahoo',start,end)

def momentum(price,period):
    lagprice=price.shift(period)
    momen=price-lagprice
    momen=momen.dropna()
    return(momen)
    
ford_close=ford.Close
momen60=momentum(ford_close,60)
momen60.head()

signal=[]
for i in momen60:
    if i>0:
        signal.append(1)
    else:
        signal.append(-1)

signal=pd.Series(signal,index=momen60.index)

tradeSig=signal.shift(1)
ret=ford_close/ford_close.shift(1)-1
momen60ret=(ret*tradeSig).dropna()
win=momen60ret[momen60ret>0]
loss=-momen60ret[momen60ret<0]
winrate=float(len(win))/float(len(momen60ret[momen60ret!=0]))
winrate

plt.subplot(221)
plt.plot(ret[-len(momen60ret):],'b')
plt.ylabel('return')
plt.grid(True)

plt.subplot(222)
plt.plot(momen60ret,'r')
plt.ylabel('momen60ret')
plt.grid(True)

plt.subplot(223)
win.hist()
plt.xlabel('Win')

plt.subplot(224)
loss.hist()
plt.xlabel('Loss')

performance=pd.DataFrame({'Win':win.describe(),'Loss':loss.describe()})
performance
