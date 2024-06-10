
import websocket
import requests
import threading
import json



REST_URL = "https://fapi.binance.com/fapi/v1/depth?symbol={}&limit=1000"
WEBSOCKET_URL = "wss://fstream.binance.com/ws/{}@depth@100ms"
symbol = 'DOGEUSDT'

def on_close(self, ws):
        print("Session closed.")

def on_message(self, ws, message_str):
    while _lock:
        pass
    message = json.loads(message_str)
    print(message)
    if message["u"] >= _last_update_id:
        #Циклически просматривайте уровни цен и количества для проведения торгов и запросов и обновляйте количество
        for price_level, qty in message["b"]:
            if float(qty) == 0:
                _bids.pop(float(price_level), None)
            else:
                _bids[float(price_level)] = float(qty)
        for price_level, qty in message["a"]:
            if float(qty) == 0:
                _asks.pop(float(price_level), None)
            else:
                _asks[float(price_level)] = float(qty)
    if _prev_u != None and _prev_u != message["pu"]:
        print("Orderbook out of sync, grabbing new snapshot")
        _get_snapshot()
    _prev_u = message["u"]

# Получили стакан
def _get_snapshot():
    """Сбросьте _bids и _asks на моментальный снимок текущей книги заказов и обновите last_update_id."""
    r = requests.get(_rest)
    _lock = True
    data = json.loads(r.text)
    print('Загрузили стакан')
    _last_update_id = data["lastUpdateId"]
    _bids = {float(price): float(qty) for price, qty in data["bids"]}
    _asks = {float(price): float(qty) for price, qty in data["asks"]}
    _lock = False
    print(_bids)

# экземпляр сокетов
_socket = WEBSOCKET_URL.format(symbol)
_rest = REST_URL.format(symbol)
_ws = websocket.WebSocketApp(_socket, on_message=on_message, on_close=on_close)
_bids = {}
_asks = {}
_last_update_id = 0
_prev_u = None
_lock = False
print('Инициализация')

print('Коннект')
wst = threading.Thread(target=_ws.run_forever)
wst.daemon = True
wst.start()
_get_snapshot()











