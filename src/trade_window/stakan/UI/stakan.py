import flet as ft
from model.orderbook import Orderbook
from threading import Event, Thread
from time import sleep
import time, threading
import numpy as np

def call_repeatedly(interval, func):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # Интервал обновления
            func()
    Thread(target=loop).start()    
    return stopped.set

class Stakan_column(ft.UserControl):

    def did_mount(self):
        self.running = True
        self.myThread = threading.Thread(target=self.update_data, args=(), daemon=True)
        self.myThread.start()

    
    # получаем данные с вебсокетов
    def set_depth(self):
        bid_data = self.orderbook.get_bids()
        bid_prices = sorted(bid_data.keys())[-self.bid_count:]
        bid_quantities = [bid_data[price] for price in bid_prices]
        bid_depth = []
        cumulative_volume = 0
        for qty in bid_quantities[::-1]:
            bid_depth.append(qty)

        bid_depth = bid_depth[::-1]

        ask_data = self.orderbook.get_asks()
        ask_prices = sorted(ask_data.keys())[:self.ask_count]
        ask_quantities = [ask_data[price] for price in ask_prices]
        ask_depth = []
        cumulative_volume = 0
        for qty in ask_quantities:
            ask_depth.append(qty)

        self.bid_x.append(bid_prices)
        self.bid_z.append(bid_depth)
        self.ask_x.append(ask_prices)
        self.ask_z.append(ask_depth)

        # print(f'{bid_x[0][-1]} | {bid_z[0][-1]}')
        # Без штуки ниже не обновляется график
        self.y.append([self.y[-1][0] + 100] * 100)
        if len(self.y) > 15:
            del self.bid_x[0]
            del self.bid_z[0]
            del self.ask_x[0]
            del self.ask_z[0]
            del self.y[0]
        # Отчищаем нулевые значения
        # print([i if j=='0.0' else -1 for i,j in enumerate(bid_z)])
        # print(bid_z)

        return self.bid_x,self.bid_z,self.ask_x,self.ask_z

    def update_data(self):
        while self.running:
            self.bid_prices,self.bid_depth,self.ask_prices,self.ask_depth = self.set_depth()
            data_ura = self.stakan_print()
            self.controls = []
            self.controls.append(data_ura)
            self.update()
            time.sleep(0.1)

    def stakan_print(self):
        self.items = []
        for i in range(len(self.bid_prices[0])):
            if round(self.bid_depth[0][i],1) != 0:
                self.items.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[ 
                                ft.Text(
                                    value=round(self.bid_depth[0][i],1),
                                    size=12,
                                    width=50,
                                ),
                                ft.Text(
                                    value=self.bid_prices[0][i],
                                    size=12,
                                    width=60,
                                ),
                            ],  
                        ),
                        bgcolor = '#EDC6C6',
                    )
                )
        for i in range(len(self.ask_prices[0])):
            # print(f'{ask_depth[i][0]} | {ask_prices[i][0]}')
            if round(self.ask_depth[0][i],1) != 0:
                self.items.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[ 
                                ft.Text(
                                    value=round(self.ask_depth[0][i],1),
                                    size=12,
                                    width=50,
                                ),
                                ft.Text(
                                    value=self.ask_prices[0][i],
                                    size=12,
                                    width=60,
                                ),                        
                            ],
                        ),
                        bgcolor = '#A0DBC6',
                    )
                )
        stakan_column = ft.Column(
                    spacing=0, 
                    controls=self.items,
                    scroll=ft.ScrollMode.HIDDEN,
                    width=110,
                )
        return stakan_column

    def build(self):
        symbol = "btcusdt"
        self.orderbook = Orderbook(symbol)
        self.orderbook.connect()
        self.bid_x = []
        self.bid_z = []
        self.ask_x = []
        self.ask_z = []
        self.y = [[0] * 100]
        self.bid_count = 60
        self.ask_count = 60

        self.bid_prices,self.bid_depth,self.ask_prices,self.ask_depth = self.set_depth()
        stakan_column = self.stakan_print()



        time.sleep(1)
        return stakan_column
        




    

































# import flet as ft


# class Stakan_column(ft.UserControl):
#     def __init__(self,symbol):
#         super().__init__()
#         self.symbol = symbol


#     def build(self):
        
#         self.stakan_column = ft.Container(
#                 content = ft.Text('Стакан',text_align='center'),
#                 width=110,
#                 height=600,
#                 bgcolor='#24c6d1',
#                 padding=0,
#                 margin=0
#             )
        
#         return self.stakan_column

