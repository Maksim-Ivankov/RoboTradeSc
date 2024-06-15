import flet as ft
from src.graph.graph import Print_graph

class Graph(ft.UserControl):
    def __init__(self,symbol,orderbook):
        super().__init__()
        self.symbol = symbol
        self.orderbook = orderbook


    def build(self):     
        graph = Print_graph(self.symbol,'5m')   
        self.graph = ft.Container( # окно выбора монеты
                    content = graph.print_graph(),
                    width=250,
                    height=200,
                    bgcolor='#d3eef0',
                )
        
        return self.graph

