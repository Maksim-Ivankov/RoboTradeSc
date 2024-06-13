import flet as ft
from src.trade_window.stakan.stakan import Stakan
from src.trade_window.finrez.finrez import Finrez
from src.trade_window.big_trade.big_trade import Big_trade
from src.trade_window.likvidnost.likvidnost import Likvidnost
from src.trade_window.robot_trade.robot_trade import Robot_trade
from src.trade_window.dev.dev import Dev    

from threading import Event, Thread


class Main:
    def __init__(self):
        self.page: ft.Page = None
        self.settings = {
           'symbol_1':'BTCUSDT',
           'symbol_2':'DOGEUSDT',
           'symbol_3':'LUNAUSDT',
        }

    def run(self, page):
        self.page: ft.Page = page
        self.page.title = "MIN"
        self.page.window_height, self.page.window_width = 1000, 1200
        # self.page.scroll = ft.ScrollMode.HIDDEN
        # self.page.padding = ft.Padding(5, 0, 5, 0)
        self.page.theme_mode = "light" 
        self.main_print = ft.Container( # общий контейнер на страницу
            content = ft.Row( # в контейнере 1 ряд
                controls=[ # состоящий из двух контейнеров - обертки стаканов и доп панели индикаторов
                    ft.Container( # обертка стаканов состоит из ряда
                        content = ft.Column(
                            controls=[
                                ft.Row( # в которых 3 стакана
                                    controls=[
                                        Stakan(self.settings['symbol_1']),
                                        Stakan(self.settings['symbol_2']),
                                        # Stakan(settings['symbol_3']),
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