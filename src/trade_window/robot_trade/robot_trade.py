import flet as ft


class Robot_trade(ft.UserControl):

    def build(self):
        
        self.robot_trade = ft.Container( # окно выбора монеты
                    content = ft.Text('Идентичные сделки',text_align='center',),
                    width=380,
                    height=250,
                    bgcolor='#d3eef0',
                    padding=20
                )
        
        return self.robot_trade

