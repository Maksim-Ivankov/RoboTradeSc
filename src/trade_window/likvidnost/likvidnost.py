import flet as ft


class Likvidnost(ft.UserControl):

    def build(self):
        
        self.likvidnost = ft.Container( # окно выбора монеты
                    content = ft.Text('Ликвидность',text_align='center',),
                    width=380,
                    height=150,
                    bgcolor='#d3eef0',
                    padding=20
                )
        
        return self.likvidnost




