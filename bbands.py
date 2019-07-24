# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 13:52:44 2019

@author: Liu
"""
# Bollinger Bands Function #

def bbands(close,period,times):
    import pandas as pd
    import numpy as np
    upband=pd.Series(0.0,index=close.index)
    midband=pd.Series(0.0,index=close.index)
    downband=pd.Series(0.0,index=close.index)
    sigma=pd.Series(0.0,index=close.index)
    for i in range(period-1,len(close)):
        midband[i]=np.nanmean(close[i-(period-1):(i+1)])
        sigma[i]=np.nanstd(close[i-(period-1):(i+1)])
        upband[i]=midband[i]+times*sigma[i]
        downband=midband[i]-times*sigma[i]
    bbands=pd.DataFrame({'Upband':upband[(period-1):],\
                        'Midband':midband[(period-1):],\
                        'Downband':downband[(period-1):],\
                        'Sigma':sigma[(period-1):]})
    return(bbands)


                        
