import websockets
import json
import asyncio

symbol = 'BTCUSDT'


# запускаем вебсокеты, когда вошли в сделку, следим за монетой, рисуем график и данные в реальном времени    
async def websocket_trade():
    try:

        url = 'wss://fstream.binance.com/stream?streams='+symbol.lower()+'@miniTicker'
        async with websockets.connect(url) as ws:
            while True:        
                try:
                    data = json.loads(await ws.recv())['data']
                    print(f"Текущая цена: {data['c']}")
                        
                except websockets.exceptions.ConnectionClosed:
                    break
    except Exception as e:
        print(f'Ошибка - {e}')


loop22 = asyncio.new_event_loop()
asyncio.set_event_loop(loop22)
loop22 = asyncio.get_event_loop()
loop22.run_until_complete(websocket_trade()) 




