# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 13:34:15 2019

@author: Liu
"""
import pandas as pd
import numpy as np

def sma(closeprice,k):
    sma=pd.Series(0.0,index=closeprice.index)
    for i in range(k-1,len(closeprice)):
        sma[i]=sum(closeprice[(i-k+1):(i+1)])/k
    return(sma)
    
def wna(closeprice,weight):
    k=len(weight)
    arrweight=np.array(weight)
    wma=pd.Series(0.0,index=closeprice.index)
    for i in range(k-1,len(closeprice)):
        wma[i]=sum(arrweight*closeprice[(i-k+1):(i+1)])
    return(wma)

def ema(closeprice,period,exponential):
    ema=pd.Series(0.0,index=closeprice.index)
    ema[period-1]=np.mean(closeprice[:period])
    for i in range(period,len(closeprice)):
        ema[i]=exponential*closeprice[i]+(1-exponential)*ema[period-1]
    return(ema)
