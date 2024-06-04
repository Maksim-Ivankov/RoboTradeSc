import flet as ft


class Order(ft.UserControl):

    def build(self):
        
        self.order = ft.Container(
                content = ft.Text('100',text_align='center'),
                width=30,
                height=600,
                bgcolor='#24c6d1',
                padding=0,
                margin=0
            )
        
        return self.order

