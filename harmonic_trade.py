from futures.constant import GARTLEY, BAT, BUTTERFLY, SHARK, CRAB
from futures.harmonic import Gartley, Bat, Butterfly, Shark, Crab

harmonics = {
    GARTLEY: Gartley,
    BAT: Bat,
    BUTTERFLY: Butterfly,
    SHARK: Shark,
    CRAB: Crab
}


def main():
    harmonic = BUTTERFLY
    x = 41815
    a = 49108
    c = None
    base = 'BTC'
    # ------
    quote = 'USD'
    invest = 100
    leverage = 10
    account = 'FTX-perp (Futures)'
    if harmonic == 'shark':
        harmonic_obj = harmonics[harmonic](x, a, c)
    else:
        harmonic_obj = harmonics[harmonic](x, a)
    res = harmonic_obj.create_trade(account, base, quote, invest, leverage)
    print('result is {}'.format(res.ok))


if __name__ == '__main__':
    main()
