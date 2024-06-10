import flet as ft
from model.orderbook import Orderbook
from threading import Event, Thread
from time import sleep
import time, threading


def call_repeatedly(interval, func):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # Интервал обновления
            func()
    Thread(target=loop).start()    
    return stopped.set

    

symbol = "btcusdt"

#Проверьте, был ли указан символ в качестве аргумента, в противном случае по умолчанию используется значение DEFAULT_SYMBOL

orderbook = Orderbook(symbol)
orderbook.connect()



bid_x = []
bid_z = []
ask_x = []
ask_z = []
y = [[0] * 100]
flag_set_depth_once = 0

# получаем данные с вебсокетов
def set_depth():
    global flag_set_depth_once
    bid_data = orderbook.get_bids()
    bid_prices = sorted(bid_data.keys())[-20:]
    bid_quantities = [bid_data[price] for price in bid_prices]
    bid_depth = []
    cumulative_volume = 0
    for qty in bid_quantities[::-1]:
        cumulative_volume += qty
        bid_depth.append(cumulative_volume)

    bid_depth = bid_depth[::-1]

    ask_data = orderbook.get_asks()
    ask_prices = sorted(ask_data.keys())[:20]
    ask_quantities = [ask_data[price] for price in ask_prices]
    ask_depth = []
    cumulative_volume = 0
    for qty in ask_quantities:
        cumulative_volume += qty
        ask_depth.append(cumulative_volume)

    bid_x.append(bid_prices)
    bid_z.append(bid_depth)
    ask_x.append(ask_prices)
    ask_z.append(ask_depth)

    # print(f'{bid_x[0][-1]} | {bid_z[0][-1]}')
    y.append([y[-1][0] + 100] * 100)

    if len(y) > 10:
        del bid_x[0]
        del bid_z[0]
        del ask_x[0]
        del ask_z[0]
        del y[0]
    # page.update()
    # stakan_work.stakan_data(bid_x,bid_z,ask_x,ask_z)
    return bid_x,bid_z,ask_x,ask_z




class Stakan_column(ft.UserControl):
    def did_mount(self):
        self.running = True
        self.myThread = threading.Thread(target=self.update_data, args=(), daemon=True)
        self.myThread.start()

    def update_data(self):
        while self.running:
            # self.count_1+=1
            # self.countdown.value = self.count_1
            self.bid_prices,self.bid_depth,self.ask_prices,self.ask_depth = set_depth()
            data_ura = self.stakan_print()
            print(f'{self.items[18].content.controls} - {self.bid_depth[0][18]}')
            # self.controls.clear()
            self.controls = []
            self.controls.append(data_ura)
            self.update()
            time.sleep(0.1)

    def stakan_print(self):
        self.items = []
        for i in range(len(self.bid_prices[0])):
            self.items.append(
                ft.Container(
                    content=ft.Row(
                        controls=[ 
                            ft.Text(
                                value=round(self.bid_depth[0][i],1),
                                size=12
                            ),
                            ft.Text(
                                value=self.bid_prices[0][i],
                                size=12,
                            ),
                        ],  
                    ),
                    bgcolor = '#EDC6C6'
                )
            )
        for i in range(len(self.ask_prices[0])):
            # print(f'{ask_depth[i][0]} | {ask_prices[i][0]}')
            self.items.append(
                ft.Container(
                    content=ft.Row(
                        controls=[ 
                            ft.Text(
                                value=round(self.ask_depth[0][i],1),
                                size=12
                            ),
                            ft.Text(
                                value=self.ask_prices[0][i],
                                size=12,
                            ),                        
                        ],
                    ),
                    bgcolor = '#A0DBC6'
                )
            )
        stakan_column = ft.Container(
                content = ft.Column(
                    spacing=0, 
                    controls=self.items,
                    scroll=ft.ScrollMode.HIDDEN
                    # scrollMode = 'HIDDEN '
                ),    
                width=110,
                height=600,
                bgcolor='#24c6d1',
                padding=0,
                margin=0,
                
            )
        return stakan_column

    def build(self):
        self.bid_prices,self.bid_depth,self.ask_prices,self.ask_depth = set_depth()
        stakan_column = self.stakan_print()
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

