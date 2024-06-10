import argparse
import numpy as np
from threading import Event, Thread
from time import sleep

from model.orderbook import Orderbook


class Stakan:
    def __init__(self):
  
        self.bid_x = []
        self.bid_z = []
        self.ask_x = []
        self.ask_z = []
        self.y = [[0] * 100]
        # print(self.orderbook)

        

    def set_depth(self,orderbook):
        bid_data = orderbook.get_bids()
        bid_prices = sorted(bid_data.keys())[-100:]
        bid_quantities = [bid_data[price] for price in bid_prices]
        bid_depth = []
        cumulative_volume = 0
        for qty in bid_quantities[::-1]:
            cumulative_volume += qty
            bid_depth.append(cumulative_volume)
        bid_depth = bid_depth[::-1]
        ask_data = orderbook.get_asks()
        ask_prices = sorted(ask_data.keys())[:100]
        ask_quantities = [ask_data[price] for price in ask_prices]
        ask_depth = []
        cumulative_volume = 0
        for qty in ask_quantities:
            cumulative_volume += qty
            ask_depth.append(cumulative_volume)
        self.bid_x.append(bid_prices)
        self.bid_z.append(bid_depth)
        self.ask_x.append(ask_prices)
        self.ask_z.append(ask_depth)
        print(f'{self.bid_x[0][-1]} | {self.bid_z[0][-1]}')
        self.y.append([self.y[-1][0] + 100] * 100)
        if len(self.y) > 10:
            del self.bid_x[0]
            del self.bid_z[0]
            del self.ask_x[0]
            del self.ask_z[0]
            del self.y[0]
        # print(self.orderbook)
            
    def call_repeatedly(self,func):
        stopped = Event()
        def loop():
            while not stopped.wait(1): # the first call is in `interval` secs
                func()
        Thread(target=loop).start()    
        return stopped.set
    
orderbook = Orderbook('BTCUSDT')
orderbook.connect()
stakan_1 = Stakan()

# cancel_future_calls = stakan_1.call_repeatedly(stakan_1.set_depth)
stakan_1.set_depth(orderbook)
sleep(0.1)
stakan_1.set_depth(orderbook)
sleep(0.1)
stakan_1.set_depth(orderbook)
sleep(0.1)
stakan_1.set_depth(orderbook)
sleep(0.1)
stakan_1.set_depth(orderbook)
sleep(0.1)
stakan_1.set_depth(orderbook)
sleep(0.1)
stakan_1.set_depth(orderbook)
sleep(0.1)
