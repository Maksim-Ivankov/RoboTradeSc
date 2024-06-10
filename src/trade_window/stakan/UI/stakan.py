import flet as ft
from model.orderbook import Orderbook
from threading import Event, Thread
from time import sleep



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

# получаем данные с вебсокетов
def set_depth():
    bid_data = orderbook.get_bids()
    bid_prices = sorted(bid_data.keys())[-100:]
    bid_quantities = [bid_data[price] for price in bid_prices]
    bid_depth = []
    cumulative_volume = 0
    for qty in bid_quantities[::-1]:
        cumulative_volume += qty
        bid_depth.append(cumulative_volume)

    bid_depth = bid_depth[::-1]

    ask_data = orderbook.get_asks()
    ask_prices = sorted(ask_data.keys())[:100]
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

    print(f'{bid_x[0][-1]} | {bid_z[0][-1]}')
    y.append([y[-1][0] + 100] * 100)

    if len(y) > 10:
        del bid_x[0]
        del bid_z[0]
        del ask_x[0]
        del ask_z[0]
        del y[0]
    return bid_x,bid_z,ask_x,ask_z




class Stakan_column(ft.UserControl):
    def __init__(self,bid_prices,bid_depth,ask_prices,ask_depth):
        self.bid_prices = bid_prices
        self.bid_depth = bid_depth
        self.ask_prices = ask_prices
        self.ask_depth = ask_depth
        
    def stakan_data(self,bid_prices,bid_depth,ask_prices,ask_depth):
        self.bid_prices = bid_prices
        self.bid_depth = bid_depth
        self.ask_prices = ask_prices
        self.ask_depth = ask_depth

    def build(self):
        items = []
        for i in range(len(self.bid_prices[0])):
            items.append(
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
            items.append(
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
                    controls=items,
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

bid_prices,bid_depth,ask_prices,ask_depth = set_depth()


stakan_work = Stakan_column(bid_prices,bid_depth,ask_prices,ask_depth)

cancel_future_calls = call_repeatedly(0.1, stakan_work.stakan_data)
        
        
        




    

































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

