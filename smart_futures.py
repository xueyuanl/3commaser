from futures.harmonic import Bat


def main():
    x = 48413
    a = 49241
    base = 'BTC'
    # ------
    quote = 'USD'
    invest = 100
    leverage = 10
    bat = Bat(x, a)
    account = 'FTX-perp (Futures)'
    res = bat.create_trade(account, base, quote, invest, leverage)

    print(res)


if __name__ == '__main__':
    main()
