# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:24:03 2018

@author: Harrison
"""

#认购期权义务仓维持保证金＝[合约结算价+Max（12%×合约标的收盘价-认购期权虚值，7%×合约标的收盘价）]×合约单位
#认沽期权义务仓维持保证金＝Min[合约结算价 +Max（12%×合标的收盘价-认沽期权虚值，7%×行权价格），行权价格]×合约单位

def maintenance1(strikeprice,settlement,settlementoption,type1,size=10000):  
    if type1 =='call':
        outofmoney=max(strikeprice-settlement,0)
        maintenance1=(settlementoption+max(0.12*settlement-outofmoney ,0.07*settlement))*size
    elif type1=='put':
        outofmoney=max(-strikeprice+settlement,0)
        maintenance1=min(settlementoption+max(0.12*settlement-outofmoney,0.07*strikeprice),strikeprice)*size
    else:
        pass

    return maintenance1 

if __name__=='__main__':
    strikeprice=2.85 #行权价
    settlement=2.663 #期货结算价
    settlementoption=0.1870#期权结算价
    size=10000 #合约乘数
    type1='put' #期权认购认沽类型 call or put
    
    a=maintenance1(strikeprice,settlement,settlementoption,type1)
    print(a)
