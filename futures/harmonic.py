from commaser.account import get_account_id
from commaser.exchange import Exchange
from commaser.smart_trade import create_smart_trade
from .constant import *

volume_scheme = {'v304030': [30, 40, 30]}


def _three_target_profit_scheme(a, d):
    tp_one = d - (d - a) * F382
    tp_two = d - (d - a) * F5
    tp_three = d - (d - a) * F618

    vs = volume_scheme['v304030']
    return [(tp_one, vs[0]), (tp_two, vs[1]), (tp_three, vs[2])]


class Gartley(object):
    def __init__(self, x, a):
        d = a - (a - x) * F786  # XA 0.786 Retracement
        self.open_point = d
        self.stop_loss = x
        self.tp_scheme = _three_target_profit_scheme(a, d)
        self.position_type = POSITION_BUY if d > x else POSITION_SELL
        self.print_status()

    def print_status(self):
        print('{} pattern position type is {}, open point {}, stop loss point {}.'.format(
            self.__class__.__name__, self.position_type, self.open_point, self.stop_loss))
        print('{} pattern target profit scheme is {}'.format(self.__class__.__name__, self.tp_scheme))

    def create_trade(self, account, base, quote, invest, leverage, **kwargs):
        exchange = kwargs.get('exchange', Exchange.FTX)

        account_id = get_account_id(account)
        params = {
            'position_type': self.position_type,
            'order_type': ORDER_LIMIT
        }

        if exchange == Exchange.BINANCE:
            pair = quote + '_' + base + quote
            params['leverage_type'] = 'isolated'
        elif exchange == Exchange.FTX:
            pair = quote + '_' + base + '-' + 'PERP'
            params['leverage_type'] = 'cross'

        params['take_profit'] = {
            'enabled': 'true',
            'steps': []
        }
        for tp in self.tp_scheme:
            step = {
                'order_type': ORDER_LIMIT,
                'price': {
                    'value': tp[0],
                    'type': 'bid'
                },
                'volume': tp[1]
            }
            params['take_profit']['steps'].append(step)

        params['stop_loss'] = {
            'enabled': 'true',
            'order_type': ORDER_MARKET,
            'breakeven': 'true',
            'conditional': {
                'price': {
                    'value': self.stop_loss,
                    'type': 'bid'
                }
            }
        }
        res = create_smart_trade(account_id, pair, invest, self.open_point, leverage, **params)
        return res


class Bat(Gartley):
    def __init__(self, x, a):
        d = a - (a - x) * F886
        self.open_point = d
        self.stop_loss = x
        self.tp_scheme = _three_target_profit_scheme(a, d)
        self.position_type = POSITION_BUY if d > x else POSITION_SELL
        self.print_status()


class Butterfly(Gartley):
    def __init__(self, x, a):
        d = a - (a - x) * F1272
        self.open_point = d
        self.stop_loss = a - (a - x) * F1414
        self.tp_scheme = _three_target_profit_scheme(a, d)
        self.position_type = POSITION_BUY if x > d else POSITION_SELL
        self.print_status()


class Shark(Gartley):
    def __init__(self, x, a, c):  # shark use c point to decide target profits
        d = a - (a - x) * F1130
        self.open_point = d
        self.stop_loss = a - (a - x) * F1272
        self.tp_scheme = _three_target_profit_scheme(c, d)
        self.position_type = POSITION_BUY if x > d else POSITION_SELL
        self.print_status()


class Crab(Gartley):
    def __init__(self, x, a):
        d = a - (a - x) * F1618
        self.open_point = d
        self.stop_loss = a - (a - x) * F2000
        self.tp_scheme = _three_target_profit_scheme(a, d)
        self.position_type = POSITION_BUY if x > d else POSITION_SELL
        self.print_status()
