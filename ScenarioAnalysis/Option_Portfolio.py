# -*- coding: utf-8 -*-
"""
Created on Tue May 15 08:48:34 2018

@author: Jax_GuoSen
"""

import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.optimize import fsolve  
from matplotlib import pyplot as plt
from IPython.display import display

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




def BS_formula(S,K,T,sigma,r,q,Otype):

    if Otype == 'call':

        V = European_Call(S,K,T,sigma,r,q)

    elif Otype =='put':

        V = European_Put(S,K,T,sigma,r,q)

    else:
        pass

    return V

