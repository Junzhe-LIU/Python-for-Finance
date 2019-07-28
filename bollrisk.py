# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 13:52:18 2019

@author: Liu
"""
# Bollinger Risk Function #

def bollrisk(close,multiplier):
    import bbands
    k=len(multiplier)
    overUp=[]
    belowDown=[]
    bollrisk=[]
    for i in range(k):
        BBands=bbands(close,20,multiplier[i])
        a=0
        b=0
        for j in range(len(BBands)):
            close=close[-(len(BBands)):]
            if close[j]>BBands.upband[j]:
                a+=1
            elif close[j]<BBands.upband[j]:
                b+=1
        overUp.append(a)
        belowDown.append(b)
        bollrisk.append(100*(a+b)/len(close))
    return(bollrisk)
                