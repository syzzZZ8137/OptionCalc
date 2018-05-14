# -*- coding: utf-8 -*-
"""
Created on Mon May 14 09:38:47 2018

@author: Jax_GuoSen
"""

import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import os 

#读出
def dbconn(sql_query):
    connection = pymysql.connect(host='www.sycamore.xyz', port=3307, user='intern', passwd='9Jh4tWAFp2K6')
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_query)
    
    data_dict=cursor.fetchall()
    connection.close
    
    col_names = list(data_dict[1].keys())
    data = pd.DataFrame(data_dict,columns=col_names)
    
    return data


data=dbconn("select barra_factor,expo from cbaas.fund_holding_analysis where barra_date='20170630' and fund_id='249258'")


