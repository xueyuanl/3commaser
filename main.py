import os

from api import ThreeCommas

key = os.getenv('API_KEY')
secret = os.getenv('SECRET')

threec = ThreeCommas(key, secret)


def main():
    eth = threec.start_new_deal(bot_id=6405856, pair='USDT_ETH')
    btc = threec.start_new_deal(bot_id=6405856, pair='USDT_BTC')


if __name__ == '__main__':
    main()
