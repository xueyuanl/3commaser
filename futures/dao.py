from commaser.account import get_account_entity
from commaser.smart_trade import create_smart_trade
from log import logger_
from .constants import *


def _default_target_profit_scheme(o, s):
    # if o > s:  # long position
    #     tp_one = o + (o - s)
    # else:
    #     tp_one = o - (s - o)
    tp_one = 2 * o - 1 * s
    tp_two = 3 * o - 2 * s
    tp_three = 4 * o - 3 * s
    tp_four = 4.5 * o - 3.5 * s
    tp_five = 5 * o - 4 * s

    return [(tp_one, 5), (tp_two, 15), (tp_three, 55), (tp_four, 15), (tp_five, 10)]


class Dao(object):
    def __init__(self, o, s, limit=None):
        self.open_point = o
        self.position_type = POSITION_BUY if o > s else POSITION_SELL
        self.stop_loss = s
        self.tp_scheme = _default_target_profit_scheme(o, s)
        self.print_status()

    def print_status(self):
        logger_.info('|------')
        logger_.info('|Dao123 position type: {}, open point {}.'.format(self.position_type, round(self.open_point, 2)))
        scheme = ''
        for s in self.tp_scheme:
            scheme += '{}/{}%, '.format(round(s[0], 2), s[1])
        scheme = scheme[:-2]
        logger_.info('|Target profit scheme: {}.'.format(scheme))
        loss_percent = round(self.get_lost_percentage() * 100, 2)
        logger_.info('|Stop loss {}, percentage {}%.'.format(round(self.stop_loss, 2), loss_percent))
        logger_.info('|------')

    def get_lost_percentage(self):
        return round(abs((self.open_point - self.stop_loss) / self.open_point), 4)

    def create_trade(self, account_name, base, quote, invest, leverage, **kwargs):
        # all is conditional-market orders
        account = get_account_entity(account_name)
        account_id = account.id_
        params = {
            'position_type': self.position_type,
            'order_type': ORDER_LIMIT if kwargs.get('limit') else ORDER_CONDITIONAL
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
        if kwargs.get('note'):
            params['note'] = kwargs.get('note')
        total = invest * leverage
        res = create_smart_trade(account_id, pair, total, self.open_point, leverage, **params)
        return res

    def cal_ttp_deviation(self):
        """
        calculate trailing take profit deviation
        :return:
        """
        pass
