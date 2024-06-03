
import flet as ft


class Lenta(ft.UserControl):

    def build(self):
        
        self.lenta = ft.Container(
                content = ft.Text('Лента',text_align='center'),
                width=57,
                height=600,
                bgcolor='#24c6d1',
                padding=0,
                margin=0
            )
        
        return self.lenta
