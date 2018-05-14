# -*- coding: utf-8 -*-
"""
Created on Tue May  8 12:37:18 2018

@author: Harrison
"""


def maintenance1(strikeprice,settlement,settlementoption,size,maintenancefuture,type1):  
    if type1 =='call':
        outofmoney=max(strikeprice-settlement,0)
    elif type1=='put':
        outofmoney=max(-strikeprice+settlement,0)
        
    else:
        pass

    maintenance1=max(settlementoption*maintenancefuture+maintenancefuture-0.5*outofmoney ,settlementoption+0.5*maintenancefuture)*size

    return maintenance1 

if __name__=='__main__':
    strikeprice=3250 #行权价
    settlement=3200 #期货结算价
    settlementoption=131.5#期权结算价
    size=10 #合约乘数
    maintenancefuture=0.07#期货保证金比例
    type1='call' #期权认购认沽类型 call or put
    
    a=maintenance1(strikeprice,settlement,settlementoption,size,maintenancefuture,type1)
    print(a)
