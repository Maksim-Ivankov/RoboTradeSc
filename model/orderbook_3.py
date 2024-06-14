# import websockets
import json
# import asyncio
import requests
import time
# import threading
import multiprocessing as mp
from binance import ThreadedWebsocketManager

class Orderbook:
    def __init__(self, symbol):
        self.symbol = symbol
        self.api_key = 'QIT80MTFskjHSr82dtsteA6bG01CUeODQCg65KoYaQ5LmPcSpYDzyv1Oa7fugW3m'
        self.api_secret = 'uMLo0WdaCv5FHBauV8QI4LZoDgmmVFf5Jd8TboKYRxHnHx6pmNrhg5bmdBgO54xI'
        # формируем ссылку для бодключения к вебсокетам 
        self.socet_symbol = []
        for sym in symbol:
            self.socet_symbol.append(f'{sym.lower()}@depth@100ms')

        self._bids = {}
        self._asks = {}
        self._last_update_id = 0
        # self._prev_u = None
        self._lock = False
        self.bid_x = []
        self.bid_z = []
        self.ask_x = []
        self.ask_z = []
        self.y = [[0] * 100]
        self.data_socket = {}
        print('Создали экземпляр ордрбук версия 3')

    def _get_snapshot(self):
        """Сбросьте значения _bids и _asks на моментальный снимок текущей книги заказов и обновите last_update_id."""
        for sym in self.symbol:
            rest = f"https://fapi.binance.com/fapi/v1/depth?symbol={sym.lower()}&limit=1000"
            self._get_once_snapshot(rest,sym)
            print(f'Получили снепшот {sym}')
            time.sleep(0.5)

    def _get_once_snapshot(self,_rest,sym):
        r = requests.get(_rest)
        self._lock = True
        data = json.loads(r.text)
        self._last_update_id = data["lastUpdateId"]
        _bids = {float(price): float(qty) for price, qty in data["bids"]}
        _asks = {float(price): float(qty) for price, qty in data["asks"]}
        self.data_socket[sym] = [_bids,_asks,self._last_update_id,None]
        self._lock = False
        return _bids, _asks


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
    def websocket_trade(self):
        twm = ThreadedWebsocketManager(api_key=self.api_key, api_secret=self.api_secret)




        # try:
        #     with websockets.connect(self._socket) as ws:
        #         print('Подключились к вебсокетам')
        #         while True:        
        #             try:
        #                 message = json.loads(ws.recv())['data']
        #                 # print(message)
        #                 for sym in self.symbol:
        #                     # print('1111')
        #                     if message['s'] == sym:
        #                         # print('22222')
        #                         if message["u"] >= self.data_socket[sym][2]:
        #                             # print('3333')
        #                             for price_level, qty in message["b"]:
        #                                 if float(qty) == 0:
        #                                     self.data_socket[sym][0].pop(float(price_level), None)
        #                                     # print('5')
        #                                 else:
        #                                     self.data_socket[sym][0][float(price_level)] = float(qty)
        #                                     # print('6')
        #                                 # print(self.data_socket[sym][0][-1])
        #                             for price_level, qty in message["a"]:
        #                                 if float(qty) == 0:
        #                                     self.data_socket[sym][1].pop(float(price_level), None)
        #                                     # print('7')
        #                                 else:
        #                                     self.data_socket[sym][1][float(price_level)] = float(qty)
        #                                     # print('8')
        #                             # print('44444')
        #                         if self.data_socket[sym][3] != None and self.data_socket[sym][3] != message["pu"]:
        #                             print("Рассинхронизация книги заказов приводит к появлению нового снимка")
        #                             self._get_snapshot()
        #                         self.data_socket[sym][3] = message["u"]
        #                     else:
        #                         continue

        #             except websockets.exceptions.ConnectionClosed:
        #                 print('Вебсокеты обосались и закрылись')
        #                 break
        # except Exception as e:
        #     print(f'Ошибка - {e}')



    def connect(self):
        print('Стартовали поток с вебсокетами')
        self._get_snapshot()
        self.running = True
        p = mp.Process(target=self.websocket_trade)
        p.start()
        # self.myThread = threading.Thread(target=self.websocket_trade(), args=(), daemon=True)
        # self.myThread.start()
        # asyncio.run(self.websocket_trade())