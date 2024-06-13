import websockets
import json
import asyncio, time

symbol = ['btcusdt','notusdt']



# формируем ссылку для бодключения к вебсокетам 
_socket = "wss://fstream.binance.com/stream?streams="
socet_symbol = ''
for sym in symbol:
    socet_symbol += f'{sym.lower()}@depth@100ms/'
_socket = _socket + socet_symbol
_socket = _socket[:-1]

# запускаем вебсокеты, когда вошли в сделку, следим за монетой, рисуем график и данные в реальном времени    
async def websocket_trade():
    try:
        async with websockets.connect(_socket) as ws:
            while True:        
                try:
                    data = json.loads(await ws.recv())['data']
                    if data['s'] == 'NOTUSDT':
                        print(data['b'][0][-1])
                except websockets.exceptions.ConnectionClosed:
                    break
    except Exception as e:
        print(f'Ошибка - {e}')



loop22 = asyncio.new_event_loop()
asyncio.set_event_loop(loop22)
loop22 = asyncio.get_event_loop()
loop22.run_until_complete(websocket_trade()) 







