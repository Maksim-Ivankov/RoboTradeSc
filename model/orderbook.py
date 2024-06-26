import websocket
import requests
import threading
import json

REST_URL = "https://fapi.binance.com/fapi/v1/depth?symbol={}&limit=1000"
WEBSOCKET_URL = "wss://fstream.binance.com/ws/{}@depth@100ms"

class Orderbook:
    def __init__(self, symbol: str):
        self._socket = WEBSOCKET_URL.format(symbol)
        self._rest = REST_URL.format(symbol)
        self._ws = websocket.WebSocketApp(self._socket, on_message=self.on_message, on_close=self.on_close)
        self._bids = {}
        self._asks = {}
        self._last_update_id = 0
        self._prev_u = None
        self._lock = False

    def _get_snapshot(self):
        """Сбросьте значения _bids и _asks на моментальный снимок текущей книги заказов и обновите last_update_id."""
        r = requests.get(self._rest)
        self._lock = True
        data = json.loads(r.text)
        
        self._last_update_id = data["lastUpdateId"]

        self._bids = {float(price): float(qty) for price, qty in data["bids"]}
        self._asks = {float(price): float(qty) for price, qty in data["asks"]}
        self._lock = False
        print('Получили снепшот')

    def on_close(self, ws):
        print("Сессия закрыта")

    def on_message(self, ws, message_str):
        while self._lock:
            pass
        # print('Вебсокеты из ордербук')
        message = json.loads(message_str)
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
    
    def get_bids(self) -> dict:
        """Return bids"""
        return self._bids
    
    def get_asks(self) -> dict:
        """Return asks"""
        return self._asks