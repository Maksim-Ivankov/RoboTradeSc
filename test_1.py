import flet as ft
import websockets
import json
import asyncio

symbol='BTCUSDT'


async def main(page: ft.Page):

    async def websocket_trade():
        url = 'wss://fstream.binance.com/stream?streams='+symbol.lower()+'@miniTicker'
        async with websockets.connect(url) as ws:
            while True: 
                data = json.loads(await ws.recv())['data'] 
                print(data['c'])
                text.value = data['c']
                await page.update_async()

    # page.window_center()
    page.theme_mode='light'
    page.horizontal_alignment = 'center'
    page.window_width = 200
    page.window_height = 200
    text = ft.Text('ЛОЛО')
   
    # loop22 = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop22)
    # loop22 = asyncio.new_event_loop()
    # loop22.run_until_complete(websocket_trade()) 


    

    await page.add_async(text)

    await websocket_trade()
ft.app(target=main)

# import asyncio
# import flet as ft

# async def main(page: ft.Page):

#     await page.add_async(
#         ft.Text("Hello!"),
#         ft.ElevatedButton("Call async method")
#     )

# ft.app(target=main)