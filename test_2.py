
import flet as ft
from websockets import connect
import aiofiles
import json
import asyncio
import httpx
from datetime import datetime

from decimal import Decimal
import pandas as pd
import requests
import math
import time







# Книга заказов
def update_orderbook(agg_level,quantity_precession,price_precession,symbol,n_intervals):
    levels_to_show = 10 # сколько строк отображать
    url = f'https://api.binance.com/api/v3/depth' # адрес для получения книги заказов вначале
    params = {
        'symbol':symbol.upper(),
        'limit': n_intervals,
    }
    data = requests.get(url,params).json()
    bid_df = pd.DataFrame(data['bids'],columns=['price','quantity'],dtype=float)
    bid_df = aggregate_levels(bid_df, agg_level=Decimal(agg_level), side='bid')
    bid_df = bid_df.sort_values('price',ascending=False) # Сортировка
    bid_df = bid_df.iloc[:levels_to_show] # обрезаем список настолько, насколько хотим через переменную

    ask_df = pd.DataFrame(data['asks'],columns=['price','quantity'],dtype=float)
    ask_df = aggregate_levels(ask_df, agg_level=Decimal(agg_level), side='ask')
    ask_df = ask_df.sort_values('price',ascending=False) # Сортировка
    ask_df = ask_df.iloc[-levels_to_show:] # обрезаем список настолько, насколько хотим через переменную

    mid_price = (bid_df.price.iloc[0] + ask_df.price.iloc[-1])/2 # спред - цена посередине
    # mid_price = f'%.{price_precession}f'%mid_price

    # bid_df.quantity = bid_df.quantity.apply(lambda x: f'%.{quantity_precession}f'%x)
    # ask_df.quantity = ask_df.quantity.apply(lambda x: f'%.{quantity_precession}f'%x)

    # bid_df.price = bid_df.price.apply(lambda x: f'%.{price_precession}f'%x)
    # ask_df.price = ask_df.price.apply(lambda x: f'%.{price_precession}f'%x)

    return bid_df.to_dict('records'),ask_df.to_dict('records'),mid_price # возвращаем список словарей






async def main(page: ft.Page):


        # Книга заказов
    async def update_orderbook(agg_level,quantity_precession,price_precession,symbol,n_intervals):
        levels_to_show = 10 # сколько строк отображать
        websocket_url = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@depth' # адрес для вебсокетов - обновление стакана
        async with connect(websocket_url) as ws:
            while True:
                data = json.loads(await ws.recv()) 
                bid_df = pd.DataFrame(data['b'],columns=['price','quantity'],dtype=float)
                bid_df = aggregate_levels(bid_df, agg_level=Decimal(agg_level), side='bid')
                bid_df = bid_df.sort_values('price',ascending=False) # Сортировка
                bid_df = bid_df.iloc[:levels_to_show] # обрезаем список настолько, насколько хотим через переменную

                ask_df = pd.DataFrame(data['a'],columns=['price','quantity'],dtype=float)
                ask_df = aggregate_levels(ask_df, agg_level=Decimal(agg_level), side='ask')
                ask_df = ask_df.sort_values('price',ascending=False) # Сортировка
                ask_df = ask_df.iloc[-levels_to_show:] # обрезаем список настолько, насколько хотим через переменную

                mid_price = (bid_df.price.iloc[0] + ask_df.price.iloc[-1])/2 # спред - цена посередине
                # mid_price = f'%.{price_precession}f'%mid_price

                # bid_df.quantity = bid_df.quantity.apply(lambda x: f'%.{quantity_precession}f'%x)
                # ask_df.quantity = ask_df.quantity.apply(lambda x: f'%.{quantity_precession}f'%x)

                # bid_df.price = bid_df.price.apply(lambda x: f'%.{price_precession}f'%x)
                # ask_df.price = ask_df.price.apply(lambda x: f'%.{price_precession}f'%x)

                print(bid_df.to_dict('records'))

                # return bid_df.to_dict('records'),ask_df.to_dict('records'),mid_price # возвращаем список словарей

    def aggregate_levels(levels_df, agg_level = Decimal('0.1'), side = 'bid'):
        if side == 'bid': # определяем вхождение цены влево или вправо
            right = False
            label_func = lambda X: X.left
        elif side == 'ask':
            right = True
            label_func = lambda X: X.right
        min_level = math.floor(Decimal(min(levels_df.price))/agg_level-1)*agg_level # округляет минимальное значение до ближайшего кратного
        max_level = math.ceil(Decimal(max(levels_df.price))/agg_level+1)*agg_level # округляет максимальное значение до ближайшего кратного

        level_bounds = [float(min_level + agg_level*X) for X in range(int((max_level-min_level)/agg_level) + 1)] # список цен с шагом

        levels_df['bin'] = pd.cut(levels_df.price,bins = level_bounds,precision=10,right=right)
        levels_df = levels_df.groupby('bin').agg(quantity = ('quantity','sum')).reset_index()
        levels_df['price'] = levels_df.bin.apply(label_func)
        levels_df = levels_df[levels_df.quantity>0] # убрать строки, где нулевой обём
        levels_df = levels_df[['price','quantity']]
        return levels_df

    async def dowload_websoket_book(symbol):
        websocket_url = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@depth' # адрес для вебсокетов - обновление стакана
        async with connect(websocket_url) as ws:
            while True:
                data = json.loads(await ws.recv()) 
                print(data['b'][0][0])
                text.value = str(data['b'][0][0])
                await page.update_async()



    # page.window_center()
    page.theme_mode='light'
    page.horizontal_alignment = 'center'
    page.window_width = 200
    page.window_height = 200
    text = ft.Text('ЛОЛО')    
    # asyncio.run(orferbook_download('BTCUSDT'))
    await page.add_async(text)
    # await dowload_websoket_book('BTCUSDT')
    await update_orderbook('0.0001','0.0001','0.0001','DOGEUSDT',100)

    # await update_main()
ft.app(target=main)
































































