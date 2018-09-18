import OptionCalc.ScenarioAnalysis.Scenario as GK
import pandas as pd
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import time
from ipywidgets import *
from IPython.display import display,clear_output,display_html


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
        value=0.03,
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
    scenario = widgets.Dropdown(
        options=['Underlying Price',
                 'Volatility',
                 'Risk Free Rate',
                 'DayPass'],
        value='Underlying Price',
        description=u'自变量：',
        disabled=False,
        continuous_update=True,
        

    )
    
    gapS = widgets.IntText(
        value=5,
        description='价格档数:',
        disabled=False,
        step=1,  #快捷变换间隔
        tooltip=u'价格档数'

    )
    rangeS = widgets.FloatText(
        value=0.01,
        description='价格间隔:',
        disabled=False,
        step=1,  #快捷变换间隔
        tooltip=u'价格间隔'

    )
    gapvol = widgets.IntText(
        value=5,
        description='波动率档数:',
        disabled=False,
        step=1,  #快捷变换间隔
        tooltip=u'波动率档数'

    )
    rangevol = widgets.FloatText(
        value=0.05,
        description='波动率间隔:',
        disabled=False,
        step=1,  #快捷变换间隔
        tooltip=u'波动率间隔'

    )
    gapT = widgets.FloatText(
        value=5,
        description='时间档数:',
        disabled=False,
        step=1,  #快捷变换间隔
        tooltip=u'时间档数'

    )
    rangeT = widgets.FloatText(
        value=1,
        description='时间间隔:',
        disabled=False,
        step=1,  #快捷变换间隔
        tooltip=u'时间间隔（天）'

    )
    tips = widgets.Label(value="选定好期权参数后，单击 【加入组合数据库】 ，随后可继续选定下一个期权的参数，以此步骤循环。")
    tips2 = widgets.Label(value="若遗忘已加入的期权信息，可单击 【查询已加期权信息】。")
    tips3 = widgets.Label(value="全部配置完成后，单击 【计算期权组合价格】。若想清空组合或返回，请单击【重置】。")
    info1 = widgets.HBox([price_date,maturity_date])
    info2 = widgets.HBox([option_type])
    info3 = widgets.HBox([S,K])
    info4 = widgets.HBox([sigma,r])
    info5 = widgets.HBox([position,direction])
    info6 = widgets.HBox([scenario])
    info7 = widgets.HBox([gapS,rangeS])
    info8 = widgets.HBox([gapvol,rangevol])
    info9 = widgets.HBox([gapT,rangeT])
    container_option_info = widgets.VBox([info1,info2,info3,info4,info5,info6,info7,info8,info9,tips,tips2,tips3])
    
    
    #计算按钮
    btn_preorder = widgets.Button(
        description=u'计算期权组合价格',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击计算已选定组合的期权价格',
        icon='check'
    )
    
    def highlight(data,mid):
        if data>mid:
            color = 'red'
        elif data<mid:
            color = 'green'
        else:
            color = 'black'
        return 'color:%s'%color
    
    def on_btnPreorder_clicked(p):
        clear_output()
        display(container_option_info)
        display(select_all)
        if len(option_portfolio)==0:
            print('无添加任何期权信息')
        else:
            greeks = pd.DataFrame()
            i = 1
            for each in option_portfolio:
                T = each[1]['maturity']
                S = each[0]['underlying price']
                K = each[1]['strike']
                sigma = each[0]['volatility']
                r = each[0]['interest']
                status = each[1]['type']
                V = GK.Greeks_Euro(S,r,sigma,K,T,status)
                tmp = V.cpt_all_greeks()
                greeks.loc[i,'Delta'] = tmp['Delta']*each[1]['position']
                greeks.loc[i,'Gamma'] = tmp['Gamma']*each[1]['position']
                greeks.loc[i,'RhoPer%'] = tmp['RhoPer%']*each[1]['position']
                greeks.loc[i,'ThetaPerday'] = tmp['ThetaPerday']*each[1]['position']
                greeks.loc[i,'VegaPer%'] = tmp['VegaPer%']*each[1]['position']
                greeks.loc[i,'Vanna'] = tmp['Vanna']*each[1]['position']
                greeks.loc[i,'VommaPer%'] = tmp['VommaPer%']*each[1]['position']
                greeks.loc[i,'CharmPerday'] = tmp['CharmPerday']*each[1]['position']
                greeks.loc[i,'VetaPerday'] = tmp['VetaPerday']*each[1]['position']
                
                i+=1
                
            greeks = greeks.append(pd.DataFrame(greeks.sum(),columns=['组合']).T)
            display(greeks)
            #print(option_portfolio)
            S_sce,r_sce,vol_sce,T_sce = GK.scenario_analysis(option_portfolio)
            #print(vol_sce)
            if scenario.value == 'Underlying Price':
                GK.plot_subplot(S_sce,scenario.value)
            elif scenario.value == 'Volatility':
                GK.plot_subplot(vol_sce,scenario.value)
            elif scenario.value == 'Risk Free Rate':
                GK.plot_subplot(r_sce,scenario.value)
            elif scenario.value == 'DayPass':
                GK.plot_subplot(T_sce,scenario.value)
            else:
                pass
            res1,res2,res3,res11,res22,res33,mid = GK.scenario_analysis2(option_portfolio,gapS.value,rangeS.value,\
                                                                         gapvol.value,rangevol.value,gapT.value,rangeT.value)
            
            res1 = res1.style.applymap(highlight,mid=mid)
            res2 = res2.style.applymap(highlight,mid=mid)
            res3 = res3.style.applymap(highlight,mid=mid)
            res11 = res11.style.applymap(highlight,mid=0)
            res22 = res22.style.applymap(highlight,mid=0)
            res33 = res33.style.applymap(highlight,mid=0)
            print('标的价格V.S.波动率 （组合价值）')
            display(res1)
            print('标的价格V.S.到期时间（年）（组合价值）')
            display(res2)
            print('波动率.S.到期时间（年）（组合价值）')
            display(res3)


            print('标的价格V.S.波动率 （组合价值变动）')
            display(res11)
            print('标的价格V.S.到期时间（年）（组合价值变动）')
            display(res22)
            print('波动率.S.到期时间（年）（组合价值变动）')
            display(res33)
                
            
            
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
        status = 'call' if option_type.value.split('/')[1]=='看涨' else 'put'
        market_property = {'underlying price':S.value,'interest':r.value,\
                           'volatility':sigma.value,'dividend':0}
        option_property = {'type':status,'position':pos,\
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

    
#初始界面按钮
def display_():
    btn_OptPort = widgets.Button(
        description=u'期权组合计算',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击进入期权组合计算页面',
        icon='check'
    )
        

    
    btn_OptPort.on_click(on_btnOptPort_clicked)
    
    clear_output()
    
    select = HBox([btn_OptPort])
    display(select)
    
if __name__ == '__main__':
    #执行语句
    display_()