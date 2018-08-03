# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:49:13 2018

@author: Harrison
"""

import SH50mantainace

import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
import scipy.stats as scs  
from scipy.stats import norm

import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
import scipy.stats as scs  
from eprogress import LineProgress

def European_Call(S,K,T,sigma,r,q):
    
    d1 = (np.log(S/K)+(r-q+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = (np.log(S/K)+(r-q-0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    V = S*np.exp(-q*T)*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)

    return V

def European_Put(S,K,T,sigma,r,q):

    d1 = (np.log(S/K)+(r-q+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = (np.log(S/K)+(r-q-0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    V =K*np.exp(-r*T)*norm.cdf(-d2)-S*np.exp(-q*T)*norm.cdf(-d1)

    return V
S0 = 2650  
r = 0.035  
sigma = 0.18 
tdays=30
T = tdays/365 
I = 1000  
K=2600
q=0

#ST1 = S0*np.exp((r - 0.5*sigma**2)*T+sigma*np.sqrt(T)*np.random.standard_normal(I))  
#plt.hist(ST1,bins = 50)  
#plt.xlabel('price')  
#plt.ylabel('ferquency')  

M = tdays*10
z = np.random.randn(M,I)
dt = T/M  
S = np.zeros((M + 1,I))  
Oprice=np.zeros((M + 1,I))
S[0] = S0  #第0行全部等于初始值
Oprice[0]=  European_Call(S[0],K,T,sigma,r,q)

for t in range(1,M+1):  
    S[t] = S[t-1]*np.exp((r-0.5*sigma**2)*dt+sigma*np.sqrt(dt)*z[t-1])  

for t in range(1,M):
    Oprice[t] = European_Call(S[t],K,T-t*dt,sigma,r,q) 























