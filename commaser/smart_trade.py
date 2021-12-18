from .exchange import Exchange
from .threecommas import threec


# include spot trade and future trade


def get_smart_trade():
    return threec.smart_trade_get()


def create_smart_trade(exchange, account_id, base, quote, total, price, leverage):
    if exchange == Exchange.BINANCE:
        pair_str = quote + '_' + base + quote
        leverage_type = 'isolated'
    elif exchange == Exchange.FTX:
        pair_str = quote + '_' + base + '-' + 'PERP'
        leverage_type = 'cross'

    position_units = total / price

    data = {
        'account_id': account_id,  # 31012823
        'pair': pair_str,
        'leverage': {
            'enabled': True,
            'type': leverage_type,
            'value': leverage
        },
        'position': {
            'type': 'buy',
            'order_type': 'limit',
            'units': {
                'value': position_units
            },
            'price': {
                'value': price
            }

        },
        'take_profit': {
            'enabled': False
        },
        'stop_loss': {
            'enabled': False
        }
    }
    res = threec.smart_trade_create(**data)
    return res
