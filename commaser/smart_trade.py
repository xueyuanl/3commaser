from .threecommas import threec


# include spot trade and future trade


def get_smart_trade():
    return threec.smart_trade_get()


def create_smart_trade(account_id, pair, total, open_price, leverage, **kwargs):
    position_units = total / open_price

    data = {
        'account_id': account_id,  # 31012823
        'pair': pair,
        'leverage': {
            'enabled': True,
            'type': kwargs['leverage_type'],
            'value': leverage
        },
        'position': {
            'type': kwargs['position_type'],
            'order_type': kwargs['order_type'],
            'units': {
                'value': position_units
            },
            'price': {
                'value': open_price
            }
        },
        'take_profit': {
            'enabled': False
        },
        'stop_loss': {
            'enabled': False
        }
    }
    if 'take_profit' in kwargs:
        data['take_profit'] = kwargs['take_profit']
    if 'stop_loss' in kwargs:
        data['stop_loss'] = kwargs['stop_loss']

    res = threec.smart_trade_create(**data)
    return res
