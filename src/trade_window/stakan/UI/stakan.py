import flet as ft


class Stakan_column(ft.UserControl):

    def build(self):
        
        self.stakan_column = ft.Container(
                content = ft.Text('Стакан',text_align='center'),
                width=110,
                height=600,
                bgcolor='#24c6d1',
                padding=0,
                margin=0
            )
        
        return self.stakan_column

