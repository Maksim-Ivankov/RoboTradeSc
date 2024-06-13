import argparse
from threading import Event, Thread
from time import sleep

from model.orderbook_2 import Orderbook

symbol = "btcusdt"

#Проверьте, был ли указан символ в качестве аргумента, в противном случае по умолчанию используется значение DEFAULT_SYMBOLh

orderbook = Orderbook(symbol)
orderbook.connect()



bid_x = []
bid_z = []
ask_x = []
ask_z = []
y = [[0] * 100]

def set_depth():
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

    bid_x.append(bid_prices)
    bid_z.append(bid_depth)
    ask_x.append(ask_prices)
    ask_z.append(ask_depth)

    # print(f'{bid_x[0][-1]} | {bid_z[0][-1]}')
    y.append([y[-1][0] + 100] * 100)

    if len(y) > 10:
        del bid_x[0]
        del bid_z[0]
        del ask_x[0]
        del ask_z[0]
        del y[0]


def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()    
    return stopped.set

cancel_future_calls = call_repeatedly(0.1, set_depth)


# set_depth()
# sleep(0.1)
