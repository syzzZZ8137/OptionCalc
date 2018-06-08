# -*- coding: utf-8 -*-
"""
Created on Tue May 15 08:38:51 2018

@author: Jax_GuoSen
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def time_split(price_date,start_fixed_date,end_fixed_date,maturity_date):
    #输入：定价日，起均日，终均日，到期日
    #输出：三段时间及分属情况
    Ta = ((maturity_date - price_date).days+1)/365
    Tb = ((maturity_date - start_fixed_date).days)/365
    Tc = ((maturity_date - end_fixed_date).days)/365
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
        
        Ari = S_path[:,num_start-1:num_end].mean(axis=1)  #均值计算
        #Ari = S_path[:,S_path.shape[1]-1]
        #print(num_start,num_end)
        #print(S_path.shape[1])

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


if __name__ == '__main__':
    
    price_date = pd.datetime(2018,5,24)
    maturity_date = pd.datetime(2018,8,22)
    start_fixed_date = pd.datetime(2018,8,22)
    end_fixed_date = pd.datetime(2018,8,22)
    Nsamples = 50000
    Tsamples = 1000
    S = 15000
    K = 15000
    r = 0.01
    sigma = 0.3
    q = 0
    SA = 15000
    OT = '亚式/算术平均/看跌/固定'
    V_Eu = 875.8
    
    result = []
    for i in range(50):
        Ta,Tb,Tc,sit = time_split(price_date,start_fixed_date,end_fixed_date,maturity_date)
        
        if Ta<=0:
            print('输入有误！请确认到期日在报价日之后！')
        elif Tb<0:
            print('输入有误！请确认到期日在起均日之后！')
        elif Tc<0:
            print('输入有误！请确认到期日在终均日之后！')
        elif Tb<Tc:
            print('输入有误！请确认终均日在起均日之后！')
        else:
            if sit==1:
                random = random_gen(Nsamples,Tsamples)
                V,se = Asian_Disc_MC(random,S,K,Ta,Tb,Tc,sit,r,sigma,q,SA,
                                     OT,Nsamples,Tsamples)
                
                print('计算结果：\t期权价格为: %.3f元\t期权费率为：%.2f%% '%(V,V/S*100))
            else:
                print('输入有误！请确认起均日在报价日之后！')
        result.append([V_Eu,V])
        print(i)
        
        
    result = pd.DataFrame(result,columns = ['Eu','Asian'])
    result.plot(kind = 'line',linewidth=2,color = 'br',grid=True)
    plt.plot(result.index,result['Eu'],color='r')
    plt.scatter(result.index,result['Asian'],marker='o',color='b')
    