from commaser.account import get_account_id
from commaser.exchange import Exchange
from commaser.smart_trade import create_smart_trade
from .constant import *


class Bat(object):
    def __init__(self, x, a):
        d = a - (a - x) * F886
        self.open_point = d
        self.stop_loss = x
        self.tp_one = d - (d - a) * F382
        self.tp_two = d - (d - a) * F5
        self.tp_three = d - (d - a) * F618
        self.position_type = POSITION_BUY if d > x else POSITION_SELL
        print(
            'Bat pattern position type is {}, open point {}, stop loss point {}, tp one {}, top two {}, tp three {}.'.format(
                self.position_type, self.open_point, self.stop_loss, self.tp_one, self.tp_two, self.tp_three))

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
            'steps': [
                {
                    'order_type': ORDER_LIMIT,
                    'price': {
                        'value': self.tp_one,
                        'type': 'bid'
                    },
                    'volume': 30
                },
                {
                    'order_type': ORDER_LIMIT,
                    'price': {
                        'value': self.tp_two,
                        'type': 'bid'
                    },
                    'volume': 40
                },
                {
                    'order_type': ORDER_LIMIT,
                    'price': {
                        'value': self.tp_three,
                        'type': 'bid'
                    },
                    'volume': 30
                },
            ]
        }
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
