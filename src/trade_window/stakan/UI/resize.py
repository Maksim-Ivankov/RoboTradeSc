import flet as ft


class Resize(ft.UserControl):

    def build(self):
        
        self.resize = ft.Container(
                content = ft.Text('Изменить размер',text_align='center'),
                width=250,
                height=30,
                bgcolor='#24c6d1',
                padding=0,
                margin=0
            )
        
        return self.resize

