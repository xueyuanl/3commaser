from commaser.account import get_account_entity
from commaser.smart_trade import create_smart_trade
from log import logger_
from .constants import *

volume_scheme = {TP_SCHEME403030: [40, 30, 30],
                 TP_SCHEME10204020: [10, 40, 30, 20]}


def _three_target_profit_scheme(a, d):
    tp_one = d - (d - a) * F382
    tp_two = d - (d - a) * F5
    tp_three = d - (d - a) * F618

    vs = volume_scheme[TP_SCHEME403030]
    return [(tp_one, vs[0]), (tp_two, vs[1]), (tp_three, vs[2])]


def _four_target_profit_scheme(a, d):
    tp_one = d - (d - a) * F146
    tp_two = d - (d - a) * F382
    tp_three = d - (d - a) * F5
    tp_four = d - (d - a) * F618

    vs = volume_scheme[TP_SCHEME10204020]
    return [(tp_one, vs[0]), (tp_two, vs[1]), (tp_three, vs[2]), (tp_four, vs[3])]


class Gartley(object):
    def __init__(self, x, a):
        d = a - (a - x) * F786  # XA 0.786 Retracement
        self.open_point = d
        self.stop_loss = x
        self.tp_scheme = _four_target_profit_scheme(a, d)
        self.position_type = POSITION_BUY if d > x else POSITION_SELL
        self.print_status()

    def print_status(self):
        logger_.info('|------')
        logger_.info('|{} pattern position type: {}, open point {}.'.format(
            self.__class__.__name__, self.position_type, self.open_point))
        scheme = ''
        for s in self.tp_scheme:
            scheme += '{}/{}%, '.format(round(s[0], 2), s[1])
        scheme = scheme[:-2]
        logger_.info('|Target profit scheme: {}.'.format(scheme))
        loss_percent = round(self.get_lost_percentage() * 100, 2)
        logger_.info('|Stop loss {}, percentage {}%.'.format(self.stop_loss, loss_percent))
        logger_.info('|------')

    def get_lost_percentage(self):
        return round(abs((self.open_point - self.stop_loss) / self.open_point), 4)

    def create_trade(self, account_name, base, quote, invest, leverage, note=None):
        account = get_account_entity(account_name)
        account_id = account.id_
        params = {
            'position_type': self.position_type,
            'order_type': ORDER_LIMIT,
        }

        if account.is_binance():
            pair = quote + '_' + base + quote
        elif account.is_ftx():
            pair = quote + '_' + base + '-' + 'PERP'

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
        if note:
            params['note'] = note
        total = invest * leverage
        res = create_smart_trade(account_id, pair, total, self.open_point, leverage, **params)
        return res


class Bat(Gartley):
    def __init__(self, x, a):
        d = a - (a - x) * F886
        self.open_point = d
        self.stop_loss = x
        self.tp_scheme = _four_target_profit_scheme(a, d)
        self.position_type = POSITION_BUY if d > x else POSITION_SELL
        self.print_status()


class Butterfly(Gartley):
    def __init__(self, x, a):
        d = a - (a - x) * F1272
        self.open_point = d
        self.stop_loss = a - (a - x) * F1414
        self.tp_scheme = _four_target_profit_scheme(a, d)
        self.position_type = POSITION_BUY if x > d else POSITION_SELL
        self.print_status()


class Shark886(Gartley):
    def __init__(self, x, a, c):  # shark use c point to decide target profits
        d = a - (a - x) * F886
        self.open_point = d
        self.stop_loss = x
        self.tp_scheme = _four_target_profit_scheme(c, d)
        self.position_type = POSITION_BUY if d > x else POSITION_SELL
        self.print_status()


class Shark113(Gartley):
    def __init__(self, x, a, c):  # shark use c point to decide target profits
        d = a - (a - x) * F1130
        self.open_point = d
        self.stop_loss = a - (a - x) * F1272
        self.tp_scheme = _four_target_profit_scheme(c, d)
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
