import flet as ft
import multiprocessing as mp
import mplfinance as mpf
import requests
import pandas as pd

# import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from flet.matplotlib_chart import MatplotlibChart
# from mpl_finance import candlestick_ohlc 
from datetime import datetime



# import matplotlib.dates as mpl_dates 



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
        # datetime_df = []
        # for index, row in df.iterrows():
        #     datetime_df.append(datetime.fromtimestamp(int(row['open_time']/1000)).strftime('%H:%M'))
        # blocks = np.array(datetime_df)
        # df['open_time'] = blocks.tolist()
        df = df[df.columns[[1,2,3,4]]]  # берем столбцы без даты открытия и закрытия
        print(df)
        # print(df)
        # self.main_print = mpf.plot(df, type='candle', style='binance',title='',ylabel='',ylabel_lower='',volume=True)
        # fig, ax = plt.subplots() 
        # candlestick_ohlc(ax, df.values, width=0.6, colorup='green', colordown='red', alpha=0.8) 
        # # ax.set_xlabel('Date') 
        # # ax.set_ylabel('Price') 
        # fig.suptitle('BTCUSDT') 
        # fig.tight_layout()

        # date_format = mpl_dates.DateFormatter('%H:%M') 
        # ax.xaxis.set_major_formatter(date_format) 
        # fig.autofmt_xdate() 

        fig = plt.figure()

        #define width of candlestick elements
        width = .4
        width2 = .05

        #define up and down prices
        up = df[df.close >=df.open ]
        down = df[df.close <df.open ]

        #define colors to use
        col1 = 'green'
        col2 = 'red'

        #plot up prices
        plt.bar (up.index ,up. close -up. open ,width,bottom=up. open ,color=col1)
        plt.bar (up.index ,up. high -up. close ,width2,bottom=up. close ,color=col1)
        plt.bar (up.index ,up. low -up. open ,width2,bottom=up. open ,color=col1)

        #plot down prices
        plt.bar (down.index ,down. close -down. open ,width,bottom=down. open ,color=col2)
        plt.bar (down.index ,down. high -down. open ,width2,bottom=down. open ,color=col2)
        plt.bar (down.index ,down. low -down. close ,width2,bottom=down. close ,color=col2)

        #rotate x-axis tick labels
        plt.xticks (rotation= 45 , ha='right')

        

        self.main_print = MatplotlibChart(fig, expand=True)

        self.page.add(self.main_print)
        





ft.app(target=Main().run)









