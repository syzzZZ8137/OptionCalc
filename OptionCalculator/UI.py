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
import OptionCalc.OptionCalculator.MC_Asian_Pricer as MC
import OptionCalc.OptionCalculator.Option_Portfolio as OP
import OptionCalc.OptionCalculator.Greeks as GK

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


    option_type = widgets.Dropdown(
        options=['欧式/看涨',
                 '欧式/看跌',
                 '美式/看涨',
                 '美式/看跌',
                 '标的资产'],
        value='欧式/看涨',
        description=u'期权种类:',
        disabled=False,
        continuous_update=True,
        

    )
    S = widgets.FloatText(
        value=15000,
        description='标的价格:',
        disabled=False,
        step=1,  #快捷变换间隔
        tooltip=u'待选期权种类'

    )
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
    direction = widgets.ToggleButtons(
        options=['买入', '卖出'],
        description='方向:',
        disabled=False,
        button_style='info', # 'success', 'info', 'warning', 'danger' or ''
        value = '买入'
    #     icons=['check'] * 3
    )
    position = widgets.BoundedIntText(
        value=1,
        min=0,
        max=999999999,
        description='头寸:',
        disabled=False,
        step=1
    )

    tips = widgets.Label(value="选定好期权参数后，单击 【加入组合数据库】 ，随后可继续选定下一个期权的参数，以此步骤循环。")
    tips2 = widgets.Label(value="若遗忘已加入的期权信息，可单击 【查询已加期权信息】。")
    tips3 = widgets.Label(value="全部配置完成后，单击 【计算期权组合价格】。若想清空组合或返回，请单击【重置】。")
    container_option_info = widgets.VBox([price_date,
                                          maturity_date,
                                          option_type,S,K,sigma,r,direction,position,tips,tips2,tips3])
    
    
    #计算按钮
    btn_preorder = widgets.Button(
        description=u'计算期权组合价格',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击计算已选定组合的期权价格',
        icon='check'
    )

    def on_btnPreorder_clicked(p):
        clear_output()
        display(container_option_info)
        display(select_all)
        if len(option_portfolio)==0:
            print('无添加任何期权信息')
        else:
            port_sum = OP.option_portfolio_main(option_portfolio,strategy_name = 'PnL')
            greeks = pd.DataFrame(columns=['Delta','Gamma','Rho(%)','ThetaPerday','Vega(%)'])
            i = 1
            for each in option_portfolio:
                T = each[1]['maturity']
                S = each[0]['underlying price']
                K = each[1]['strike']
                sigma = each[0]['volatility']
                r = each[0]['interest']
                status = 'call' if each[1]['type'].split('/')[1]=='看涨' else 'put'
                V = GK.Greeks_Euro(S,r,sigma,K,T,status)
                tmp = V.cpt_all_greeks()
                greeks.loc[i,'Delta'] = tmp['Delta']*each[1]['position']
                greeks.loc[i,'Gamma'] = tmp['Gamma']*each[1]['position']
                greeks.loc[i,'Rho(%)'] = tmp['Rho(%)']*each[1]['position']
                greeks.loc[i,'ThetaPerday'] = tmp['ThetaPerday']*each[1]['position']
                greeks.loc[i,'Vega(%)'] = tmp['Vega(%)']*each[1]['position']
                i+=1
            greeks = greeks.append(pd.DataFrame(greeks.sum(),columns=['组合']).T)
            display(greeks)
    
    #增加期权品种按钮
    #将新增加的期权信息，添加至option_portfolio变量中
    btn_entry_db = widgets.Button(
        description=u'加入组合数据库',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击将已配置好的期权参数加入组合',
        icon='check'
    )
    def entry_db(p):
        #global container_option_info   #加全局变量
        clear_output()
        display(container_option_info)
        display(select_all)
        
        if direction.value == '卖出':
            pos = -position.value
        else:
            pos = position.value

        market_property = {'underlying price':S.value,'interest':r.value,\
                           'volatility':sigma.value,'dividend':0}
        option_property = {'type':option_type.value,'position':pos,\
                           'strike':K.value,'maturity':(maturity_date.value - price_date.value).days/365}
        print('已进入期权组合！')
        option_portfolio.append([market_property,option_property])
    
    #查询已添加的期权数据
    btn_query_db = widgets.Button(
        description=u'查询已加期权信息',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击查询已加入组合的期权信息',
        icon='check'
    )
    
    def query_db(p):
        clear_output()
        display(container_option_info)
        display(select_all)
        if len(option_portfolio)==0:
            print('无添加任何期权信息')
        else:
            i=1
            option_info = []
            for each in option_portfolio:
                option_info.append([i,each[1]['type'],each[0]['underlying price'],\
                                   each[1]['strike'],each[1]['position'],\
                                   each[1]['maturity'],\
                                   each[0]['interest'],each[0]['volatility']])
                i+=1
                
            option_info = pd.DataFrame(option_info,columns=['期权序号','期权类型','标的价格',\
                                                            '期权行权价','期权头寸','期权到期时间（年）',\
                                                            '无风险利率','波动率'])  #组合成pandas
            option_info.set_index('期权序号',inplace=True,drop=True)    
            display(option_info)
    
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
    
    global option_portfolio
    option_portfolio = []
    btn_preorder.on_click(on_btnPreorder_clicked)
    btn_entry_db.on_click(entry_db)
    btn_query_db.on_click(query_db)
    btn_init.on_click(init)
    
    display(container_option_info)
    
    select = HBox([btn_entry_db,btn_query_db])
    select2 = HBox([btn_preorder,btn_init])
    select_all = VBox([select,select2])
    display(select_all)


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
    position = widgets.BoundedIntText(
        value=1,
        min=0,
        max=999999999,
        description='头寸:',
        disabled=False,
        step=1
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

    date_info = widgets.HBox([price_date,maturity_date])
    date_info2 = widgets.HBox([start_fixed_date,end_fixed_date])
    info1 = widgets.HBox([S,K])
    info2 = widgets.HBox([r,sigma])
    info3 = widgets.HBox([position])
    
    container_option_info = widgets.VBox([date_info,date_info2,tips1,
                                          option_type,tips2,info1,info2,info3])
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
                #random,S,SA,r,sigma,K,price_date,maturity_date,start_fixed_date,end_fixed_date,status
                status = 'call' if OT.split('/')[2]=='看涨' else 'put'
                VV = GK.Aisan_Greeks(random,S.value,S.value,r.value,sigma.value,K.value,price_date.value,maturity_date.value,\
                                    start_fixed_date.value,end_fixed_date.value,status)
                res = VV.cpt_all_greeks()
                time_end = time.time()
                print('第%d次计算结果：\t期权单价为: %.3f元\t总权利金为%.3f元\t用时：%.3f秒'%(count,V,V*position.value,time_end-time_start))
                res = pd.DataFrame(res,index=[count])
                res = res*position.value
                display(res)
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
    
    select = HBox([btn_OptPort,btn_asian])
    display(select)

    




if __name__ == '__main__':
    #执行语句
    display_()
