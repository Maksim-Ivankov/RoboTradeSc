import flet as ft
from src.trade_window.graph.graph import Graph
from src.trade_window.stakan.UI.stakan import Stakan_column
from src.trade_window.stakan.UI.lenta import Lenta
from src.trade_window.stakan.UI.nakopleniya import Nakopleniya
from src.trade_window.stakan.UI.order import Order
from src.trade_window.stakan.UI.change_symbol import Change_symbol
from src.trade_window.stakan.UI.resize import Resize


class Stakan(ft.UserControl):
    def __init__(self,symbol,orderbook):
        super().__init__()
        self.symbol = symbol
        self.orderbook = orderbook



    def build(self):
        self.stakan = ft.Column(
            width=250,
            controls=[
                Change_symbol(self.symbol),
                Resize(self.symbol),
                ft.Container( # стакан контейнер
                    content = ft.Row(
                        controls=[
                            Nakopleniya(),
                            Lenta(),
                            Stakan_column(self.symbol,self.orderbook),
                            Order()
                        ],
                        spacing=1,
                        expand = True
                    ),
                    width=250,
                    bgcolor='#d3eef0',
                    expand = True
                    
                ),
                ft.Container( # График
                    content = Graph(),
                    width=250,
                    height=200,
                    bgcolor='#d3eef0',
                ),
            ],
            spacing=1,
            

        )
        
        return self.stakan
    
    














