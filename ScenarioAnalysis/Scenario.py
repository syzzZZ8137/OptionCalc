# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 12:27:16 2018

@author: Jax_GuoSen
"""

import numpy as np
import pandas as pd
from scipy.stats import norm
from matplotlib import pyplot as plt
import OptionCalc.ScenarioAnalysis.Option_Portfolio as OP

class Greeks_Euro:
    def __init__(self,S,r,sigma,K,T,status):
        self.info = {'und_price':S,
                     'rf':r,
                     'vol':sigma,
                     'strike':K,
                     'ttm':T,
                     'status':status}
        self.d1 = (np.log(S/K)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
        self.d2 = (np.log(S/K)+(r-0.5*sigma**2)*T)/(sigma*np.sqrt(T))
        self.c1 = -S*sigma/(2*np.sqrt(2*np.pi*T))*np.exp((-self.d1**2)/2)
        self.c2 = -r*K*np.exp(-r*T)*norm.cdf(self.d2)
        self.c3 = r*K*np.exp(-r*T)*norm.cdf(-self.d2)
        
    def cpt_delta(self):
        if self.info['status'] =='call':
            delta = norm.cdf(self.d1)
        elif self.info['status'] == 'put':
            delta = norm.cdf(self.d1)-1
        else:
            delta = np.nan
        return delta
    
    def cpt_theta(self):
        if self.info['status'] == 'call':
            theta = self.c1+self.c2
        elif self.info['status'] == 'put':
            theta = self.c1+self.c3
        else:
            theta = np.nan
        return theta
    
    def cpt_gamma(self):
        gamma = 1/(self.info['und_price']*np.sqrt(2*np.pi*(self.info['vol']**2)*self.info['ttm']))*np.exp((-self.d1**2)/2)
        return gamma
    
    
    def cpt_vega(self):
        vega = np.sqrt(self.info['ttm'])*self.info['und_price']*np.exp((-self.d1**2)/2)/np.sqrt(2*np.pi)
        return vega
    
    def cpt_rho(self):
        if self.info['status'] =='call':
            rho = self.info['strike']*self.info['ttm']*np.exp(-self.info['rf']*self.info['ttm'])*norm.cdf(self.d2)
        elif self.info['status'] == 'put':
            rho = -self.info['strike']*self.info['ttm']*np.exp(-self.info['rf']*self.info['ttm'])*norm.cdf(-self.d2)
        else:
            rho = np.nan
        return rho
    
    def cpt_vanna(self):
        #DvegaDs
        vega = self.cpt_vega()
        vanna = vega/self.info['und_price']*(1-self.d1/(self.info['vol']*np.sqrt(self.info['ttm'])))
        return vanna

    def cpt_vomma(self):
        #DvegaDvol
        vega = self.cpt_vega()
        vomma = vega*self.d1*self.d2/self.info['vol']
        return vomma
    
    def cpt_charm(self):
        #DdeltaDtime
        charm = -norm.pdf(self.d1)*(2*self.info['rf']*self.info['ttm']-self.d2*self.info['vol']*np.sqrt(self.info['ttm']))/(2*self.info['ttm']*self.info['vol']*np.sqrt(self.info['ttm']))
        return charm

    
    def cpt_veta(self):
        #DvegaDtime
        veta = self.info['und_price']*norm.pdf(self.d1)*np.sqrt(self.info['ttm'])*(self.info['rf']*self.d1/(self.info['vol']*np.sqrt(self.info['ttm']))-(1+self.d1*self.d2)/(2*self.info['ttm']))
        return veta

    def cpt_all_greeks(self):
        res = {'Delta':round(self.cpt_delta(),8),
               'Gamma':round(self.cpt_gamma(),8),
               'VegaPer%':round(self.cpt_vega()/100,8),
               'ThetaPerday':round(self.cpt_theta()/246,8),
               'RhoPer%':round(self.cpt_rho()/100,8),
               'Vanna':round(self.cpt_vanna()/100,8),
               'VommaPer%':round(self.cpt_vomma()/10000,8),
               'CharmPerday':round(self.cpt_charm()/246,8),
               'VetaPerday':round(self.cpt_veta()/24600,8)
               }
        return res
    
def scenario_analysis(option_portfolio):
    #关于greeks的情景分析
    S_lst = []
    r_lst = []
    vol_lst = []
    T_lst = []
    
    for each in option_portfolio:
        S_lst.append(each[0]['underlying price'])
        r_lst.append(each[0]['interest'])
        vol_lst.append(each[0]['volatility'])
        T_lst.append(each[1]['maturity'])
        
    
    #设置好产生离散点的序列
    S_lst = np.arange(min(S_lst)*0.7,max(S_lst)*1.3,(max(S_lst)*1.3-min(S_lst)*0.7)*0.01)
    S_sce = pd.DataFrame()
    r_lst = np.arange(min(r_lst)-0.01,max(r_lst)+0.03,0.005)
    r_sce = pd.DataFrame()
    vol_lst = np.arange(min(vol_lst)*0.7,max(vol_lst)*1.3,(max(vol_lst)*1.3-min(vol_lst)*0.7)*0.01)
    vol_sce = pd.DataFrame()
    T_lst = np.arange(0.001,min(T_lst),0.001)
    T_sce = pd.DataFrame()
    
    count = 1
    
    for each in option_portfolio:
        TMP = pd.DataFrame()
        for eachS in S_lst:
            V = Greeks_Euro(eachS,each[0]['interest'],each[0]['volatility'],each[1]['strike'],each[1]['maturity'],each[1]['type'])
            tmp = V.cpt_all_greeks()
            tmp = pd.DataFrame(tmp,index=[eachS])*each[1]['position']
            #tmp.loc[eachS,'value'] = OP.BS_formula(eachS,each[1]['strike'],each[1]['maturity'],each[0]['volatility'],each[0]['interest'],0,each[1]['type'])*each[1]['position']
            TMP = TMP.append(tmp)
        if count == 1:
            S_sce = S_sce.append(TMP)   #如果是portfilio的第一个，就用append
        else:
            S_sce = S_sce+TMP    #如果是portfilio的第一个以上，就用+
        
        TMP = pd.DataFrame()
        for eachr in r_lst:
            V = Greeks_Euro(each[0]['underlying price'],eachr,each[0]['volatility'],each[1]['strike'],each[1]['maturity'],each[1]['type'])
            tmp = V.cpt_all_greeks()
            tmp = pd.DataFrame(tmp,index=[eachr])*each[1]['position']
            #tmp.loc[eachr,'value'] = OP.BS_formula(each[0]['underlying price'],each[1]['strike'],each[1]['maturity'],each[0]['volatility'],eachr,0,each[1]['type'])*each[1]['position']
            TMP = TMP.append(tmp)
        if count == 1:
            r_sce = r_sce.append(TMP)
        else:
            r_sce = r_sce+TMP
        
        TMP = pd.DataFrame()
        for eachvol in vol_lst:
            V = Greeks_Euro(each[0]['underlying price'],each[0]['interest'],eachvol,each[1]['strike'],each[1]['maturity'],each[1]['type'])
            tmp = V.cpt_all_greeks()
            tmp = pd.DataFrame(tmp,index=[eachvol])*each[1]['position']
            #tmp.loc[eachvol,'value'] = OP.BS_formula(each[0]['underlying price'],each[1]['strike'],each[1]['maturity'],eachvol,each[0]['interest'],0,each[1]['type'])*each[1]['position']
            TMP = TMP.append(tmp)
        if count == 1:
            vol_sce = vol_sce.append(TMP)
        else:
            vol_sce = vol_sce+TMP
        
        TMP = pd.DataFrame()
        for eachT in T_lst:
            V = Greeks_Euro(each[0]['underlying price'],each[0]['interest'],each[0]['volatility'],each[1]['strike'],eachT,each[1]['type'])
            tmp = V.cpt_all_greeks()
            tmp = pd.DataFrame(tmp,index=[eachT])*each[1]['position']
            #tmp.loc[eachvol,'value'] = OP.BS_formula(each[0]['underlying price'],each[1]['strike'],eachT,each[0]['volatility'],each[0]['interest'],0,each[1]['type'])*each[1]['position']
            TMP = TMP.append(tmp)
        if count == 1:
            T_sce = T_sce.append(TMP)
        else:
            T_sce = T_sce+TMP
        
        count+=1
    S_sce = S_sce[['Delta','Gamma','VegaPer%','ThetaPerday','RhoPer%','Vanna','VommaPer%','CharmPerday','VetaPerday']]
    r_sce = r_sce[['Delta','Gamma','VegaPer%','ThetaPerday','RhoPer%','Vanna','VommaPer%','CharmPerday','VetaPerday']]
    vol_sce = vol_sce[['Delta','Gamma','VegaPer%','ThetaPerday','RhoPer%','Vanna','VommaPer%','CharmPerday','VetaPerday']]
    T_sce = T_sce[['Delta','Gamma','VegaPer%','ThetaPerday','RhoPer%','Vanna','VommaPer%','CharmPerday','VetaPerday']]
    
    return S_sce,r_sce,vol_sce,T_sce

def scenario_analysis2(option_portfolio,gapS,rangeS,gapvol,rangevol,gapT,rangeT):
    #关于组合价值的情景分析
    S_lst = []
    vol_lst = []
    T_lst = []
    
    tmp = 0
    for each in option_portfolio:
        S_lst.append(each[0]['underlying price'])
        vol_lst.append(each[0]['volatility'])
        T_lst.append(each[1]['maturity'])
        tmp += OP.BS_formula(each[0]['underlying price'],each[1]['strike'],each[1]['maturity'],each[0]['volatility'],each[0]['interest'],0,each[1]['type'])*each[1]['position']
    mid = tmp  #计算初始价格
    
    #设置好产生离散点的序列
    S_lst = np.arange(min(S_lst)*(1-gapS*rangeS),max(S_lst)*(1+gapS*rangeS),rangeS*np.mean([min(S_lst),max(S_lst)]))
    vol_lst = np.arange(min(vol_lst)*(1-gapvol*rangevol),max(vol_lst)*(1+gapvol*rangevol),rangevol*np.mean([min(vol_lst),max(vol_lst)]))
    T_lst = np.arange(min(T_lst)-gapT*rangeT*0.004,min(T_lst),0.004*rangeT)  #0.004年=1个交易日
    
    res1 = pd.DataFrame()
    res2 = pd.DataFrame()
    res3 = pd.DataFrame()

    for eachS in S_lst:
        eachS = round(eachS,3)
        for eachvol in vol_lst:
            eachvol = round(eachvol,3)
            tmp = 0
            for each in option_portfolio:
                tmp += OP.BS_formula(eachS,each[1]['strike'],each[1]['maturity'],eachvol,each[0]['interest'],0,each[1]['type'])*each[1]['position']
            res1.loc[eachS,eachvol] = tmp
            
    res11 = (res1-mid)
    
    for eachS in S_lst:
        eachS = round(eachS,3)
        for eachT in T_lst:
            eachT = round(eachT,3)
            tmp = 0
            for each in option_portfolio:
                tmp += OP.BS_formula(eachS,each[1]['strike'],eachT,each[0]['volatility'],each[0]['interest'],0,each[1]['type'])*each[1]['position']
            res2.loc[eachS,eachT] = tmp
            
    res22 = (res2-mid)
    
    for eachT in T_lst:
        eachT = round(eachT,3)
        for eachvol in vol_lst:
            eachvol = round(eachvol,3)
            tmp = 0
            for each in option_portfolio:
                tmp += OP.BS_formula(each[0]['underlying price'],each[1]['strike'],eachT,eachvol,each[0]['interest'],0,each[1]['type'])*each[1]['position']
            res3.loc[eachvol,eachT] = tmp
            
    res33 = (res3-mid)
    
    return res1,res2,res3,res11,res22,res33,mid
    
        

def plot_subplot(stamps,xlabel):
    plt.figure(figsize=(11,11))
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.9, top=0.9,wspace=0.35, hspace=0.35)

    columns = stamps.columns.tolist()
    count = 331
    for each in columns:
        ax = plt.subplot(count)
        plt.sca(ax)
        plt.plot(stamps.index.tolist(),stamps[each].tolist(),color='b')
        ax.set_title('%s V.S. %s'%(xlabel,each))
        ax.grid(True)
        count+=1
    plt.show()
    
       
        
if __name__ == '__main__':    
    #a = pd.datetime(2018,9,12)
    #b = pd.datetime(2018,10,12)
    #T = (b-a).days/365
    #S = 3346
    #K1 = 3346
    
    #sigma1 = 0.1262
    #r = 0
    #status = 'call'
    #plot_subplot(S_sce,'Underlying Price')
    #plot_subplot(vol_sce,'Volatility')
    
    
    
    market_property1 = {'underlying price':15000,'interest':0.03,\
                        'volatility':0.3,'dividend':0}
    option_property1 = {'type':'call','position':-1,\
                       'strike':17000,'maturity':0.3}
    
    market_property2 = {'underlying price':15000,'interest':0.03,\
                        'volatility':0.3,'dividend':0}
    option_property2 = {'type':'put','position':-1,\
                       'strike':13500,'maturity':0.3}
    
    option_portfolio = [[market_property1,option_property1],[market_property2,option_property2]]
    S_sce,r_sce,vol_sce,T_sce = scenario_analysis(option_portfolio)
    plot_subplot(vol_sce,'Volatility')
    
    
    res1,res2,res3,res11,res22,res33,mid = scenario_analysis2(option_portfolio,5,0.02,5,0.02,5,1)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

            
        
        
        
        
        
        