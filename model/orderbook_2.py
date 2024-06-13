import websocket
import requests
import threading
import json
from time import sleep


class Orderbook:
    def __init__(self, symbol):
        self.symbol = symbol
        # формируем ссылку для бодключения к вебсокетам 
        self._socket = "wss://fstream.binance.com/stream?streams="
        socet_symbol = ''
        for sym in self.symbol:
            socet_symbol += f'{sym.lower()}@depth@100ms/'
        self._socket = self._socket + socet_symbol
        self._socket = self._socket[:-1]
        # подключение к вебсокетам
        self._ws = websocket.WebSocketApp(self._socket, on_message=self.on_message, on_close=self.on_close)
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
            sleep(0.5)

    def _get_once_snapshot(self,_rest):
        r = requests.get(_rest)
        self._lock = True
        data = json.loads(r.text)
        self._last_update_id = data["lastUpdateId"]
        _bids = {float(price): float(qty) for price, qty in data["bids"]}
        _asks = {float(price): float(qty) for price, qty in data["asks"]}
        self._lock = False
        return _bids, _asks


    def on_close(self):
        print("Сессия закрыта")

    def on_message(self, message_str):
        while self._lock:
            pass
        print('Вебсокеты из ордербук')
        message = json.loads(message_str)
        print(message)
        if message["u"] >= self._last_update_id:
            #Просматривайте уровни цен и количества для получения информации о предложениях и запросах, а также обновляйте количество
            for price_level, qty in message["b"]:
                if float(qty) == 0:
                    self._bids.pop(float(price_level), None)
                else:
                    self._bids[float(price_level)] = float(qty)

            for price_level, qty in message["a"]:
                if float(qty) == 0:
                    self._asks.pop(float(price_level), None)
                else:
                    self._asks[float(price_level)] = float(qty)

        if self._prev_u != None and self._prev_u != message["pu"]:
            print("Рассинхронизация книги заказов приводит к появлению нового снимка")
            self._get_snapshot()

        self._prev_u = message["u"]

    def connect(self):
        wst = threading.Thread(target=self._ws.run_forever)
        wst.daemon = True
        wst.start()
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

symbol = ['BTCUSDT','NOTUSDT']

orderbook = Orderbook(symbol)
orderbook.connect()

bid_x = []
bid_z = []
ask_x = []
ask_z = []
y = [[0] * 100]

def set_depth():
    bid_data = orderbook.get_bids(symbol[0])
    bid_prices = sorted(bid_data.keys())[-100:]
    bid_quantities = [bid_data[price] for price in bid_prices]
    bid_depth = []
    cumulative_volume = 0
    for qty in bid_quantities[::-1]:
        cumulative_volume += qty
        bid_depth.append(cumulative_volume)

    bid_depth = bid_depth[::-1]

    ask_data = orderbook.get_asks(symbol[0])
    ask_prices = sorted(ask_data.keys())[:100]
    ask_quantities = [ask_data[price] for price in ask_prices]
    ask_depth = []
    cumulative_volume = 0
    for qty in ask_quantities:
        cumulative_volume += qty
        ask_depth.append(cumulative_volume)

    bid_x.append(bid_prices)
    bid_z.append(bid_depth)
    ask_x.append(ask_prices)
    ask_z.append(ask_depth)

    print(f'{bid_x[0][-1]} | {bid_z[0][-1]}')
    y.append([y[-1][0] + 100] * 100)

    if len(y) > 10:
        del bid_x[0]
        del bid_z[0]
        del ask_x[0]
        del ask_z[0]
        del y[0]

def update_data():
    while True:
        set_depth()
        sleep(0.1)

def did_mount():
    myThread = threading.Thread(target=update_data, args=(), daemon=True)
    myThread.start()


did_mount()







