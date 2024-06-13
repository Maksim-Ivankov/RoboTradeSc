import flet as ft
from src.trade_window.stakan.stakan import Stakan
from src.trade_window.finrez.finrez import Finrez
from src.trade_window.big_trade.big_trade import Big_trade
from src.trade_window.likvidnost.likvidnost import Likvidnost
from src.trade_window.robot_trade.robot_trade import Robot_trade
from src.trade_window.dev.dev import Dev   
from model.orderbook_2 import Orderbook 
import time, threading


settings = ['DOGEUSDT','NOTUSDT']
orderbook = Orderbook(settings)
orderbook.connect()


class Main:
    def __init__(self):
        self.page: ft.Page = None
        self.bid_x = []
        self.bid_z = []
        self.ask_x = []
        self.ask_z = []
        self.y = [[0] * 100]
        self.bid_count = 30
        self.ask_count = 30
        self.did_mount()

    def did_mount(self):
        print('МОНТИРОВАНИЕ')
        self.running = True
        self.myThread = threading.Thread(target=self.update_data22, args=(), daemon=True)
        self.myThread.start()

    def update_data22(self):
        while self.running:
            bid_data = orderbook.get_bids(settings[0])
            bid_prices = sorted(bid_data.keys())[-self.bid_count:]
            bid_quantities = [bid_data[price] for price in bid_prices]
            bid_depth = []
            cumulative_volume = 0
            for qty in bid_quantities[::-1]:
                bid_depth.append(qty)
            bid_depth = bid_depth[::-1]
            # print(f'{bid_x[0][-1]} | {bid_z[0][-1]}')
            self.bid_x.append(bid_prices)
            self.bid_z.append(bid_depth)
            print(f'{self.bid_x[0][-1]} | {self.bid_z[0][-1]}')
            # Без штуки ниже не обновляется график
            self.y.append([self.y[-1][0] + 100] * 100)
            if len(self.y) > 15:
                del self.bid_x[0]
                del self.bid_z[0]
                del self.y[0]
            
            # self.update()
            time.sleep(0.1)

    def run(self, page):
        self.page: ft.Page = page
        self.page.title = "MIN"
        self.page.window_height, self.page.window_width = 1000, 1200
        # self.page.scroll = ft.ScrollMode.HIDDEN
        # self.page.padding = ft.Padding(5, 0, 5, 0)
        self.page.theme_mode = "light" 
        self.main_print = ft.Container( # общий контейнер на страницу
            content = ft.Row( # в контейнере 1 ряд
                controls=[ # состоящий из двух контейнеров - обертки стаканов и доп панели индикаторова
                    ft.Container( # обертка стаканов состоит из ряда
                        content = ft.Column(
                            controls=[
                                ft.Row( # в которых 3 стакана
                                    controls=[
                                        ft.Text('111')
                                        # Stakan(settings[0],orderbook), # передаем монету и объект - оредрбук для доступа к нему
                                        # Stakan(settings[1],orderbook),
                                        # Stakan(self.settings[2]),
                                    ],
                                    expand = True
                                ),
                                Dev()
                            ]
                        ),
                        expand = True,
                    ),
                    ft.Container( # обертка индикаторов состоит из колонки
                        content = ft.Column(
                            controls=[
                                Finrez(),
                                Big_trade(),
                                Likvidnost(),
                                Robot_trade()
                            ],
                            width=380,
                            expand = True,
                        ),
                        width=380,
                    )
                ]
            ),
            expand = True
        )
        self.page.add(self.main_print)


    
        

ft.app(target=Main().run)