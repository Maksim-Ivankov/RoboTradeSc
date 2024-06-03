import flet as ft


class Change_symbol(ft.UserControl):
    def __init__(self,symbol):
        super().__init__()
        self.symbol = symbol


    def build(self):

        

        self.change_symbol = ft.Container(
                content = ft.Row(
                    controls=[
                        ft.Container( # отображение движения за день в процентах
                            content=ft.Text(
                                '+15%',
                                size=12,
                                color='#2c2e2c',
                                text_align='center',  
                            ),
                            width=50,
                            height=30,
                            bgcolor='#0ECB81',
                            # bgcolor='#F6465D',
                            padding=0,
                            margin=0

                        ),
                        ft.FilledButton(
                            text=self.symbol,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=0),
                                bgcolor={ft.MaterialState.FOCUSED: ft.colors.PINK_200, "": '#C0D2CE'},
                                color={
                                    ft.MaterialState.HOVERED: ft.colors.BLACK,
                                    ft.MaterialState.FOCUSED: ft.colors.BLACK,
                                    ft.MaterialState.DEFAULT: ft.colors.BLACK,
                                },
                                padding = 0
                            ),
                            width=100
                        ),
                        ft.FilledButton(
                            text='FUTURES',
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=0),
                                bgcolor={ft.MaterialState.FOCUSED: ft.colors.PINK_200, "": '#C0D2CE'},
                                color={
                                    ft.MaterialState.HOVERED: ft.colors.BLACK,
                                    ft.MaterialState.FOCUSED: ft.colors.BLACK,
                                    ft.MaterialState.DEFAULT: ft.colors.BLACK,
                                },
                                padding = 0
                            ),
                            width=80
                        ),
                    ]
                ),
                width=250,
                height=20,
                # bgcolor='#24c6d1',
                padding=0,
                margin=0
            )
        
        return self.change_symbol

    def change_symbol(self,e):
        print(e)