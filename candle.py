# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 13:04:33 2019

@author: Liu
"""
# Create candlePlot function to draw candlestick chart ( applicable to cases fetching data from Yahoo Finance) #

import matplotlib.pyplot as plt
import matplotlib.dates
from mpl_finance import candlestick_ohlc
from matplotlib.dates import DateFormatter,WeekdayLocator,DayLocator,MONDAY

def candlePlot(Data,title='a'):
    Data.reset_index(inplace=True)  
    Data=Data[['Date','Open','High','Low','Close']]  
    Data.loc[:,'Date']=Data.Date.map(matplotlib.dates.date2num)
    
    ax=plt.subplot()
    mondays=WeekdayLocator(MONDAY)
    weekFormatter=DateFormatter('%y %b %d')
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(DayLocator())
    ax.xaxis.set_major_formatter(weekFormatter)
    ax.set_title(title)
    
    candlestick_ohlc(ax,Data.values, width=0.7, colorup='g', colordown='r')
    plt.setp(plt.gca().get_xticklabels(),rotation=50,horizontalalignment='center')
    ax.grid(True)
    return(plt.show())