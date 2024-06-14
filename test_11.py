import time

from binance import ThreadedWebsocketManager

api_key = 'QIT80MTFskjHSr82dtsteA6bG01CUeODQCg65KoYaQ5LmPcSpYDzyv1Oa7fugW3m'
api_secret = 'uMLo0WdaCv5FHBauV8QI4LZoDgmmVFf5Jd8TboKYRxHnHx6pmNrhg5bmdBgO54xI'

def main():

    # symbol = 'BNBBTC'

    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        # print(f"message type: {msg['e']}")
        print(msg)

    # twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

    # # multiple sockets can be started
    # twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

    # или можно запустить мультиплексный сокет следующим образом
    # названия потоков приведены в документации Binance
    streams = ['btcusdt@depth@100ms', 'notusdt@depth@100ms']
    twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)
    twm.join()


if __name__ == "__main__":
   main()