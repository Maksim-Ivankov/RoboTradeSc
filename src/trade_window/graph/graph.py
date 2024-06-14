import flet as ft
import mplfinance as mpf

class Graph(ft.UserControl):
    def __init__(self,symbol,orderbook):
        super().__init__()
        self.symbol = symbol
        self.orderbook = orderbook


    def build(self):        
        self.graph = ft.Container( # окно выбора монеты
                    content = ft.Text('График',text_align='center',),
                    width=250,
                    height=200,
                    bgcolor='#d3eef0',
                    padding=20
                )
        
        return self.graph

