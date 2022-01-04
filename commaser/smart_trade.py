from log import logger_
from .constants import *
from .threecommas import threec


# include spot trade and future trade


def get_smart_trade():
    return threec.smart_trade_get()


def create_smart_trade(account_id, pair, total, price, leverage, **kwargs):
    position_units = total / price

    data = {
        'account_id': account_id,  # 31012823
        'pair': pair,
        'leverage': {
            'enabled': True,
            'type': kwargs.get('leverage_type', 'cross'),
            'value': leverage
        },
        'position': {
            'type': kwargs['position_type'],
            'order_type': kwargs['order_type'],
            'units': {
                'value': position_units
            }
        },
        'take_profit': {
            'enabled': False
        },
        'stop_loss': {
            'enabled': False
        }
    }
    if kwargs['order_type'] == ORDER_LIMIT:
        data['position']['price'] = {
            'value': price
        }
    elif kwargs['order_type'] == ORDER_CONDITIONAL:
        if 'cond_type' in kwargs and kwargs['cond_type'] == COND_LIMIT:
            data['position']['price'] = {
                'value': price
            }
            data['position']['conditional'] = {
                'price': {
                    'value': kwargs['cond_limit_price']
                },
                'order_type': COND_LIMIT
            }
        else:
            data['position']['conditional'] = {
                'price': {
                    'value': price
                },
                'order_type': COND_MARKET
            }

    if 'take_profit' in kwargs:
        data['take_profit'] = kwargs['take_profit']
    if 'stop_loss' in kwargs:
        data['stop_loss'] = kwargs['stop_loss']

    if 'note' in kwargs:
        data['note'] = kwargs['note']

    logger_.debug('smart trade params: {}'.format(data))
    res = threec.smart_trade_create(**data)
    return res
