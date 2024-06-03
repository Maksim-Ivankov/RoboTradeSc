import flet as ft
from src.trade_window.graph.graph import Graph


class Stakan(ft.UserControl):

    def build(self):
        
        self.stakan = ft.Column(
            width=250,
            controls=[
                ft.Container( # окно выбора монеты
                    content = ft.Row(),
                    width=250,
                    height=30,
                    bgcolor='#d3eef0',
                ),
                ft.Container( # окно инфо и масштаба
                    content = ft.Row(),
                    width=250,
                    height=30,
                    bgcolor='#d3eef0',
                ),
                ft.Container( # стакан контейнер
                    content = ft.Row(
                        controls=[
                            ft.Container(
                                content = ft.Row(),
                                width=50,
                                height=600,
                                bgcolor='#24c6d1',
                                padding=0,
                                margin=0
                            ),
                            ft.Container(
                                content = ft.Row(),
                                width=57,
                                height=600,
                                bgcolor='#24c6d1',
                            ),
                            ft.Container(
                                content = ft.Row(),
                                width=110,
                                height=600,
                                bgcolor='#24c6d1',
                            ),
                            ft.Container(
                                content = ft.Row(),
                                width=30,
                                height=600,
                                bgcolor='#24c6d1',
                            )
                        ],
                        spacing=1
                    ),
                    width=250,
                    height=600,
                    bgcolor='#d3eef0',
                ),
                ft.Container( # График
                    content = Graph(),
                    width=250,
                    height=200,
                    bgcolor='#d3eef0',
                ),
            ],
            spacing=1
        )

        return self.stakan
    
    














