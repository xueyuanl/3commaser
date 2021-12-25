import argparse

from futures.constant import GARTLEY, BAT, BUTTERFLY, SHARK, CRAB
from futures.harmonic import Gartley, Bat, Butterfly, Shark, Crab

harmonics = {
    GARTLEY: Gartley,
    BAT: Bat,
    BUTTERFLY: Butterfly,
    SHARK: Shark,
    CRAB: Crab
}


def get_args():
    parser = argparse.ArgumentParser(description='3commas bot configuration')
    parser.add_argument('--harmonic', dest='harmonic', action='store', type=str, nargs='?', default=BAT, help='shape')
    parser.add_argument('-x', dest='x', required=True, action='store', type=float, help='X point')
    parser.add_argument('-a', dest='a', required=True, action='store', type=float, help='A point')
    parser.add_argument('-c', dest='c', action='store', type=float, help='A point')

    parser.add_argument('-b', '--base', dest='base', required=True, action='store', type=str, help='coin name')
    parser.add_argument('-q', '--quote', dest='quote', action='store', type=str, nargs='?',
                        default='USDT', help='USDT or USD')

    parser.add_argument('-i', '--invest', dest='invest', action='store', type=int, nargs='?', default=100,
                        help='number of invest')
    parser.add_argument('-l', '--leverage', dest='leverage', action='store', type=int, nargs='?', default=10,
                        help='leverage')
    parser.add_argument('--account', dest='account', action='store', type=str, nargs='?',
                        default='Binance Futures USDT-M', help='account name')

    args = parser.parse_args()
    if args.harmonic == SHARK and not args.c:
        parser.error('-c requires, Shark harmonic need C point value')
    return args


def main():
    args = get_args()
    print('------')
    print(f'Harmonic pattern is {args.harmonic}.')
    if args.harmonic == SHARK:
        print(f'X point {args.x}, A point {args.a}, C point {args.c}')
    else:
        print(f'X point {args.x}, A point {args.a}.')
    print(f'Trade pair is {args.base}/{args.quote}.')
    print(f'Total invest {args.invest} at leverage {args.leverage}')
    print(f'Opening position on account {args.account}')
    print('------')
    
    harmonic = args.harmonic
    x = args.x
    a = args.a
    c = args.c
    base = args.base
    # ------
    quote = args.quote
    invest = args.invest
    leverage = args.leverage
    account_name = args.account  # 'FTX-perp (Futures)'

    if harmonic == SHARK:
        if not c:
            raise Exception('need value on c')
        harmonic_obj = harmonics[harmonic](x, a, c)
    else:
        harmonic_obj = harmonics[harmonic](x, a)
    res = harmonic_obj.create_trade(account_name, base, quote, invest, leverage)
    print('result: {}'.format(res.ok))


if __name__ == '__main__':
    main()
