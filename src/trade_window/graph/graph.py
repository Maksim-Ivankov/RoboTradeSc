import flet as ft

class Graph(ft.UserControl):

    def build(self):
        
        self.graph = ft.Container( # окно выбора монеты
                    content = ft.Text('График',text_align='center',),
                    width=250,
                    height=200,
                    bgcolor='#d3eef0',
                    padding=20
                )
        
        return self.graph

