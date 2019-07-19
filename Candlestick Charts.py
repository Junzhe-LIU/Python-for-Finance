# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 11:12:39 2019

@author: Liu
"""

import numpy as np
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime

start=datetime.datetime(2018,1,1)
end=datetime.datetime(2019,6,30)
dowj=web.DataReader('^DJI','yahoo',start,end)
dowj.reset_index(inplace=True) # turn 'Date' from index to column#
dowj=dowj[['Date','Open','High','Low','Close']]


import matplotlib.dates as mdates
dowj.loc[:,'Date']=dowj.Date.map(mdates.date2num)

from mpl_finance import candlestick_ohlc
ax=plt.subplot()
candlestick_ohlc(ax,dowj.values, width=0.7, colorup='g', colordown='r')
ax.xaxis_date()
ax.grid(True)
plt.show()














