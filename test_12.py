import flet as ft

import asyncio
from src.graph.graph import Print_graph
import multiprocessing as mp
import time


class Main:
    def __init__(self):
        self.page: ft.Page = None

    def run(self, page):
        print('РИСУЕМ MAIN')
        self.page: ft.Page = page
        self.settings = ['BTCUSDT']

        
        self.page.title = "MIN"
        self.page.window_height, self.page.window_width = 1000, 1200
        self.page.theme_mode = "light" 
        self.main_print = ft.Container( # общий контейнер на страницу
            
        )
  

if __name__ == '__main__':
    main = Main()
    # asyncio.run(main.websocket_start())
    ft.app(target=Main().run)















