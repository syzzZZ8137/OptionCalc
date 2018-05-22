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

def Tprice(strikeprice,step,increment,temp_input):
    '''ATM strikeprice'''
    '''上下实虚档数'''
    '''档数步幅'''
   
    S=temp_input[0]
    T=temp_input[1]
    r=temp_input[2]
    q=temp_input[3]
    
    kk=[]
#%% 判断每步间隔大小
    if strikeprice*increment>2.5:
        incrementamount=round(increment*strikeprice/5)*5
    else:
        incrementamount=round(increment*strikeprice)
#%% 循环输出T形状列表 
    for i in range(-step,step+1):
        
        Kprice=incrementamount*i+strikeprice
        
        sigma_buy = temp_input[4]#iv=Mysql(Kprice)
        sigma_sell = temp_input[5]#iv=Mysql(Kprice)
        ecb=round(European_Call(S,Kprice,T,sigma_buy,r,q),4)
        epb=round(European_Put(S,Kprice,T,sigma_buy,r,q),4)
        ecs=round(European_Call(S,Kprice,T,sigma_sell,r,q),4)
        eps=round(European_Put(S,Kprice,T,sigma_sell,r,q),4)
        
        K=[epb,eps,Kprice,ecb,ecs]
        kk.append(K)
    
    kk=pd.DataFrame(kk,columns=['看跌买价','看跌卖价','执行价','看涨买价','看涨卖价'])
    kk = kk.sort_values(by='执行价',axis=0,ascending=False)
    kk.reset_index(inplace=True,drop=True)
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

if __name__ == '__main__':  
    temp_input = [1000,30/365,0.04,0,0.2,0.3] #temp_input = [S,T,r,q,buy_sigma,sell_sigma]
    temp_output = Tprice(1000,5,0.01,temp_input)
    #print(temp_output)

