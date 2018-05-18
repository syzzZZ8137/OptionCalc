# -*- coding: utf-8 -*-
"""
Created on Tue May 15 08:47:23 2018

@author: Jax_GuoSen
"""

from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import time
from ipywidgets import *
from IPython.display import display,clear_output,display_html
import OptionCalc.Guosen_OTC_Option.MC_Asian_Pricer as MC
import OptionCalc.Guosen_OTC_Option.Option_Portfolio as OP

#%%
#期权组合界面
def on_btnOptPort_clicked(p):
    clear_output()
    
    now = datetime.now()
    f = now + timedelta(days=90)  #90天后日期

    price_date = widgets.DatePicker(
        description='期权报价日:',
        disabled=False,
        value=now.date(),
        tooltip=u'计算期权价格的日期，默认今天'
    )

    maturity_date = widgets.DatePicker(
        description='期权到期日:',
        disabled=False,
        value=f.date()
    )

    S = widgets.FloatText(
        value=15000,
        description='标的价格:',
        disabled=False,
        step=1,  #快捷变换间隔
        tooltip=u'待选期权种类'

    )
    
    r = widgets.FloatText(
        value=0.01,
        description='无风险利率:',
        disabled=False,
        step=0.01
    )
    
    

    option_type1 = widgets.Dropdown(
        options=['欧式/看涨',
                 '欧式/看跌',
                 '美式/看涨',
                 '美式/看跌',
                 '标的资产',
                 '无'],
        value='欧式/看涨',
        description=u'期权1:',
        disabled=False,
        continuous_update=True,
    )

    K1 = widgets.BoundedFloatText(
        value=15000,
        description='行权价:',
        disabled=False,
        step=1,
        min=0.01,
        max=1000000000
    )
    
    sigma1 = widgets.BoundedFloatText(
        value=0.3,
        description='波动率:',
        disabled=False,
        step=0.01,
        min = 0
    )
    
    direction1 = widgets.Dropdown(
        options=['买入', '卖出'],
        description='方向:',
        disabled=False,
        value = '买入',
        continuous_update=True
    )
    
    position1 = widgets.BoundedIntText(
        value=1,
        min=0,
        description='头寸:',
        disabled=False,
        step=1
    )

    option_type2 = widgets.Dropdown(
        options=['欧式/看涨',
                 '欧式/看跌',
                 '美式/看涨',
                 '美式/看跌',
                 '标的资产',
                 '无'],
        value='无',
        description=u'期权2:',
        disabled=False,
        continuous_update=True,
    )

    K2 = widgets.BoundedFloatText(
        value=15000,
        description='行权价:',
        disabled=False,
        step=1,
        min=0.01,
        max=1000000000
    )
    
    sigma2 = widgets.BoundedFloatText(
        value=0.3,
        description='波动率:',
        disabled=False,
        step=0.01,
        min = 0
    )
    
    direction2 = widgets.Dropdown(
        options=['买入', '卖出'],
        description='方向:',
        disabled=False,
        value = '买入',
        continuous_update=True
    )
    
    position2 = widgets.BoundedIntText(
        value=1,
        min=0,
        description='头寸:',
        disabled=False,
        step=1
    )


    option_type3 = widgets.Dropdown(
        options=['欧式/看涨',
                 '欧式/看跌',
                 '美式/看涨',
                 '美式/看跌',
                 '标的资产',
                 '无'],
        value='无',
        description=u'期权3:',
        disabled=False,
        continuous_update=True,
    )

    K3 = widgets.BoundedFloatText(
        value=15000,
        description='行权价:',
        disabled=False,
        step=1,
        min=0.01,
        max=1000000000
    )
    
    sigma3 = widgets.BoundedFloatText(
        value=0.3,
        description='波动率:',
        disabled=False,
        step=0.01,
        min = 0
    )
    
    direction3 = widgets.Dropdown(
        options=['买入', '卖出'],
        description='方向:',
        disabled=False,
        value = '买入',
        continuous_update=True
    )
    
    position3 = widgets.BoundedIntText(
        value=1,
        min=0,
        description='头寸:',
        disabled=False,
        step=1
    )
    
    tips = widgets.Label(value="全部配置完成后，单击 【计算期权组合价格】。若想清空组合或返回，请单击【重置】。")
    tips1 = widgets.Label(value=" ") #产生一个空行
    tips2 =  widgets.HTML(value="<head><b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          版本号：1.0.0</b></head></div>")
    tips3 = widgets.Label(value=" ") #产生一个空行
    #排版
    public_info_sub1 = widgets.HBox([price_date,maturity_date,tips2])
    public_info_sub2 = widgets.HBox([S,r,tips3])
    public_info = widgets.VBox([public_info_sub1,public_info_sub2,tips1])
    
    private_info1 = widgets.VBox([option_type1,K1,sigma1,direction1,position1])
    private_info2 = widgets.VBox([option_type2,K2,sigma2,direction2,position2])
    private_info3 = widgets.VBox([option_type3,K3,sigma3,direction3,position3])
    
    private_info = widgets.HBox([private_info1,private_info2,private_info3])
    global option_portfolio,container_option_info
    
    
    container_option_info = widgets.VBox([public_info,private_info,tips])
    
    option_portfolio = []
    
    #判断期权类型是否为“无”，若是，则加入。
    def entry_combos(private_info):
        if private_info.children[0].value=='无':
            pass
        else:
            if private_info.children[3].value == '卖出':
                pos = -private_info.children[4].value
            else:
                pos = private_info.children[4].value
            #加入组合库
            market_property = {'underlying price':S.value,'interest':r.value,\
                               'volatility':private_info.children[2].value,'dividend':0}
            option_property = {'type':private_info.children[0].value,'position':pos,\
                               'strike':private_info.children[1].value,'maturity':((maturity_date.value - price_date.value).days+1)/365}
            option_portfolio.append([market_property,option_property])
    
    
    
    #计算按钮
    btn_preorder = widgets.Button(
        description=u'计算期权组合价格',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击计算已选定组合的期权价格',
        icon='check'
    )

    def on_btnPreorder_clicked(p):
        #clear_output()
        global option_portfolio,container_option_info
        entry_combos(private_info1)
        entry_combos(private_info2)
        entry_combos(private_info3)
        
        if len(option_portfolio)==0:
            print('无添加任何期权信息')
        else:
            port_sum = OP.option_portfolio_main(option_portfolio,strategy_name = 'PnL')
        option_portfolio = []  #清空本次记录
        
    #重置，返回上一步界面
    btn_init = widgets.Button(
        description=u'重置',
        disabled=False,
        button_style='success', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击返回上一单元',
        icon='check'
    )
    
    def init(p):
        display_()
    
    
    btn_preorder.on_click(on_btnPreorder_clicked)
    btn_init.on_click(init)
    
    display(container_option_info)

    select = HBox([btn_preorder,btn_init])
    display(select)

#%%
#亚式期权界面
def on_btnAsian_clicked(p):
    clear_output()

    now = datetime.now()
    f = now + timedelta(days=90)  #90天后日期

    price_date = widgets.DatePicker(
        description='期权报价日',
        disabled=False,
        value=now.date()
    )

    start_fixed_date = widgets.DatePicker(
        description='期权起均日',
        disabled=False,
        value=now.date()
    )
    end_fixed_date = widgets.DatePicker(
        description='期权终均日',
        disabled=False,
        value=f.date()
    )
    maturity_date = widgets.DatePicker(
        description='期权到期日',
        disabled=False,
        value=f.date()
    )

    tips1 = widgets.Label(value="【期权起均日】 至 【期权终均日】，意为亚式期权平均值累计(采价)区间。")
    
    option_type = widgets.Dropdown(
        options=['亚式/看涨',
                 '亚式/看跌'],
        value='亚式/看跌',
        description=u'期权种类',
        disabled=False,
        continuous_update=True,

    )
    
    tips2 = widgets.Label(value="国内目前“保险+期货”项目多为看跌。")

    S = widgets.FloatText(
        value=15000,
        description='标的价格:',
        disabled=False,
        step=1,  #快捷变换间隔

    )
#    SA = widgets.FloatText(
#        value=0,
#        description='当前均价:',
#        disabled=False,
#        step=1,
#
#    )
    #tips3 = widgets.Label(value='【当前均价】 用于期权起均日在期权报价日之前，则此时该期权已累计部分均价点。若起均日在报价日当天或之后，则该项可选0。')

    K = widgets.FloatText(
        value=15000,
        description='行权价:',
        disabled=False,
        step=1
    )
    sigma = widgets.FloatText(
        value=0.3,
        description='波动率:',
        disabled=False,
        step=0.01,
        min = 0
    )
    r = widgets.FloatText(
        value=0.01,
        description='无风险利率:',
        disabled=False,
        step=0.01
    )
    
#    q = widgets.FloatText(
#        value=0.0,
#        description='股息率:',
#        disabled=False,
#        step=0.01
#    )
#
#    Nsamples = widgets.BoundedIntText(
#        value=50000,
#        description='MC样本量:',
#        disabled=False,
#        step=10000,
#        max = 200000,
#        min = 10000
#    )
#    Tsamples = widgets.BoundedIntText(
#        value=1000,
#        description='MC步数:',
#        disabled=False,
#        step=100,
#        max = 20000,
#        min = 100
#    )
    tips3 =  widgets.HTML(value="<head><b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          版本号：1.0.0</b></head></div>")
    date_info = widgets.HBox([price_date,maturity_date,tips3])
    date_info2 = widgets.HBox([start_fixed_date,end_fixed_date])
    info1 = widgets.HBox([S,K])
    info2 = widgets.HBox([r,sigma])
    
    container_option_info = widgets.VBox([date_info,date_info2,tips1,
                                          option_type,tips2,info1,info2])
    global count#记录计算次数
    count = 1
    #计算按钮
    btn_preorder = widgets.Button(
        description=u'计算期权价格',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击计算价格，由于为蒙特卡洛算法，可能消耗一定时间，请耐心等待！',
        icon='check'
    )

    def on_btnPreorder_clicked(p):
        #clear_output()
        global container_option_info   #加全局变量
        global count
        #global count
        print('正在运行，请耐心等待......')
        time_start = time.time()
        #以下三行为执行亚式期权计算指令
        SA = S.value
        q = 0
        Nsamples = 50000
        Tsamples = (maturity_date.value-price_date.value).days*10
        
        if option_type.value == '亚式/看涨':
            OT = '亚式/算术平均/看涨/固定'
        else:
            OT = '亚式/算术平均/看跌/固定'

        Ta,Tb,Tc,sit = MC.time_split(price_date.value,start_fixed_date.value,end_fixed_date.value,maturity_date.value)
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
                random = MC.random_gen(Nsamples,Tsamples)
                V,se = MC.Asian_Disc_MC(random,S.value,K.value,Ta,Tb,Tc,sit,r.value,sigma.value,q,SA,
                                     OT,Nsamples,Tsamples)
                time_end = time.time()
                print('第%d次计算结果：\t期权价格为: %.3f元\t用时：%.3f秒'%(count,V,time_end-time_start))
                count+=1
            else:
                print('输入有误！请确认起均日在报价日之后！')
                
        
        

    #重置按钮，返回上一步界面
    btn_init = widgets.Button(
        description=u'重置',
        disabled=False,
        button_style='success', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击返回上一单元',
        icon='check'
    )
    
    def init(p):
        display_()

    btn_preorder.on_click(on_btnPreorder_clicked)
    btn_init.on_click(init)
    
    display(container_option_info)
    select = HBox([btn_preorder,btn_init])
    display(select)

#%%
#初始界面按钮
def display_():
    btn_OptPort = widgets.Button(
        description=u'期权组合计算',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击进入期权组合计算页面',
        icon='check'
    )
        
        
    btn_asian = widgets.Button(
        description=u'亚式期权计算',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击进入亚式期权计算页面',
        icon='check'
    )
    
    btn_OptPort.on_click(on_btnOptPort_clicked)
    btn_asian.on_click(on_btnAsian_clicked)
    
    clear_output()
    tips =  widgets.HTML(value="<head><b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          版本号：1.0.0</b></head></div>")
    select = HBox([btn_OptPort,btn_asian,tips])
    display(select)

    
#%%



if __name__ == '__main__':
    #执行语句
    display_()

