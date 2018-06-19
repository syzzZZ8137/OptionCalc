# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 14:17:37 2018

@author: Harrison
"""
import OptionCalc.Guosen_OTC_Option_RT.PyMySQLreadZH as PyMySQLreadZH
import pandas as pd
def GetContract(exchange,contract):
    nowday=pd.datetime.now().date()
    strall="SELECT * FROM futurexdb.contractinfo where exchange_symbol='"+exchange+"' and underlying_symbol='"+contract+"';"
    a=PyMySQLreadZH.dbconn(strall)
    contractlist=[]
    for i in range( a.shape[0]):
        if a.expiration[i]>nowday:
            contractlist.append(a.contract_symbol[i])
    return contractlist

if __name__ == '__main__':
    print(GetContract('DCE','C'))