# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 08:25:22 2019

@author: Liu
"""
#Formation Period#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime

start=datetime.datetime(2016,1,1)
end=datetime.datetime(2017,12,31)
gm=web.DataReader('GM','yahoo',start,end)
ford=web.DataReader('F','yahoo',start,end)

gm=gm.dropna()
ford=ford.dropna()

gm=pd.Series(gm['Adj Close'].values, index=pd.to_datetime(gm.index))
ford=pd.Series(ford['Adj Close'].values, index=pd.to_datetime(ford.index))

gm.name='GM Price'
ford.name='Ford Price'

pairs=pd.concat([gm,ford],axis=1)


def SSD(priceX, priceY):
    returnX=((priceX-priceX.shift(1))/priceX.shift(1))[1:]
    returnY=((priceY-priceY.shift(1))/priceY.shift(1))[1:]
    standardX=(1+returnX).cumprod()
    standardY=(1+returnY).cumprod()
    SSD=np.sum((standardX-standardY)**2)
    return(SSD)

price_distance=SSD(gm,ford)
price_distance

returnA=((gm-gm.shift(1))/gm.shift(1))[1:]
returnB=((ford-ford.shift(1))/ford.shift(1))[1:]
standardA=(1+returnA).cumprod()
standardB=(1+returnB).cumprod()

SSD_pairs=standardB-standardA
meanSSD_pairs=np.mean(SSD_pairs)
sdSSD_pairs=np.std(SSD_pairs)
thresholdup=meanSSD_pairs+1.2*sdSSD_pairs
thresholddown=meanSSD_pairs-1.2*sdSSD_pairs

SSD_pairs.plot()
plt.axhline(y=meanSSD_pairs,color='red')
plt.axhline(y=thresholdup,color='green')
plt.axhline(y=thresholddown,color='green')

#Trading Period#

start=datetime.datetime(2018,1,1)
end=datetime.datetime(2019,7,13)
GM=web.DataReader('GM','yahoo',start,end)
FORD=web.DataReader('F','yahoo',start,end)

GM=GM.dropna()
FORD=FORD.dropna()

GM=pd.Series(GM['Adj Close'].values, index=pd.to_datetime(GM.index))
FORD=pd.Series(FORD['Adj Close'].values, index=pd.to_datetime(FORD.index))

def spread(priceX,priceY):
    returnX=((priceX-priceX.shift(1))/priceX.shift(1))[1:]
    returnY=((priceY-priceY.shift(1))/priceY.shift(1))[1:]
    standardX=(1+returnX).cumprod()
    standardY=(1+returnY).cumprod()
    spread=standardY-standardX
    return(spread)
trading_spread=spread(GM,FORD)

trading_spread.plot()
plt.axhline(y=meanSSD_pairs,color='red')
plt.axhline(y=thresholdup,color='green')
plt.axhline(y=thresholddown,color='green')    
    