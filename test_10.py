import websockets
import json
import asyncio, time

symbol = ['btcusdt','notusdt']


class lol:
    def __init__(self, symbol):
        self.symbol = symbol
        # формируем ссылку для бодключения к вебсокетам 
        self._socket = "wss://fstream.binance.com/stream?streams="
        socet_symbol = ''
        for sym in symbol:
            socet_symbol += f'{sym.lower()}@depth@100ms/'
        self._socket = self._socket + socet_symbol
        self._socket = self._socket[:-1]

        # запускаем вебсокеты, когда вошли в сделку, следим за монетой, рисуем график и данные в реальном времени    
    async def websocket_trade(self):
        try:
            async with websockets.connect(self._socket) as ws:
                while True:        
                    try:
                        data = json.loads(await ws.recv())['data']
                        if data['s'] == 'NOTUSDT':
                            print(data['b'][0][-1])
                    except websockets.exceptions.ConnectionClosed:
                        break
        except Exception as e:
            print(f'Ошибка - {e}')



lolka = lol(symbol)

loop22 = asyncio.new_event_loop()
asyncio.set_event_loop(loop22)
loop22 = asyncio.get_event_loop()
loop22.run_until_complete(lolka.websocket_trade()) 







