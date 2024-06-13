import flet as ft
from src.trade_window.stakan.stakan import Stakan
from src.trade_window.finrez.finrez import Finrez
from src.trade_window.big_trade.big_trade import Big_trade
from src.trade_window.likvidnost.likvidnost import Likvidnost
from src.trade_window.robot_trade.robot_trade import Robot_trade
from src.trade_window.dev.dev import Dev    

from threading import Event, Thread

settings = {
    'symbol_1':'BTCUSDT',
    'symbol_2':'DOGEUSDT',
    'symbol_3':'LUNAUSDT',
}

def call_repeatedly(interval, func):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # Интервал обновленияm,
            func()
    Thread(target=loop).start()    
    return stopped.set

def main(page: ft.Page):
    # page.window_center()

    page.theme_mode='light'
    page.horizontal_alignment = 'center'
    page.window_width = 1200
    page.window_height = 1000
    main_print = ft.Container( # общий контейнер на страницу
        content = ft.Row( # в контейнере 1 ряд
            controls=[ # состоящий из двух контейнеров - обертки стаканов и доп панели индикаторов
                ft.Container( # обертка стаканов состоит из ряда
                    content = ft.Column(
                        controls=[
                            ft.Row( # в которых 3 стакана
                                controls=[
                                    Stakan(settings['symbol_1']),
                                    # Stakan(settings['symbol_2']),
                                    # Stakan(settings['symbol_3']),
                                ]
                            ),
                            Dev()
                        ]
                    ),
                ),
                ft.Container( # обертка индикаторов состоит из колонки
                    content = ft.Column(
                        controls=[
                            Finrez(),
                            Big_trade(),
                            Likvidnost(),
                            Robot_trade()
                        ]
                    )
                )
            ]
        )
    )
    page.add(main_print)
    # page.update()
    
    # def update_stakan():
    #     # stakan_1.stakan_1.print_stakan()
    #     stakan_1.print()
    #     page.update()

    # # stakan_1.stakan_1.update_async()
    
    # cancel_future_calls = call_repeatedly(0.1, update_stakan )    
        


ft.app(target=main)