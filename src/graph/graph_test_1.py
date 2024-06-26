import flet as ft

import asyncio
# from src.graph.graph import Print_graph
import multiprocessing as mp
import time
import mplfinance as mpf
import requests
import pandas as pd
import datetime
from datetime import datetime
import numpy as np

# class Main:
#     def __init__(self):
#         self.page: ft.Page = None

#     def run(self, page):
#         print('РИСУЕМ MAIN')
#         self.page: ft.Page = page
#         self.settings = ['BTCUSDT']


        
        
#         self.page.title = "MIN"
#         self.page.window_height, self.page.window_width = 1000, 1200
#         self.page.theme_mode = "light" 
#         self.main_print = ft.Container( # общий контейнер на страницу
            
#         )

# Получите последние n свечей по n минут для торговой пары, обрабатываем и записывае данные в датафрейм
def get_futures_klines(symbol,TF,VOLUME):
    x = requests.get('https://fapi.binance.com/fapi/v1/klines?symbol='+symbol.upper()+'&limit='+str(VOLUME)+'&interval='+TF)
    df=pd.DataFrame(x.json())
    df.columns=['open_time','open','high','low','close','volume','close_time','d1','d2','d3','d4','d5']
    df=df.drop(['d1','d2','d3','d4','d5'],axis=1)
    df['open']=df['open'].astype(float)
    df['high']=df['high'].astype(float)
    df['low']=df['low'].astype(float)
    df['close']=df['close'].astype(float)
    df['volume']=df['volume'].astype(float)
    return(df) # возвращаем датафрейм с подготовленными данными

format = '%Y-%m-%d %H:%M:%S'

df = get_futures_klines('BTCUSDT','5m',100)
# df.rename(columns={'open_time':'Datetime'},inplace=True)
# df['Datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
# df['Datetime'] = pd.to_datetime(df['open_time'], format=format)
# df = df.set_index(pd.DatetimeIndex(df['Datetime']))
# df['Datetime'] = pd.to_datetime(datetime.fromtimestamp(int(df['open_time'])).strftime('%Y-%m-%d %H:%M:%S'))
# df=pd.DataFrame(df)
datetime_df = []
for index, row in df.iterrows():
    datetime_df.append(datetime.fromtimestamp(int(row['open_time']/1000)).strftime('%Y-%m-%d %H:%M:%S'))
blocks = np.array(datetime_df)
df['open_time'] = blocks.tolist()
df.rename(columns={'open_time':'DatetimeIndex'},inplace=True)
# df.set_index(df['DatetimeIndex'])
df=df.set_index('index')
df = df[df.columns[[1,2,3,4,5]]]  # берем столбцы без даты открытия и закрытия

print(df)



mpf.plot(df, type='candle', style='binance',
    title='',
    ylabel='',
    ylabel_lower='',
    volume=True)


# ft.app(target=Main().run)









