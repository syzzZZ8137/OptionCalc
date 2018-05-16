# -*- coding: utf-8 -*-
"""
Created on Wed May 16 09:42:16 2018

@author: Harrison
"""
#strikeprice=3000
#step=5
#increment=0.01

import pandas as pd 
import numpy as np
from scipy.stats import norm
def Tprice(strikeprice,step,increment):
   
    S=2650
    T=30/365
    r=0.04
    q=0
    
    kk=[]
#%% 判断每步间隔大小
    if strikeprice*increment>2.5:
        incrementamount=round(increment*strikeprice/5)*5
    else:
        incrementamount=round(increment*strikeprice)
#%% 循环输出T形状列表 
    for i in range(-step,step+1):
        
        Kprice=incrementamount*i+strikeprice
        
        sigma=0.20#iv=Mysql(Kprice)
        
        ecb=round(European_Call(S,Kprice,T,sigma,r,q),4)
        epb=round(European_Put(S,Kprice,T,sigma,r,q),4)
        ecs=round(European_Call(S,Kprice,T,sigma+0.001,r,q),4)
        eps=round(European_Put(S,Kprice,T,sigma+0.001,r,q),4)
        
        K=[epb,eps,Kprice,ecb,ecs]
        kk.append(K)
    
    kk=pd.DataFrame(kk,columns=['买价','卖价','执行价','买价','卖价'])
    return kk

#%% 欧式看涨期权定价
def European_Call(S,K,T,sigma,r,q):
    
    d1 = (np.log(S/K)+(r-q+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = (np.log(S/K)+(r-q-0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    V = S*np.exp(-q*T)*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)

    return V
#%% 欧式看跌期权定价
def European_Put(S,K,T,sigma,r,q):

    d1 = (np.log(S/K)+(r-q+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = (np.log(S/K)+(r-q-0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    V =K*np.exp(-r*T)*norm.cdf(-d2)-S*np.exp(-q*T)*norm.cdf(-d1)

    return V
