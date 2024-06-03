import flet as ft


class Finrez(ft.UserControl):

    def build(self):
        
        self.finrez = ft.Container( # окно выбора монеты
                    content = ft.Text('Финрез',text_align='center',),
                    width=380,
                    height=100,
                    bgcolor='#d3eef0',
                    padding=20
                )
        
        return self.finrez
















