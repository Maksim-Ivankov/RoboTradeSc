import flet as ft
import mplfinance as mpf
import requests
import pandas as pd

import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from datetime import datetime



class Main:
    def __init__(self):
        self.page: ft.Page = None

    # Получите последние n свечей по n минут для торговой пары, обрабатываем и записывае данные в датафрейм
    def get_futures_klines(self,symbol,TF,VOLUME):
        x = requests.get('https://fapi.binance.com/fapi/v1/klines?symbol='+symbol.upper()+'&limit='+str(VOLUME)+'&interval='+TF)
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

    def run(self, page):
        print('РИСУЕМ MAIN')
        self.page: ft.Page = page
        self.settings = ['BTCUSDT']
        self.page.title = "MIN"
        self.page.window_height, self.page.window_width = 1000, 1200
        self.page.theme_mode = "light" 

        df = self.get_futures_klines('BTCUSDT','5m',100)
        df.index = pd.DatetimeIndex(df['open_time'])
        df = df[df.columns[[1,2,3,4,5]]]  # берем столбцы без даты открытия и закрытия
        print(df)
        fig, axlist = mpf.plot(df, type='candle', style='binance',returnfig=True,title='',ylabel='',ylabel_lower='',volume=True)
        self.main_print = MatplotlibChart(fig)
        self.page.add(self.main_print)
        





ft.app(target=Main().run)









