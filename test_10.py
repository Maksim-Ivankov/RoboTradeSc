import websockets
import json
import asyncio, time
import requests

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

        self._bids = {}
        self._asks = {}
        self._last_update_id = 0
        self._prev_u = None
        self._lock = False
        self.bid_x = []
        self.bid_z = []
        self.ask_x = []
        self.ask_z = []
        self.y = [[0] * 100]
        self.data_socket = {}

    def _get_snapshot(self):
        """Сбросьте значения _bids и _asks на моментальный снимок текущей книги заказов и обновите last_update_id."""
        for sym in self.symbol:
            rest = f"https://fapi.binance.com/fapi/v1/depth?symbol={sym.lower()}&limit=1000"
            _bids,_asks = self._get_once_snapshot(rest)
            self.data_socket[sym] = [_bids,_asks]
            print(f'Получили снепшот {sym}')
            time.sleep(0.5)

    def _get_once_snapshot(self,_rest):
        r = requests.get(_rest)
        self._lock = True
        data = json.loads(r.text)
        self._last_update_id = data["lastUpdateId"]
        _bids = {float(price): float(qty) for price, qty in data["bids"]}
        _asks = {float(price): float(qty) for price, qty in data["asks"]}
        self._lock = False
        return _bids, _asks

    def connect(self):
        loop22 = asyncio.new_event_loop()
        asyncio.set_event_loop(loop22)
        loop22 = asyncio.get_event_loop()
        loop22.run_until_complete(self.websocket_trade()) 
        print('Стартовали поток с вебсокетами')
        self._get_snapshot()

    def get_quotes(self) -> tuple[float, float]:
        """Return best bid and ask"""
        return max(self._bids.keys()), min(self._asks.keys())
    
    def get_bids(self,symbol):
        """Return bids"""
        return self.data_socket[symbol][0]
    
    def get_asks(self,symbol):
        """Return asks"""
        return self.data_socket[symbol][1]

        # запускаем вебсокеты, когда вошли в сделку, следим за монетой, рисуем график и данные в реальном времени    
    async def websocket_trade(self):
        try:
            async with websockets.connect(self._socket) as ws:
                while True:        
                    try:
                        message = json.loads(await ws.recv())['data']
                        print(message)
                        for sym in self.symbol:
                            if message['s'] == sym:
                                if message["u"] >= self._last_update_id:
                                    for price_level, qty in message["b"]:
                                        if float(qty) == 0:
                                            self.data_socket[sym][0].pop(float(price_level), None)
                                        else:
                                            self.data_socket[sym][0][float(price_level)] = float(qty)
                                    for price_level, qty in message["a"]:
                                        if float(qty) == 0:
                                            self.data_socket[sym][1].pop(float(price_level), None)
                                        else:
                                            self.data_socket[sym][1][float(price_level)] = float(qty)
                                if self._prev_u != None and self._prev_u != message["pu"]:
                                    print("Рассинхронизация книги заказов приводит к появлению нового снимка")
                                    self._get_snapshot()
                                self._prev_u = message["u"]

                    except websockets.exceptions.ConnectionClosed:
                        break
        except Exception as e:
            print(f'Ошибка - {e}')

# self.data_socket[sym] = [_bids,_asks]
# self.data_socket[message['s']] = [_bids,_asks]
# self.data_socket[sym][0]

lolka = lol(symbol)
lolka.connect()







