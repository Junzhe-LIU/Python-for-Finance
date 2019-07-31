# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 14:42:50 2019

@author: Liu
"""

import pandas as pd
import numpy as np
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime
import movingaverage as ma

start=datetime.datetime(2018,1,1)
end=datetime.datetime(2019,6,30)
costco=web.DataReader('COST','yahoo',start,end)
cos_close=costco.Close

sma10=ma.sma(cos_close,10)
smasignal=pd.Series(0,index=cos_close.index)
for i in range(10,len(cos_close)):
    if all([cos_close[i-1]<sma10[i-1],cos_close[i]>sma10[i]]):
        smasignal[i]=1
    elif all([cos_close[i-1]>sma10[i-1],cos_close[i]<sma10[i]]):
        smasignal[i]=-1

sma5=ma.sma(cos_close,5)
sma30=ma.sma(cos_close,30)
SLsignal=pd.Series(0,index=sma30.index)
for i in range(1,len(sma30)):
    if all([sma5[i-1]<sma30[i-1],sma5[i]>sma30[i]]):
        SLsignal[i]=1
    elif all([sma5[i-1]>sma30[i-1],sma5[i]<sma30[i]]):
        SLsignal[i]=-1

DIF=ma.ema(cos_close,12,2.0/(1+12))-ma.ema(cos_close,26,2.0/(1+26))
DEA=ma.ema(cos_close,9,2.0/(1+9))
MACD=DIF-DEA

macdsignal=pd.Series(0,index=DIF.index[1:])
for i in range(1,len(DIF)):
    if all ([DIF[i-1]<DEA[i-1],DIF[i]>DEA[i]]):
        macdsignal[i]=1
    elif all([DIF[i-1]>DEA[i-1],DIF[i]<DEA[i]]):
        macdsignal[i]=-1

Allsignal=smasignal+SLsignal+macdsignal
for i in Allsignal.index:
    if Allsignal[i]>1:
        Allsignal[1]=1
    elif Allsignal[i]<-1:
        Allsignal[i]=-1
    else:
        Allsignal[i]=0

tradeSig=Allsignal.shift(1).dropna()

asset=pd.Series(0.0,index=cos_close.index)
cash=pd.Series(0.0,index=cos_close.index)
share=pd.Series(0.0,index=cos_close.index)

entry=3
cash[:entry]=2000000.0
while entry<len(cos_close):
    cash[entry]=cash[entry-1]
    if all ([cos_close[entry-1]>cos_close[entry-2],\
             cos_close[entry-2]>cos_close[entry-3],Allsignal[entry-1]!=-1]):
       share[entry]=100
       cash[entry]=cash[entry]-100*cos_close[entry]
    break
entry+=1
i=entry+1
while i<len(tradeSig):
     cash[i]=cash[i-1]
     share[i]=share[i-1]
     if tradeSig[i]==1:
         share[i]=share[i]+300
         cash[i]=cash[i]-300*cos_close[i]
     if all([tradeSig[i]==-1,share[i]>=100]):
         share[i]=share[i]-100
         cash[i]=cash[i]+100*cos_close[i]
     i+=1

asset=cash+share*cos_close

plt.subplot(411)
plt.title('Trading Account Performance')
plt.plot(cos_close,color='g')
plt.ylabel('Price')
plt.subplot(412)
plt.plot(share,'b')
plt.ylabel('Share')
plt.ylim(0,max(share)+1000)
plt.subplot(413)
plt.plot(asset,color='r')
plt.ylabel('Asset')
plt.ylim(min(asset)-5000.0,max(asset)+5000.0)
plt.subplot(414)
plt.plot(cash,color='y')
plt.ylabel('Cash')
plt.ylim(0,max(cash)+5000.0)

        

