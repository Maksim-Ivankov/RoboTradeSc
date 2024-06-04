import flet as ft
from model.orderbook import Orderbook
import threading
from time import sleep

class Stakan_column(ft.UserControl):
    def __init__(self,symbol):
        super().__init__()
        self.symbol = symbol
        
    def build(self):
        self.orderbook = Orderbook(self.symbol)
        self.orderbook.connect()

        def potok():
            while True:
                sleep(1)   
                bid_data = self.orderbook.get_bids()
                bid_prices = sorted(bid_data.keys())[-100:]
                bid_quantities = [bid_data[price] for price in bid_prices]
                bid_depth = []
                cumulative_volume = 0
                for qty in bid_quantities[::-1]:
                    cumulative_volume += qty
                    bid_depth.append(cumulative_volume)

                bid_depth = bid_depth[::-1]

                ask_data = self.orderbook.get_asks()
                ask_prices = sorted(ask_data.keys())[:100]
                ask_quantities = [ask_data[price] for price in ask_prices]
                ask_depth = []
                cumulative_volume = 0
                print(bid_prices)
                for qty in ask_quantities:
                    cumulative_volume += qty
                    ask_depth.append(cumulative_volume)
                return bid_prices,bid_depth,ask_prices,ask_depth
                # await self.stakan_column.update_async()


        def items():
            
            
            bid_prices,bid_depth,ask_prices,ask_depth = potok()
            items = []
            for i in range(len(bid_prices)):
                items.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[ 
                                ft.Text(
                                    value=round(bid_depth[i],1),
                                    size=12
                                ),
                                ft.Text(
                                    value=bid_prices[i],
                                    size=12,
                                    text_align='right'
                                ),
                            ],  
                        ),
                        bgcolor = '#EDC6C6'
                    )
                )
            for i in range(len(ask_prices)):
                items.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[ 
                                ft.Text(
                                    value=round(ask_depth[i],1),
                                    size=12
                                ),
                                ft.Text(
                                    value=ask_prices[i],
                                    size=12,
                                    text_align='right'
                                ),                        
                            ],
                        ),
                        bgcolor = '#A0DBC6'
                    )
                )
            return items

        
        self.stakan_column = ft.Container(
                content = ft.Column(
                    spacing=0, 
                    controls=items(),
                    scroll=ft.ScrollMode.HIDDEN
                    
                    # scrollMode = 'HIDDEN '
                ),
                
                width=110,
                height=600,
                bgcolor='#24c6d1',
                padding=0,
                margin=0,
                
            )
        print('Посчитали стакан')
        # self.potok.update()
        # threading.Timer(1.0, self.build).start()
        return self.stakan_column




    

































# import flet as ft


# class Stakan_column(ft.UserControl):
#     def __init__(self,symbol):
#         super().__init__()
#         self.symbol = symbol


#     def build(self):
        
#         self.stakan_column = ft.Container(
#                 content = ft.Text('Стакан',text_align='center'),
#                 width=110,
#                 height=600,
#                 bgcolor='#24c6d1',
#                 padding=0,
#                 margin=0
#             )
        
#         return self.stakan_column

