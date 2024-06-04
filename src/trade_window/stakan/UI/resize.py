import flet as ft


class Resize(ft.UserControl):
    def __init__(self,symbol):
        super().__init__()
        self.symbol = symbol


    def build(self):
        
        self.resize = ft.Container(
                content = ft.Row(
                    controls=[
                        ft.IconButton(
                            ft.icons.REMOVE_CIRCLE_SHARP, 
                            on_click=self.click_plus,
                            icon_size=17,
                            width=20,
                            height=20,
                            # padding=0      
                        ),
                        ft.IconButton(
                            ft.icons.ADD_CIRCLE_SHARP,
                            on_click=self.click_minus,
                            icon_size=17,
                            width=20,
                            height=20,
                            # padding=0
                        ),
                        ft.Text('X10'),
                        ft.Text(f'BNC:FT:{self.symbol}'),
                    ]
            ),
            width=250,
            height=30,
            # bgcolor='#24c6d1',
            padding=5,
            margin=0,
        )
        
        
        return self.resize

    def click_plus(self,e):
        print(e)

    def click_minus(self,e):
        print(e)