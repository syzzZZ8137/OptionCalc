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

def US_Call(S,K,T,sigma,r,q):
    #Barone Adesi Whaley
    b = r-q
    M = 2*r/(sigma**2)
    N = 2*b/(sigma**2)
    X = 1-np.exp(-r*T)
    q2 = (-(N-1)+np.sqrt((N-1)**2+4*M/X))/2

    def root_find(SS):
        d11 = (np.log(SS/K)+(b+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
        LHS = SS-K
        RHS = European_Call(SS,K,T,sigma,r,q) + (1-np.exp((b-r)*T)*norm.cdf(d11))*SS/q2
        diff = LHS - RHS
        return diff
    SS = fsolve(root_find,S)[0]
    d11 = (np.log(SS/K)+(b+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    A2 = SS/q2*(1-np.exp((b-r)*T)*norm.cdf(d11))
    if S<SS:
        V = European_Call(S,K,T,sigma,r,q)+A2*(S/SS)**q2
    else:
        V = S-K

    return V


def US_Put(S,K,T,sigma,r,q):
    #Barone Adesi Whaley
    b = r-q
    M = 2*r/(sigma**2)
    N = 2*b/(sigma**2)
    X = 1-np.exp(-r*T)
    q1 = (-(N-1)-np.sqrt((N-1)**2+4*M/X))/2

    def root_find(SS):
        d11 = (np.log(SS/K)+(b+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
        LHS = K - SS
        RHS = European_Put(SS,K,T,sigma,r,q) - (1-np.exp((b-r)*T)*norm.cdf(-d11))*SS/q1
        diff = LHS - RHS
        return diff
    SS = fsolve(root_find,S)[0]
    d11 = (np.log(SS/K)+(b+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    A1 = -SS/q1*(1-np.exp((b-r)*T)*norm.cdf(-d11))
    if S>SS:
        V = European_Put(S,K,T,sigma,r,q)+A1*(S/SS)**q1
    else:
        V = K-S

    return V


def BS_formula(market_property,option_property):

    S = market_property['underlying price']
    r = market_property['interest']
    sigma = market_property['volatility']
    q = market_property['dividend']
    K = option_property['strike']
    T = option_property['maturity']
    Otype = option_property['type']
    if Otype == '欧式/看涨':

        V = European_Call(S,K,T,sigma,r,q)

    elif Otype =='欧式/看跌':

        V = European_Put(S,K,T,sigma,r,q)

    elif Otype =='美式/看涨':

        V = US_Call(S,K,T,sigma,r,q)

    elif Otype =='美式/看跌':

        V = US_Put(S,K,T,sigma,r,q)

    elif Otype =='标的资产':

        V = European_Call(S,0.0001,T,sigma,r,q)

    else:
        pass

    return V

def payoff_search(market_property,option_property,K_limit,T_limit):

    OT = option_property['type']
    S = market_property['underlying price']
    K = option_property['strike']
    T = option_property['maturity']
    
    final_price = list(np.arange(K_limit[0]*0.85,K_limit[1]*1.15,(K_limit[1]*1.15-K_limit[0]*0.85)/500))
    S_T = pd.DataFrame(final_price,columns=['priceT'])
    if T_limit == T:
        if (OT == '欧式/看涨') or (OT == '美式/看涨'):
            S_T['payoff'] = S_T['priceT']-K
            S_T['payoff'] = S_T['payoff'].apply(lambda x:max(x,0))
        elif (OT == '欧式/看跌') or (OT == '美式/看跌'):
            S_T['payoff'] = K - S_T['priceT']
            S_T['payoff'] = S_T['payoff'].apply(lambda x:max(x,0))
        elif OT == '标的资产':
            S_T['payoff'] = S_T['priceT']
    
        else:
            pass
    
    else:
        T = T - T_limit
        #print(T_limit)
        sigma = market_property['volatility']
        r = market_property['interest']
        q = market_property['dividend']
        
        if OT == '欧式/看涨':
            S_T['payoff'] = S_T['priceT'].apply(lambda x:European_Call(x,K,T,sigma,r,q))
        elif OT == '欧式/看跌':
            S_T['payoff'] = S_T['priceT'].apply(lambda x:European_Put(x,K,T,sigma,r,q))
        elif OT == '美式/看涨':
            S_T['payoff'] = S_T['priceT'].apply(lambda x:US_Call(x,K,T,sigma,r,q))
        elif OT == '美式/看跌':
            S_T['payoff'] = S_T['priceT'].apply(lambda x:US_Put(x,K,T,sigma,r,q))
        elif OT == '标的资产':
            S_T['payoff'] = S_T['priceT']
        else:
            pass
        
    return S_T


def cal_opt_port(option_portfolio):

    portfolio_payoff = []
    V_price = []
    
    K_lst = []
    for i in range(len(option_portfolio)):
        K_lst.append(option_portfolio[i][1]['strike'])
    
    T_lst = []
    for i in range(len(option_portfolio)):
        T_lst.append(option_portfolio[i][1]['maturity'])
    #print(K_lst)
    K_limit = [min(K_lst),max(K_lst)]
    T_limit = min(T_lst)
    
    
    for each in option_portfolio:
        V = each[1]['position']*BS_formula(each[0],each[1])
        V_price.append(V)
        payoff = payoff_search(each[0],each[1],K_limit,T_limit)
        payoff['payoff'] = payoff['payoff']*each[1]['position'] - V
        portfolio_payoff.append(payoff)

    port_sum = portfolio_payoff[0]

    if len(portfolio_payoff)> 1:
        for i in range(len(portfolio_payoff)-1):
            port_sum = port_sum.merge(portfolio_payoff[i+1],on='priceT',how='inner')
        port_sum.set_index('priceT',inplace=True)
        port_sum['sum'] = np.sum(port_sum,axis=1)
        port_sum = port_sum['sum'].reset_index()

    return portfolio_payoff,port_sum,V_price,T_limit

def option_portfolio_main(option_portfolio,strategy_name = '期权组合收益结构'):
    fig = plt.figure(figsize=(8,5))
    ax=fig.gca()

    portfolio_payoff,port_sum,V_price,T_limit = cal_opt_port(option_portfolio)
    legend=[]
    i = 0
    for each in portfolio_payoff:
        ax.plot(each['priceT'],each['payoff'],'-',linewidth=2,markersize=10)
        legend.append(i+1)
        i+=1

    if len(option_portfolio)>1:
        #画合成后的
        ax.plot(port_sum['priceT'],port_sum['sum'],'-',linewidth=2,markersize=10)
        legend.append('Combo')

    ax.grid(color='black',linestyle='--',linewidth=0.5)
    ax.set_title(strategy_name+'\n',fontsize=14)
    ax.legend(legend)
    
    in_put1 = [int(round(T_limit*365)),\
               option_portfolio[0][0]['underlying price'],\
               '%.2f%%'%(option_portfolio[0][0]['interest']*100)]
    in_put2 = []
    for i in range(len(option_portfolio)):
        
        if option_portfolio[i][1]['position']<0:
            in_put2.append(['期权%d'%(i+1),-round(V_price[i],4),\
                            '%.2f%%'%(-round(V_price[i],4)/abs(option_portfolio[i][1]['position'])/option_portfolio[0][0]['underlying price']*100),\
                            option_portfolio[i][1]['type'],\
                            option_portfolio[i][1]['strike'],\
                        '%.2f%%'%(option_portfolio[i][0]['volatility']*100),\
                        '卖出',abs(option_portfolio[i][1]['position'])])
        else:
            in_put2.append(['期权%d'%(i+1),round(V_price[i],4),\
                            '%.2f%%'%(round(V_price[i],4)/abs(option_portfolio[i][1]['position'])/option_portfolio[0][0]['underlying price']*100),\
                            option_portfolio[i][1]['type'],\
                            option_portfolio[i][1]['strike'],\
                        '%.2f%%'%(option_portfolio[i][0]['volatility']*100),\
                        '买入',abs(option_portfolio[i][1]['position'])])
    
    in_put1 = pd.DataFrame(in_put1,index=['到期天数','标的价格','无风险利率'],columns=['市场信息']).T
    in_put2 = pd.DataFrame(in_put2,columns=['期权序号','期权价格','期权费率','期权类型','行权价','波动率','方向','头寸'])
    in_put2.set_index('期权序号',inplace=True)
    
    display(in_put1)
    display(in_put2)
    print('组合价格为：%.4f'%sum(V_price))
    
    print('到期期权损益图如下：')
    return port_sum

if __name__ == '__main__':
    market_property = {'underlying price':10000,'interest':0.05,\
                   'volatility':0.1,'dividend':0}
    option_property1 = {'type':'欧式/看涨','position':-1,\
                       'strike':10000,'maturity':0.75}
    option_property2 = {'type':'欧式/看涨','position':1,\
                       'strike':10000,'maturity':0.25}
    option_portfolio = [[market_property,option_property1],[market_property,option_property2]]
    
    port_sum = option_portfolio_main(option_portfolio,'Bull Strategy')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

