# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 08:22:08 2019

@author: Liu
"""
#Application of Markowitz Mean-Variance Model in portfolio selection#


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime
selected=['KO','GE','BA','TSLA','AAPL','BABA','F']
stocks=web.DataReader(selected,'yahoo',datetime.datetime(2014,5,1),datetime.date.today())
stocks.to_csv('.\\out\\ stocks.csv')

lists=pd.read_csv('C:\\stocks.csv')
lists.iloc[:,-7:]
indexs=lists.iloc[:,0]
aapl=lists.iloc[:,-7]
ba=lists.iloc[:,-6]
baba=lists.iloc[:,-5]
f=lists.iloc[:,-4]
ge=lists.iloc[:,-3]
ko=lists.iloc[:,-2]
tsla=lists.iloc[:,-1]
prices=pd.concat([indexs,aapl,ba,baba,f,ge,ko,tsla],axis=1)
prices.columns=['Date','AAPL','BA','BABA','F','GE','KO','TSLA'] 
cleandata=prices.drop(prices.index[0:2])
cleandata.index=cleandata.loc[:,'Date']  
cleandata.pop('Date')
cleandata.index=pd.to_datetime(cleandata.index)
cleandata=cleandata.dropna()
cleandata=pd.DataFrame(cleandata, dtype=float) 
normalized_returns=cleandata.pct_change() 


normalized_returns.hist(bins=50, figsize=(12,9))
normalized_returns.plot()
normalized_returns.corr()

year_return=normalized_returns.mean()*252
year_volatility=normalized_returns.cov()*252
number_of_assets=len(selected)
portfolio_returns=[]
portfolio_volatility=[]
sharpe_ratio=[]
stock_weights=[]
num_of_combinations_of_imiginary_portfolios=50000

for p in range(num_of_combinations_of_imiginary_portfolios):
    weights=np.random.random(number_of_assets)
    weights/=np.sum(weights)
    ret=np.dot(weights,year_return)
    volatility=np.sqrt(np.dot(weights.T,np.dot(year_volatility,weights)))
    sharpe=ret/volatility
    portfolio_returns.append(ret)
    portfolio_volatility.append(volatility)
    sharpe_ratio.append(sharpe)
    stock_weights.append(weights)
    

portfolio={'Returns':portfolio_returns,'Volatility':portfolio_volatility,'Sharpe Ratio':sharpe_ratio}
for counter,symbol in enumerate(selected):
    portfolio[symbol+' Weight']=[Weight[counter] for Weight in stock_weights]
df=pd.DataFrame(portfolio)
column_order=['Returns','Volatility','Sharpe Ratio']+[stock+' Weight' for stock in selected]
df=df[column_order]
df.head()

plt.style.use('seaborn-dark')
df.plot.scatter(x='Volatility',y='Returns',c='Sharpe Ratio',cmap='RdYlGn', edgecolors='black', figsize=(15,10), grid=True)
plt.xlabel('Standard Deviation')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
plt.show()

def statistics(weights): 
    weights=np.array(weights)
    pret=np.dot(weights,year_return)
    pvol=np.sqrt(np.dot(weights.T,np.dot(year_volatility,weights)))
    sharpe_ratio=pret/pvol
    return np.array([pret,pvol,sharpe_ratio])


import scipy.optimize as sco

def neg_sharpe(weights):
    return -statistics(weights)[2]

def max_sharpe_ratio(weights):
    cons=({'type':'eq','fun':lambda x:np.sum(x)-1})
    bons=tuple((0.0,1.0) for x in range(number_of_assets))
    result=sco.minimize(neg_sharpe, number_of_assets*[1./number_of_assets,],method='SLSQP',bounds=bons,constraints=cons)
    return result

optimal_port_sharpe=max_sharpe_ratio(weights)
pd.DataFrame([round(x,2) for x in optimal_port_sharpe['x']],index=selected).T

def portfolio_variance(weights):
    return statistics(weights)[1]**2

def min_portfolio_variance(weights):
    cons=({'type':'eq','fun':lambda x:np.sum(x)-1})
    bons=tuple((0.0,1.0) for x in range(number_of_assets))
    result=sco.minimize(portfolio_variance, number_of_assets*[1./number_of_assets,],method='SLSQP',bounds=bons,constraints=cons)
    return result

min_port_variance=min_portfolio_variance(weights)

statistics(optimal_port_sharpe['x']).round(3)
statistics(min_port_variance['x']).round(3)


tar_return=[]
def optimal_weights(tar_return):
    con=({'type':'eq','fun':lambda x:statistics(x)[0]-tar_return},{'type':'eq','fun':lambda x:np.sum(x)-1})
    bons=tuple((0.0,1.0) for x in range(number_of_assets))
    res=sco.minimize(portfolio_variance,number_of_assets*[1./number_of_assets,],method='SLSQP',bounds=bons,constraints=con)
    return pd.DataFrame([round(x,2) for x in res['x']],index=selected).T

tar_return=0.003 
optimal_weights(tar_return)

    

