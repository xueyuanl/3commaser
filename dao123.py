import argparse

from constants import *
from futures.dao import Dao


def get_args():
    parser = argparse.ArgumentParser(description='3commas bot configuration')
    parser.add_argument('-p', '--price', dest='price', required=True, action='store', type=float, help='open point')
    parser.add_argument('-s', '--stop', dest='stop', required=True, action='store', type=float, help='stop loss point')
    parser.add_argument('--limit', dest='limit', action='store', type=float, help='condition limit order')

    parser.add_argument('-b', '--base', dest='base', required=True, action='store', type=str, help='coin name')
    parser.add_argument('-q', '--quote', dest='quote', action='store', type=str, nargs='?',
                        default='USD', help='USDT or USD')

    parser.add_argument('-i', '--invest', dest='invest', action='store', type=int, nargs='?', default=50,
                        help='number of invest')
    parser.add_argument('-l', '--leverage', dest='leverage', action='store', type=int, nargs='?', default=20,
                        help='leverage')
    parser.add_argument('--account', dest='account', action='store', type=str, nargs='?',
                        default=FTX_FUTURE, help='account name')
    parser.add_argument('-r', '--risk', dest='risk', action='store', type=float, help='max loss money')

    args = parser.parse_args()
    return args


def main():
    args = get_args()
    price = args.price
    stop = args.stop

    base = args.base
    # ------
    quote = args.quote
    invest = args.invest
    leverage = args.leverage
    account_name = args.account

    dao = Dao(price, stop)
    if args.risk:
        invest = args.risk / dao.get_lost_percentage() / leverage

    print('------')
    print(f'Trade pair is {args.base}/{args.quote}.')
    print(f'Price at {args.price}, stop loss at {args.stop}.')
    print(f'Total invest {round(invest, 2)} at leverage {args.leverage}')
    max_loss = args.risk if args.risk else invest * leverage * dao.get_lost_percentage()
    print(f'Max loss: {round(max_loss, 2)} USD at {dao.get_lost_percentage() * 100}%.')
    print(f'Opening position on account {args.account}')
    print('------')

    res = dao.create_trade(account_name, base, quote, invest, leverage)
    print('result: {}'.format(res.ok))


if __name__ == '__main__':
    main()
