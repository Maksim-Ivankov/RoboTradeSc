import flet as ft
from src.trade_window.stakan.stakan import Stakan
from src.trade_window.finrez.finrez import Finrez
from src.trade_window.big_trade.big_trade import Big_trade
from src.trade_window.likvidnost.likvidnost import Likvidnost
from src.trade_window.robot_trade.robot_trade import Robot_trade
from src.trade_window.dev.dev import Dev   
from model.orderbook_3 import Orderbook 
import asyncio
# import threading
import multiprocessing as mp
import time


class Main:
    def __init__(self):
        self.page: ft.Page = None
        
        # loop22734 = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop22734)
        # loop22734 = asyncio.get_event_loop()
        # loop22734.run_until_complete(self.websocket_start()) 

        # thread76544 = threading.Thread(target=self.websocket_start())
        # thread76544.start()
        # p=mp.Process(target=self.websocket_start)
        # p.start()

    async def websocket_start(self):
        
        await self.orderbook.connect() 

    def run(self, page):
        self.page: ft.Page = page
        self.settings = ['BTCUSDT','NOTUSDT']
        self.orderbook = Orderbook(self.settings)
        self.orderbook.connect() 
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
                                        # ft.Text('111')
                                        Stakan(self.settings[0],self.orderbook), # передаем монету и объект - оредрбук для доступа к нему
                                        Stakan(self.settings[1],self.orderbook),
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


# thread7654 = threading.Thread(target=ft.app(target=Main().run))
# thread7654.start()
           
# loop22734 = asyncio.new_event_loop()
# asyncio.set_event_loop(loop22734)
# loop22734 = asyncio.get_event_loop()
# loop22734.run_until_complete(ft.app(target=Main().run)) 
if __name__ == '__main__':
    main = Main()
    # asyncio.run(main.websocket_start())
    ft.app(target=Main().run)