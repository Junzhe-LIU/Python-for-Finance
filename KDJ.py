# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 15:10:41 2019

@author: Liu
"""

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
RSV1=pd.Series([50,50],index=costco[6:8]).append(RSV)

Kvalue=pd.Series(0.0,index=RSV1.index)
Kvalue[0]=50
for i in range(1,len(RSV1)):
    Kvalue[i]=2/3*Kvalue[i-1]+RSV1[i]/3

Dvalue=pd.Series(0.0,index=RSV1.index)
Dvalue[0]=50
for i in range(1,len(RSV1)):
    Dvalue[i]=2/3*Dvalue[i-1]+Kvalue[i]/3
    
Jvalue=3*Kvalue-2*Dvalue



