# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:48:59 2019

@author: Liu
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime

start=datetime.datetime(1990,1,1)
end=datetime.datetime(2019,6,30)
cos=web.DataReader('COST','yahoo',start,end)
cos=cos[['Open','High','Low','Close']]
cos.reset_index()

Close=cos.Close
Open=cos.Open
Diff=Close-Open
Diff.describe()

Shape=[0,0]
for i in range(2,len(Diff)):
    if all([Diff[i-2]<-0.33,abs(Diff[i-1])<0.031,Diff[i]>0,Diff[i]>abs(Diff[i-2]*0.5)]):
        Shape.append(1)
    else:
        Shape.append(0)

Doji=[0,0]
for i in range(2,len(Open)):
    if all([Open[i-1]<Open[i],Close[i-1]<Open[i],Open[i-1]<Close[i-2],Close[i-1]<Close[i-2]]):
        Doji.append(1)
    else:
        Doji.append(0)

ret=Close/Close.shift(1)-1
Trend=[0,0]
for i in range(2,len(ret)):
    if all([ret[i-1]<0,ret[i-2]<0]):
        Trend.append(1)
    else:
        Trend.append(0)

Morningstar=[]
for i in range(0,len(Trend)):
    if all([Shape[i]==1,Doji[i]==1,Trend[i]==1]):
        Morningstar.append(1)
    else:
        Morningstar.append(0)

for i in range(0,len(Morningstar)):
    if Morningstar[i]==1:
        print(cos.index[i])




    
    
        