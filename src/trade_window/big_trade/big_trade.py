import flet as ft


class Big_trade(ft.UserControl):

    def build(self):
        
        self.big_trade = ft.Container( # окно выбора монеты
                    content = ft.Text('Крупные заявки',text_align='center',),
                    width=380,
                    height=400,
                    bgcolor='#d3eef0',
                    padding=20
                )
        
        return self.big_trade




