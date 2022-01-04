import argparse

from constants import *
from futures.constants import GARTLEY, BAT, BUTTERFLY, SHARK, CRAB, SHARK113
from futures.harmonic import Gartley, Bat, Butterfly, Shark113, Crab, Shark886

harmonics = {
    GARTLEY: Gartley,
    BAT: Bat,
    BUTTERFLY: Butterfly,
    SHARK: Shark886,
    SHARK113: Shark113,
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
                        default='USD', help='USDT or USD')

    parser.add_argument('-i', '--invest', dest='invest', action='store', type=int, nargs='?', default=50,
                        help='number of invest')
    parser.add_argument('-l', '--leverage', dest='leverage', action='store', type=int, nargs='?', default=20,
                        help='leverage')
    parser.add_argument('--account', dest='account', action='store', type=str, nargs='?',
                        default=FTX_FUTURE, help='account name')
    parser.add_argument('-r', '--risk', dest='risk', action='store', type=float, help='max loss money')
    parser.add_argument('-n', '--note', dest='note', action='store', type=str, help='note message')

    args = parser.parse_args()
    if args.harmonic == SHARK and not args.c:
        parser.error('-c requires, Shark harmonic need C point value')
    return args


def main():
    args = get_args()

    harmonic = args.harmonic
    x = args.x
    a = args.a
    c = args.c
    base = args.base
    # ------
    quote = args.quote
    invest = args.invest
    leverage = args.leverage
    account_name = args.account

    if harmonic == SHARK or harmonic == SHARK113:
        if not c:
            raise Exception('need value on c')
        harmonic_obj = harmonics[harmonic](x, a, c)
    else:
        harmonic_obj = harmonics[harmonic](x, a)
    if args.risk:
        invest = args.risk / harmonic_obj.get_lost_percentage() / leverage

    print('------')
    print(f'Harmonic pattern: {args.harmonic}.')
    if args.harmonic == SHARK:
        print(f'X point {args.x}, A point {args.a}, C point {args.c}')
    else:
        print(f'X point {args.x}, A point {args.a}.')
    print(f'Trade pair: {args.base}/{args.quote}.')
    print(f'Total invest {round(invest, 2)} at leverage {args.leverage}')
    max_loss = args.risk if args.risk else invest * leverage * harmonic_obj.get_lost_percentage()
    print(f'Max loss: {round(max_loss, 2)} USD at {round(harmonic_obj.get_lost_percentage() * 100, 2)}%.')
    print(f'Opening position on account {args.account}')
    print('------')
    note = args.note if args.note else args.harmonic + ', risk ' + str(round(max_loss, 2))
    res = harmonic_obj.create_trade(account_name, base, quote, invest, leverage, note=note)
    print('result: {}'.format(res.ok))


if __name__ == '__main__':
    main()
