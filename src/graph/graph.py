import flet as ft
import mplfinance as mpf
import requests
import pandas as pd

import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from datetime import datetime



class Print_graph(MatplotlibChart):
    def __init__(self,coin,tf):
        self.coin = coin
        self.tf = tf

    # Получите последние n свечей по n минут для торговой пары, обрабатываем и записывае данные в датафрейм
    def get_futures_klines(self):
        x = requests.get('https://fapi.binance.com/fapi/v1/klines?symbol='+self.coin.upper()+'&limit='+str(200)+'&interval='+self.tf)
        df=pd.DataFrame(x.json())
        df.columns=['open_time','open','high','low','close','volume','close_time','d1','d2','d3','d4','d5']
        df=df.drop(['d1','d2','d3','d4','d5'],axis=1)
        df['open']=df['open'].astype(float)
        df['high']=df['high'].astype(float)
        df['low']=df['low'].astype(float)
        df['close']=df['close'].astype(float)
        df['volume']=df['volume'].astype(float)
        df['open_time'] = df['open_time'].apply(lambda x: int(x/1000))
        df['open_time'] = df['open_time'].apply(lambda x: datetime.fromtimestamp(x).strftime('%H:%M'))
        return(df) # возвращаем датафрейм с подготовленными данными

    def print_graph(self):  
        print('РИСУЕМ ГРАФИК')
        df = self.get_futures_klines()
        df.index = pd.DatetimeIndex(df['open_time'])
        df = df[df.columns[[1,2,3,4,5]]]  # берем столбцы без даты открытия и закрытия
        fig, axlist = mpf.plot(df, type='candle', style='binance',returnfig=True,title='',ylabel='',ylabel_lower='',volume=True,axisoff=True,scale_padding=0.2)
        
        self.main_print = MatplotlibChart(fig)
        return self.main_print
        











