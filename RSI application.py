# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 09:21:47 2019

@author: Liu
"""

import numpy as np
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime

start=datetime.datetime(2018,1,1)
end=datetime.datetime(2019,6,30)
costco=web.DataReader('COST','yahoo',start,end)
cos_close=costco.Close

def rsi(price,period):
    import pandas as pd
    priceChg=price-price.shift(1)
    priceChg=priceChg.dropna()
    up=pd.Series(0,index=priceChg.index)
    up[priceChg>0]=priceChg[priceChg>0]
    down=pd.Series(0,index=priceChg.index)
    down[priceChg<0]=-priceChg[priceChg<0]
    rsidata=pd.concat([price,priceChg,up,down],axis=1)
    rsidata.columns=['Close','PriceChange','Up','Down']
    rsidata=rsidata.dropna()
    
    SUMUP=[]
    SUMDOWN=[]
    for i in range(period,len(rsidata)+1):
        SUMUP.append(np.mean(up.values[(i-period):i],dtype=np.float))
        SUMDOWN.append(np.mean(down.values[(i-period):i],dtype=np.float))
    rsi=[100*SUMUP[i]/(SUMUP[i]+SUMDOWN[i]) for i in range(len(SUMUP))]
    rsi=pd.Series(rsi,index=rsidata.index[(period-1):])
    return(rsi)

rsi6=rsi(cos_close,6)
rsi24=rsi(cos_close,24)

sig1=[]
for i in rsi6:
    if i>80:
        sig1.append(-1)
    elif i<20:
        sig1.append(1)
    else:
        sig1.append(0)

sig1=pd.Series(sig1,index=rsi6.index)

sig2=pd.Series(0,index=rsi24.index)
lagrsi6=rsi6.shift(1)
lagrsi24=rsi24.shift(1)
for i in rsi24.index:
    if (rsi6[i]>rsi24[i]) & (lagrsi6[i]<lagrsi24[i]):
        sig2[i]=1
    elif(rsi6[i]<rsi24[i]) & (lagrsi6[i]>lagrsi24[i]):
        sig2[i]=-1

sig=sig1+sig2
sig[sig>=1]=1
sig[sig<=-1]=-1
sig=sig.dropna()
tradesig=sig.shift(3)
ret=cos_close/cos_close.shift(1)-1
ret=ret[tradesig.index]

buy=tradesig[tradesig==1]
buyret=ret[tradesig==1]*buy



sell=tradesig[tradesig==-1]
sellret=ret[tradesig==-1]*sell

traderet=ret*tradesig
traderet=traderet.dropna()
traderet[traderet==(-0)]=0
winrate=float(len(traderet[traderet>0]))/float(len(traderet[traderet!=0]))
winrate

cumstock=np.cumprod(1+ret)-1
cumtrade=np.cumprod(1+traderet)-1
plt.subplot(211)
plt.plot(cumstock)
plt.title('CUMSTOCK RETURN')
plt.subplot(212)
plt.plot(cumtrade)
plt.title('CUM RSI RETURN')
