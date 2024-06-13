import flet as ft


class Dev(ft.UserControl):

    def build(self):
        
        self.dev = ft.Container( # окно выбора монеты
                    content = ft.Text('Окно разработчика',text_align='center'),
                    height=60,
                    bgcolor='#d3eef0',
                    padding=20,
                    expand = True,
                )
        
        return self.dev



