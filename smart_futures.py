from commaser.exchange import Exchange
from commaser.smart_trade import create_smart_trade


def main():
    exchange = Exchange.BINANCE
    account_id = 31012823
    res = create_smart_trade(exchange, account_id, 'BTC', 'USDT', 100, 2000, 10)

    print(res)


if __name__ == '__main__':
    main()
