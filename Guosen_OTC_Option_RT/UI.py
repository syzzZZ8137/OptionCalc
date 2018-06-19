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
import OptionCalc.Guosen_OTC_Option.Tprice as TP
import OptionCalc.Guosen_OTC_Option.Tprice_RealTime as TP_RT
import OptionCalc.Guosen_OTC_Option.GetDataMySQL as GetDataMySQL
import OptionCalc.Guosen_OTC_Option.GetUnderling as GetUnderling
import OptionCalc.Guosen_OTC_Option.GetContract as GetContract

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
        value=1,
        disabled=False,
        step=0.01,
        layout=Layout(width='207.5px')
    )
    Labelr = widgets.Label(value='无风险利率(%):')
    Boxr = widgets.HBox([Labelr,r])
    

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
        value=30,
        description='波动率(%):',
        disabled=False,
        step=0.01,
        min = 0.01
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
        value=30,
        description='波动率(%):',
        disabled=False,
        step=0.01,
        min = 0.01
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
        value=30,
        description='波动率(%):',
        disabled=False,
        step=0.01,
        min = 0.01
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
                          版本号：1.1.0</b></head></div>")
    tips3 = widgets.Label(value=" ") #产生一个空行
    #排版
    public_info_sub1 = widgets.HBox([price_date,maturity_date,tips2])
    public_info_sub2 = widgets.HBox([S,Boxr,tips3])
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
            market_property = {'underlying price':S.value,'interest':r.value/100,\
                               'volatility':private_info.children[2].value/100,'dividend':0}
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
        global option_portfolio,container_option_info
        
        clear_output()
        display(container_option_info)
        display(select)

        entry_combos(private_info1)
        entry_combos(private_info2)
        entry_combos(private_info3)
        
        if len(option_portfolio)==0:
            print('无添加任何期权信息')
        else:
            if option_portfolio[0][1]['maturity']<=0:
                print('输入有误！请确认到期日在报价日之后！')
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

    select = widgets.HBox([btn_preorder,btn_init])
    display(select)

#%%
#亚式期权界面
def on_btnAsian_clicked(p):
    clear_output()

    now = datetime.now()
    f = now + timedelta(days=90)  #90天后日期

    price_date = widgets.DatePicker(
        description='期权报价日:',
        disabled=False,
        value=now.date()
    )

    start_fixed_date = widgets.DatePicker(
        description='期权起均日:',
        disabled=False,
        value=now.date()
    )
    end_fixed_date = widgets.DatePicker(
        description='期权终均日:',
        disabled=False,
        value=f.date()
    )
    maturity_date = widgets.DatePicker(
        description='期权到期日:',
        disabled=False,
        value=f.date()
    )

    tips1 = widgets.Label(value="【期权起均日】 至 【期权终均日】，意为亚式期权平均值累计(采价)区间。")
    
    option_type = widgets.Dropdown(
        options=['亚式/看涨',
                 '亚式/看跌'],
        value='亚式/看跌',
        description=u'期权种类:',
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
        value=30,
        description='波动率(%):',
        disabled=False,
        step=0.01,
        min = 0.01
    )
    r = widgets.FloatText(
        value=1,
        disabled=False,
        step=0.01,
        layout=Layout(width='207.5px')
    )
    Labelr = widgets.Label(value='无风险利率(%):')
    Boxr = widgets.HBox([Labelr,r])
    
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
                          版本号：1.1.0</b></head></div>")
    date_info = widgets.HBox([price_date,maturity_date,tips3])
    date_info2 = widgets.HBox([start_fixed_date,end_fixed_date])
    info1 = widgets.HBox([S,K])
    info2 = widgets.HBox([Boxr,sigma])
    
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
                V,se = MC.Asian_Disc_MC(random,S.value,K.value,Ta,Tb,Tc,sit,r.value/100,sigma.value/100,q,SA,
                                     OT,Nsamples,Tsamples)
                time_end = time.time()
                in_put = [S.value,K.value,price_date.value,maturity_date.value,\
                          start_fixed_date.value,end_fixed_date.value,\
                          '%.2f%%'%r.value,'%.2f%%'%sigma.value]
                in_put = pd.DataFrame(in_put,index=['标的价格','行权价','期权报价日','期权到期日',\
                                                    '期权起均日','期权终均日','无风险利率','波动率'],columns=[count]).T
                
                display(in_put)
                
                print('第%d次计算结果：\t期权价格为: %.3f元\t期权费率为：%.2f%% \t 用时：%.3f秒'%(count,V,V/S.value*100,time_end-time_start))
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
    select = widgets.HBox([btn_preorder,btn_init])
    display(select)
#%%T字型报价
def on_btnTprice_clicked(p):
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
        value=1,
        disabled=False,
        step=0.01,
        layout=Layout(width='207.5px')
    )
    Labelr = widgets.Label(value='无风险利率(%):')
    Boxr = widgets.HBox([Labelr,r])
    
    
    sigma_buy = widgets.BoundedFloatText(
        value=20,
        disabled=False,
        step=0.01,
        min = 0.01,
        layout=Layout(width='207.5px')
    )
    LabelsigB = widgets.Label(value='买价波动率(%):')
    BoxsigB = widgets.HBox([LabelsigB,sigma_buy])
    
    sigma_sell = widgets.BoundedFloatText(
        value=30,
        disabled=False,
        step=0.01,
        min = 0.01,
        layout=Layout(width='207.5px')
    )
    LabelsigS = widgets.Label(value='卖价波动率(%):')
    BoxsigS = widgets.HBox([LabelsigS,sigma_sell])
    
    step = widgets.BoundedIntText(
        value=5,
        description='实虚档数:',
        disabled=False,
        step=1,
        min = 1,
        tooltip=u'待选期权种类'
    )
    increment = widgets.BoundedFloatText(
        value=1,
        description='每档步长(%):',
        disabled=False,
        step=1,
        tooltip=u'待选期权种类',
        min=0.01
    )
    
    tips3 =  widgets.HTML(value="<head><b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                              &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                              &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                              &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                              版本号：1.1.0</b></head></div>")
    
    info1 = widgets.HBox([S,tips3])
    info2 = widgets.HBox([price_date,maturity_date])
    info3 = widgets.HBox([BoxsigB,BoxsigS])
    info4 = widgets.HBox([Boxr])
    info5 = widgets.HBox([step,increment])
    tips1 = widgets.Label(value="【实虚档数】 为希望计算T字型报价的最高档数。 【每档步长】 为每档之间的间隔(按百分比计算)。")
    tips2 = widgets.Label(value="【买价波动率】和【卖价波动率】针对双向报价，【买价波动率】小于【卖价波动率】。")
    global container_option_info
    
    container_option_info = widgets.VBox([info1,info2,info3,info4,info5,tips1,tips2])
    
    #计算按钮
    btn_preorder = widgets.Button(
        description=u'计算期权价格',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击计算已选定组合的期权价格',
        icon='check'
    )
    def highlight(data,steps):
        #改变T字型颜色
        Put_OM = 'color:{}'.format('green')
        Put_IM = 'color:{}'.format('red')
        Call_OM = 'color:{}'.format('green')
        Call_IM = 'color:{}'.format('red')
        Strike = 'background-color:{}'.format('yellow')

        row1 = [[Put_IM,Put_IM,Put_IM,Put_IM,Strike,Call_OM,Call_OM,Call_OM,Call_OM]]
        row2 = [['','','','',Strike,'','','','']]
        row3 = [[Put_OM,Put_OM,Put_OM,Put_OM,Strike,Call_IM,Call_IM,Call_IM,Call_IM]]
        style_df = row1*steps +row2+row3*steps
        return pd.DataFrame(style_df,index=data.index,columns=data.columns)
    
    def on_btnPreorder_clicked(p):
        
        global container_option_info
        clear_output()
        display(container_option_info)
        select = widgets.HBox([btn_preorder,btn_init])
        display(select)
        
        ttmday = (maturity_date.value-price_date.value).days+1
        ttm = (ttmday)/365
        temp_input = [S.value,ttm,r.value/100,0,sigma_buy.value/100,sigma_sell.value/100] #temp_input = [S,T,r,q,buy_sigma,sell_sigma]
        temp_output = TP.Tprice(S.value,step.value,increment.value/100,temp_input)
        temp_output.index = temp_output.index-step.value
        
        temp_output_pct = temp_output.copy()
        temp_output_pct2 = temp_output.copy()
        temp_output_pct['看跌买价'] = temp_output_pct['看跌买价'].apply(lambda x : '%.2f%%'%(x/S.value*100))
        temp_output_pct2.insert(1,'看跌买价%',temp_output_pct['看跌买价'])
        temp_output_pct['看跌卖价'] = temp_output_pct['看跌卖价'].apply(lambda x : '%.2f%%'%(x/S.value*100))
        temp_output_pct2.insert(3,'看跌卖价%',temp_output_pct['看跌卖价'])
        temp_output_pct['看涨买价'] = temp_output_pct['看涨买价'].apply(lambda x : '%.2f%%'%(x/S.value*100))
        temp_output_pct2.insert(6,'看涨买价%',temp_output_pct['看涨买价'])
        temp_output_pct['看涨卖价'] = temp_output_pct['看涨卖价'].apply(lambda x : '%.2f%%'%(x/S.value*100))
        temp_output_pct2.insert(8,'看涨卖价%',temp_output_pct['看涨卖价'])

        
        
        #out = widgets.Output(layout={'border': '2px solid black'})
        out = widgets.Output()
        with out:
            tips =  widgets.HTML(value="<head><b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                              &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                              距离到期日还剩：%d天</b></head></div>"%ttmday)
            
            
            display(tips)
            temp_output_pct2 = temp_output_pct2.style.apply(highlight,steps=step.value,axis=None)
            display(temp_output_pct2)
        display(out)
    
    btn_preorder.on_click(on_btnPreorder_clicked)
    
    
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
    select = widgets.HBox([btn_preorder,btn_init])
    display(select)
    
#%%
#实时波动率报价界面
def on_btnRealTimeprice_clicked(p):
    clear_output()
    
    global exchange_lst,relation_lst,EN_EX,EN_cont
    exchange_lst,relation_lst = GetUnderling.Getunderling()
    exchange = exchange_lst['ZHname'].tolist()
    exchange.insert(0,'无')
    EN_EX = '无'
    EN_cont = '无'
    
    #关联3个选项框的函数
    
    def on_select(change):
        global CN_cont_lst,EN_cont_lst,CN_EX,EN_EX
        V2.options = ['无']
        EN_EX = '无'
        for i in range(len(exchange_lst)):
            if change['new'] == exchange_lst.loc[i,'ZHname']:
                CN_cont_lst = relation_lst[i]['ZHname']
                EN_cont_lst = relation_lst[i]['contract']
                CN_EX = exchange_lst.loc[i,'ZHname']
                EN_EX = exchange_lst.loc[i,'exchange']

                tmp = ['无']
                tmp.extend(CN_cont_lst)
                V2.options = tmp

    def on_select2(change):
        global EN_cont,CN_cont,cont_date_lst
        V3.options = ['无']
        EN_cont = '无'
        for i in range(len(EN_cont_lst)):
            if change['new'] == CN_cont_lst[i]:
                cont_date_lst = GetContract.GetContract(EN_EX,EN_cont_lst[i])
                tmp = ['无']
                tmp.extend(cont_date_lst)
                V3.options = tmp

                EN_cont = EN_cont_lst[i]
                CN_cont = CN_cont_lst[i]
                #print(EN_cont_lst,CN_EX,EN_EX,CN_cont,EN_cont,cont_date_lst)

    def on_select3(change):
        global cont_date
        cont_date = change['new']
        #print(cont_date)

    V1 = widgets.Dropdown(options=exchange,description=u'交易所:',disabled=False,continuous_update=True)
    V2 = widgets.Dropdown(options=['无'],description=u'品种:',disabled=False,continuous_update=True)
    V3 = widgets.Dropdown(options=['无'],description=u'合约:',disabled=False,continuous_update=True)

    V1.observe(on_select,'value')
    V2.observe(on_select2,'value')
    V3.observe(on_select3,'value')
    
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
        value=1,
        disabled=False,
        step=0.01,
        layout=Layout(width='207.5px')
    )
    Labelr = widgets.Label(value='无风险利率(%):')
    Boxr = widgets.HBox([Labelr,r])
    
    step = widgets.BoundedIntText(
        value=5,
        description='实虚档数:',
        disabled=False,
        step=1,
        min = 1,
        tooltip=u'待选期权种类'
    )
    
    increment = widgets.BoundedFloatText(
        value=1,
        description='每档步长(%):',
        disabled=False,
        step=1,
        tooltip=u'待选期权种类',
        min=0.01
    )
    
    LabelP = widgets.Label(value='报价方式:',layout=Layout(width='120px',left='130px'))
    is_price_percent = widgets.Checkbox(value=True,description='费率',disabled=False,layout=Layout(width='100%',align_self='center'))
    is_vol = widgets.Checkbox(value=True,description='波动率',disabled=False,layout=Layout(width='100%',align_self='center'))

    
    
    tips3 =  widgets.HTML(value="<head><b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                              &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                              &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                              &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                              版本号：1.1.0</b></head></div>")
    
    info0 = widgets.HBox([V1,tips3])
    info00 = widgets.HBox([V2,V3])
    info1 = widgets.HBox([S])
    info2 = widgets.HBox([price_date,maturity_date])
    info3 = widgets.HBox([Boxr])
    info4 = widgets.HBox([step,increment])
    info5 = widgets.HBox([LabelP,is_price_percent,is_vol],layout=Layout(display='flex',flex_flow='row',width='50%'))
    info55 = widgets.VBox([is_price_percent,is_vol],layout=Layout(align_items='stretch'))
    info5 = widgets.HBox([LabelP,info55],layout=Layout(width='30%',align_self='stretch'))
    
    #info6 = widgets.HBox([info5])
    tips1 = widgets.Label(value="【实虚档数】 为希望计算T字型报价的最高档数。 【每档步长】 为每档之间的间隔(按百分比计算)。")
    tips2 = widgets.Label(value="选择以何种形式报价：【价格】、【费率】、【波动率】")
    
    global container_option_info
    
    container_option_info = widgets.VBox([info0,info00,info1,info2,info3,info4,tips1,info5,tips2])
    
    #计算按钮
    btn_preorder = widgets.Button(
        description=u'计算期权价格',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击计算已选定组合的期权价格',
        icon='check'
    )
    
    def highlight(data,steps):
        #改变T字型颜色
        Put_OM = 'color:{}'.format('green')
        Put_IM = 'color:{}'.format('red')
        Call_OM = 'color:{}'.format('green')
        Call_IM = 'color:{}'.format('red')
        Strike = 'background-color:{}'.format('yellow')
        
        row1 = [[Put_IM,Put_IM,Put_IM,Put_IM,Strike,Call_OM,Call_OM,Call_OM,Call_OM]]
        row2 = [['','','','',Strike,'','','','']]
        row3 = [[Put_OM,Put_OM,Put_OM,Put_OM,Strike,Call_IM,Call_IM,Call_IM,Call_IM]]
        
        style_df = row1*steps +row2+row3*steps
        return pd.DataFrame(style_df,index=data.index,columns=data.columns)
    
    def on_btnPreorder_clicked(p):
        
        global container_option_info
        clear_output()
        display(container_option_info)
        select = widgets.HBox([btn_preorder,btn_init])
        display(select)
        
        if EN_EX == '无':
            print('请选择交易所')
        elif EN_cont == '无':
            print('请选择标的资产')
        else:

            myfuture = EN_EX+'-'+EN_cont
            print(myfuture)
            ttmday = (maturity_date.value-price_date.value).days+1
            ttm = (ttmday)/365
            temp_input = [S.value,ttm,r.value/100,0,myfuture] #S,T,r,q,contract

            temp_output,temp_output_vol = TP_RT.Tprice_realtime(S.value,step.value,increment.value/100,temp_input)
            temp_output.index = temp_output.index-step.value
            temp_output_vol.index = temp_output_vol.index - step.value
            
            if is_price_percent.value:
                temp_output_pct = temp_output.copy()
                temp_output_pct2 = temp_output.copy()
                temp_output_pct['看跌买价'] = temp_output_pct['看跌买价'].apply(lambda x : '%.2f%%'%(x/S.value*100))
                temp_output_pct2.insert(1,'看跌买价%',temp_output_pct['看跌买价'])
                temp_output_pct['看跌卖价'] = temp_output_pct['看跌卖价'].apply(lambda x : '%.2f%%'%(x/S.value*100))
                temp_output_pct2.insert(3,'看跌卖价%',temp_output_pct['看跌卖价'])
                temp_output_pct['看涨买价'] = temp_output_pct['看涨买价'].apply(lambda x : '%.2f%%'%(x/S.value*100))
                temp_output_pct2.insert(6,'看涨买价%',temp_output_pct['看涨买价'])
                temp_output_pct['看涨卖价'] = temp_output_pct['看涨卖价'].apply(lambda x : '%.2f%%'%(x/S.value*100))
                temp_output_pct2.insert(8,'看涨卖价%',temp_output_pct['看涨卖价'])

            if is_vol.value:
                temp_output_vol2 = temp_output.copy()
                temp_output_vol['看跌买方波动率'] = temp_output_vol['看跌买方波动率'].apply(lambda x : '%.2f%%'%(x*100))
                temp_output_vol2.insert(1,'看跌买波动率',temp_output_vol['看跌买方波动率'])
                temp_output_vol['看跌卖方波动率'] = temp_output_vol['看跌卖方波动率'].apply(lambda x : '%.2f%%'%(x*100))
                temp_output_vol2.insert(3,'看跌卖波动率',temp_output_vol['看跌卖方波动率'])
                temp_output_vol['看涨买方波动率'] = temp_output_vol['看涨买方波动率'].apply(lambda x : '%.2f%%'%(x*100))
                temp_output_vol2.insert(6,'看涨买波动率',temp_output_vol['看涨买方波动率'])
                temp_output_vol['看涨卖方波动率'] = temp_output_vol['看涨卖方波动率'].apply(lambda x : '%.2f%%'%(x*100))
                temp_output_vol2.insert(8,'看涨卖波动率',temp_output_vol['看涨卖方波动率'])
                
            out = widgets.Output()
            with out:
                tips =  widgets.HTML(value="<head><b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                                  &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                                  距离到期日还剩：%d天</b></head></div>"%ttmday)

                display(tips)
                
                if is_price_percent.value:
                    temp_output_pct2 = temp_output_pct2.style.apply(highlight,steps=step.value,axis=None)
                    display(temp_output_pct2)
                if is_vol.value:
                    temp_output_vol2 = temp_output_vol2.style.apply(highlight,steps=step.value,axis=None)
                    display(temp_output_vol2)
            display(out)
    
    btn_preorder.on_click(on_btnPreorder_clicked)
            
    
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
    
    btn_init.on_click(init)
    
    display(container_option_info)
    
    select = widgets.HBox([btn_preorder,btn_init])
    display(select)

    
def on_btn_RT_OptPort_clicked(p):
    clear_output()
    
    global exchange_lst,relation_lst,EN_EX,EN_cont
    exchange_lst,relation_lst = GetUnderling.Getunderling()
    exchange = exchange_lst['ZHname'].tolist()
    exchange.insert(0,'无')
    EN_EX = '无'
    EN_cont = '无'
    
    #关联3个选项框的函数
    
    def on_select(change):
        global CN_cont_lst,EN_cont_lst,CN_EX,EN_EX
        V2.options = ['无']
        EN_EX = '无'
        for i in range(len(exchange_lst)):
            if change['new'] == exchange_lst.loc[i,'ZHname']:
                CN_cont_lst = relation_lst[i]['ZHname']
                EN_cont_lst = relation_lst[i]['contract']
                CN_EX = exchange_lst.loc[i,'ZHname']
                EN_EX = exchange_lst.loc[i,'exchange']

                tmp = ['无']
                tmp.extend(CN_cont_lst)
                V2.options = tmp

    def on_select2(change):
        global EN_cont,CN_cont,cont_date_lst
        V3.options = ['无']
        EN_cont = '无'
        for i in range(len(EN_cont_lst)):
            if change['new'] == CN_cont_lst[i]:
                cont_date_lst = GetContract.GetContract(EN_EX,EN_cont_lst[i])
                tmp = ['无']
                tmp.extend(cont_date_lst)
                V3.options = tmp

                EN_cont = EN_cont_lst[i]
                CN_cont = CN_cont_lst[i]
                #print(EN_cont_lst,CN_EX,EN_EX,CN_cont,EN_cont,cont_date_lst)

    def on_select3(change):
        global cont_date
        cont_date = change['new']
        #print(cont_date)

    V1 = widgets.Dropdown(options=exchange,description=u'交易所:',disabled=False,continuous_update=True)
    V2 = widgets.Dropdown(options=['无'],description=u'品种:',disabled=False,continuous_update=True)
    V3 = widgets.Dropdown(options=['无'],description=u'合约:',disabled=False,continuous_update=True)

    V1.observe(on_select,'value')
    V2.observe(on_select2,'value')
    V3.observe(on_select3,'value')
    
    
    
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
        value=1,
        disabled=False,
        step=0.01,
        layout=Layout(width='207.5px')
    )
    Labelr = widgets.Label(value='无风险利率(%):')
    Boxr = widgets.HBox([Labelr,r])
    

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
                          版本号：1.1.0</b></head></div>")
    tips3 = widgets.Label(value=" ") #产生一个空行
    
    
    #排版
    V = widgets.HBox([V1,tips2])
    VV = widgets.HBox([V2,V3])
    public_info_sub1 = widgets.HBox([price_date,maturity_date])
    public_info_sub2 = widgets.HBox([S,Boxr,tips3])
    public_info = widgets.VBox([public_info_sub1,public_info_sub2,tips1])
    
    private_info1 = widgets.VBox([option_type1,K1,direction1,position1])
    private_info2 = widgets.VBox([option_type2,K2,direction2,position2])
    private_info3 = widgets.VBox([option_type3,K3,direction3,position3])
    
    private_info = widgets.HBox([private_info1,private_info2,private_info3])
    global option_portfolio,container_option_info
    
    
    container_option_info = widgets.VBox([V,VV,public_info,private_info,tips])
    
    option_portfolio = []
    
    #判断期权类型是否为“无”，若是，则加入。
    def entry_combos(private_info):
        if private_info.children[0].value=='无':
            pass
        else:
            myfuture = EN_EX+'-'+EN_cont
            volbuy,volsell = TP_RT.cal_buy_sell_vol(myfuture,S.value,(maturity_date.value - price_date.value).days+1,[private_info.children[1].value])
            
            if private_info.children[2].value == '卖出':
                pos = -private_info.children[3].value
                vol = volbuy['vol'].values[0]
            else:
                pos = private_info.children[3].value
                vol = volsell['vol'].values[0]
                
            #加入组合库
            
            market_property = {'underlying price':S.value,'interest':r.value/100,\
                               'volatility':vol,'dividend':0}
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
        global option_portfolio,container_option_info
        
        clear_output()
        display(container_option_info)
        display(select)
        
        if EN_EX == '无':
            print('请选择交易所')
        elif EN_cont == '无':
            print('请选择标的资产')
        else:
            
            
            entry_combos(private_info1)
            entry_combos(private_info2)
            entry_combos(private_info3)

            if len(option_portfolio)==0:
                print('无添加任何期权信息')
            else:
                if option_portfolio[0][1]['maturity']<=0:
                    print('输入有误！请确认到期日在报价日之后！')
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

    select = widgets.HBox([btn_preorder,btn_init])
    display(select)


def on_btn_RT_aisan_clicked(p):
    clear_output()

    global exchange_lst,relation_lst,EN_EX,EN_cont
    exchange_lst,relation_lst = GetUnderling.Getunderling()
    exchange = exchange_lst['ZHname'].tolist()
    exchange.insert(0,'无')
    EN_EX = '无'
    EN_cont = '无'
    
    #关联3个选项框的函数
    
    def on_select(change):
        global CN_cont_lst,EN_cont_lst,CN_EX,EN_EX
        V2.options = ['无']
        EN_EX = '无'
        for i in range(len(exchange_lst)):
            if change['new'] == exchange_lst.loc[i,'ZHname']:
                CN_cont_lst = relation_lst[i]['ZHname']
                EN_cont_lst = relation_lst[i]['contract']
                CN_EX = exchange_lst.loc[i,'ZHname']
                EN_EX = exchange_lst.loc[i,'exchange']

                tmp = ['无']
                tmp.extend(CN_cont_lst)
                V2.options = tmp

    def on_select2(change):
        global EN_cont,CN_cont,cont_date_lst
        V3.options = ['无']
        EN_cont = '无'
        for i in range(len(EN_cont_lst)):
            if change['new'] == CN_cont_lst[i]:
                cont_date_lst = GetContract.GetContract(EN_EX,EN_cont_lst[i])
                tmp = ['无']
                tmp.extend(cont_date_lst)
                V3.options = tmp

                EN_cont = EN_cont_lst[i]
                CN_cont = CN_cont_lst[i]
                #print(EN_cont_lst,CN_EX,EN_EX,CN_cont,EN_cont,cont_date_lst)

    def on_select3(change):
        global cont_date
        cont_date = change['new']
        #print(cont_date)

    V1 = widgets.Dropdown(options=exchange,description=u'交易所:',disabled=False,continuous_update=True)
    V2 = widgets.Dropdown(options=['无'],description=u'品种:',disabled=False,continuous_update=True)
    V3 = widgets.Dropdown(options=['无'],description=u'合约:',disabled=False,continuous_update=True)

    V1.observe(on_select,'value')
    V2.observe(on_select2,'value')
    V3.observe(on_select3,'value')
    
    
    now = datetime.now()
    f = now + timedelta(days=90)  #90天后日期

    price_date = widgets.DatePicker(
        description='期权报价日:',
        disabled=False,
        value=now.date()
    )

    start_fixed_date = widgets.DatePicker(
        description='期权起均日:',
        disabled=False,
        value=now.date()
    )
    end_fixed_date = widgets.DatePicker(
        description='期权终均日:',
        disabled=False,
        value=f.date()
    )
    maturity_date = widgets.DatePicker(
        description='期权到期日:',
        disabled=False,
        value=f.date()
    )

    tips1 = widgets.Label(value="【期权起均日】 至 【期权终均日】，意为亚式期权平均值累计(采价)区间。")
    
    option_type = widgets.Dropdown(
        options=['亚式/看涨',
                 '亚式/看跌'],
        value='亚式/看跌',
        description=u'期权种类:',
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
    
    r = widgets.FloatText(
        value=1,
        disabled=False,
        step=0.01,
        layout=Layout(width='207.5px')
    )
    Labelr = widgets.Label(value='无风险利率(%):')
    Boxr = widgets.HBox([Labelr,r])
    
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
                          版本号：1.1.0</b></head></div>")
    V = widgets.HBox([V1,tips3])
    VV = widgets.HBox([V2,V3])
    date_info = widgets.HBox([price_date,maturity_date])
    date_info2 = widgets.HBox([start_fixed_date,end_fixed_date])
    info1 = widgets.HBox([S,K])
    info2 = widgets.HBox([Boxr])
    
    container_option_info = widgets.VBox([V,VV,date_info,date_info2,tips1,
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
        
        if EN_EX == '无':
            print('请选择交易所')
        elif EN_cont == '无':
            print('请选择标的资产')
        else:
        
            global container_option_info   #加全局变量
            global count
            #global count
            #抓取波动率
            myfuture = EN_EX+'-'+EN_cont
            volbuy,volsell = TP_RT.cal_buy_sell_vol(myfuture,S.value,(maturity_date.value - price_date.value).days+1,[K.value])
            volbuy = volbuy['vol'].values[0]
            volsell = volsell['vol'].values[0]
            
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
                    Vbuy,se1 = MC.Asian_Disc_MC(random,S.value,K.value,Ta,Tb,Tc,sit,r.value/100,volbuy,q,SA,
                                         OT,Nsamples,Tsamples)
                    Vsell,se2 = MC.Asian_Disc_MC(random,S.value,K.value,Ta,Tb,Tc,sit,r.value/100,volsell,q,SA,
                                         OT,Nsamples,Tsamples)
                    time_end = time.time()
                    in_put = [Vbuy,Vsell,S.value,K.value,option_type.value,price_date.value,maturity_date.value,\
                              start_fixed_date.value,end_fixed_date.value,\
                              '%.2f%%'%r.value,'%.2f%%'%(volbuy*100),'%.2f%%'%(volsell*100)]
                    in_put = pd.DataFrame(in_put,index=['期权买价','期权卖价','标的价格','行权价','期权类型','期权报价日','期权到期日',\
                                                        '期权起均日','期权终均日','无风险利率','买方波动率','卖方波动率'],columns=[count]).T

                    display(in_put)

                    print('第%d次计算结果：\t期权价格为: %.3f/%.3f元\t期权费率为：%.2f%%/%.2f%% \t 用时：%.3f秒'%(count,Vbuy,Vsell,Vbuy/S.value*100,Vsell/S.value*100,time_end-time_start))
                    
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
    select = widgets.HBox([btn_preorder,btn_init])
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
    
    btn_Tprice = widgets.Button(
        description=u'T字型报价',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击进入T字型报价页面',
        icon='check'
    )
    
    btn_RT_OptPort = widgets.Button(
        description=u'期权组合报价（实时波动率）',
        disabled=False,
        button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击进入期权组合报价（实时波动率）页面',
        icon='check',
        layout=Layout(width='250px')
    )
    
    btn_RT_aisan = widgets.Button(
        description=u'亚式期权报价（实时波动率）',
        disabled=False,
        button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击进入亚式期权报价（实时波动率）页面',
        icon='check',
        layout=Layout(width='250px')
    )
    
    btn_RealTimeprice = widgets.Button(
        description=u'T字型报价（实时波动率）',
        disabled=False,
        button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击进入T字型报价（实时波动率）页面',
        icon='check',
        layout=Layout(width='250px')
    )
    
    btn_OptPort.on_click(on_btnOptPort_clicked)
    btn_asian.on_click(on_btnAsian_clicked)
    btn_Tprice.on_click(on_btnTprice_clicked)
    btn_RT_OptPort.on_click(on_btn_RT_OptPort_clicked)
    btn_RT_aisan.on_click(on_btn_RT_aisan_clicked)
    btn_RealTimeprice.on_click(on_btnRealTimeprice_clicked)
    
    
    clear_output()
    tips =  widgets.HTML(value="<head><b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          版本号：1.1.0</b></head></div>")
    select1 = HBox([btn_OptPort,tips])
    select11 = VBox([btn_asian,btn_Tprice])
    select2 = VBox([btn_RT_OptPort,btn_RT_aisan,btn_RealTimeprice])
    select = VBox([select1,select11,select2])
    display(select)

    
#%%

if __name__ == '__main__':
    #执行语句
    display_()

