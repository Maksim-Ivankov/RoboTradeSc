import flet as ft
import multiprocessing as mp
import mplfinance as mpf
import requests
import pandas as pd

# import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from flet.matplotlib_chart import MatplotlibChart
from mpl_finance import candlestick_ohlc 
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
        df = df[df.columns[[0,1,2,3,4]]]  # берем столбцы без даты открытия и закрытия
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

        
        # plot the data
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])

         # customization of the axis
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='both', direction='out', width=2, length=8,
                       labelsize=12, pad=8)
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_linewidth(2)
            # set the ticks of the x axis only when starting a new day
        # ax.set_xticks(data2[ndays[1],0])
        # ax.set_xticklabels(xdays, rotation=45, horizontalalignment='right')

        ax.set_ylabel('Quote ($)', size=20)
        ax.set_ylim([177, 196])

        candlestick_ohlc(ax, df.values, width=0.6, colorup='green', colordown='red', alpha=0.8) 

        

        self.main_print = MatplotlibChart(fig, expand=True)

        self.page.add(self.main_print)
        





ft.app(target=Main().run)









