import flet as ft


class Nakopleniya(ft.UserControl):

    def build(self):
        
        self.nakopleniya = ft.Container(
                content = ft.Text('Накопл',text_align='center'),
                width=50,
                expand = True,
                bgcolor='#24c6d1',
                padding=0,
                margin=0
            )
        
        return self.nakopleniya
