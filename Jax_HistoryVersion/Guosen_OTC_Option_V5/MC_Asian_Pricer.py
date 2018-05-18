# -*- coding: utf-8 -*-
"""
Created on Tue May 15 08:38:51 2018

@author: Jax_GuoSen
"""

import numpy as np

def time_split(price_date,start_fixed_date,end_fixed_date,maturity_date):
    #输入：定价日，起均日，终均日，到期日
    #输出：三段时间及分属情况
    Ta = (maturity_date - price_date).days/365
    Tb = (maturity_date - start_fixed_date).days/365
    Tc = (maturity_date - end_fixed_date).days/365
    #分三种情况考虑
    #1.定价日位于起均日前
    #2.定价日位于起均日到终均日间
    #3.定价日位于终均日到到期日间
    if Ta>=Tb:
        sit = 1
    elif (Tc<Ta)&(Ta<Tb):
        sit = 2
    elif Ta<=Tc:
        sit = 3
    else:
        pass
    return Ta,Tb,Tc,sit

def random_gen(N=100000,TStep=1000):

    z = np.random.randn(N,TStep)

    return z


def Asian_Disc_MC(random,S,K,Ta,Tb,Tc,sit,r,sigma,q,SA,option_type,Nsamples=100000,Tsteps=1000):

    time_step = Tsteps   #计算步数
    S_path = np.zeros((Nsamples,time_step+1))
    Ret_path = np.ones((Nsamples,time_step+1))

    z = random
    dt = Ta/Tsteps

    for i in range(time_step):
        Ret_path[:,i+1] = np.exp((r-q-0.5*sigma**2)*dt+sigma*np.sqrt(dt)*z[:,i])  #产生收益率序列

    S_path[:,0] = S

    for i in range(time_step):
        S_path[:,i+1] = S_path[:,i]*Ret_path[:,i+1]     #产生股价序列

    if sit == 1:
        t1 = Ta-Tb  #定价日到起均日
        t2 = Tb-Tc  #起均日到终均日
        num_start = int(t1/Ta*Tsteps)        #起均日步数
        num_end = int(t2/Ta*Tsteps) + num_start  #终均日步数
        Ari = S_path[:,num_start:num_end].mean(axis=1)  #均值计算

    elif sit == 2:
        t1 = Tb-Ta
        t2 = Ta-Tc
        num_start = 0       #起均日步数
        num_end = int(t2/Ta*Tsteps)  #终均日步数
        Ari = S_path[:,num_start:num_end].mean(axis=1)  #均值计算
        Ari = SA*(t1/(t1+t2))+Ari*(t2/(t1+t2))

    elif sit == 3:
        Ari = np.ones(Nsamples)*SA
    else:
        pass

    #四种亚式期权的收益结构
    if option_type == '亚式/算术平均/看涨/固定':
        for i in range(len(Ari)):
            Ari[i] = Ari[i]-K if (Ari[i]-K)>0 else 0
        payoff = Ari

    elif option_type == '亚式/算术平均/看跌/固定':
        for i in range(len(Ari)):
            Ari[i] = K-Ari[i] if (K-Ari[i])>0 else 0
        payoff = Ari

    elif option_type == '亚式/算术平均/看涨/浮动':
        payoff = S_path[:,-1]-Ari
        for i in range(len(payoff)):
            payoff[i] = payoff[i] if (payoff[i])>0 else 0

    elif option_type == '亚式/算术平均/看跌/浮动':
        payoff = Ari-S_path[:,-1]
        for i in range(len(payoff)):
            payoff[i] = payoff[i] if (payoff[i])>0 else 0

    else:
        pass

    V = np.mean(np.exp(-r*Ta)*payoff)
    se = np.sqrt((np.sum(payoff**2)-Nsamples*V**2)/Nsamples/(Nsamples-1))

    return V,se