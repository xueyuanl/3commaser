from commaser.account import get_account_entity
from commaser.smart_trade import create_smart_trade
from .constants import *


class Dao(object):
    def __init__(self, o, s, limit=None):
        self.open_point = o
        self.position_type = POSITION_BUY if o > s else POSITION_SELL
        self.stop_loss = s

    def get_lost_percentage(self):
        return round(abs((self.open_point - self.stop_loss) / self.open_point), 4)

    def create_trade(self, account_name, base, quote, invest, leverage):
        # all is conditional orders
        account = get_account_entity(account_name)
        account_id = account.id_
        params = {
            'position_type': self.position_type,
            'order_type': ORDER_CONDITIONAL
        }

        if account.is_binance():
            pair = quote + '_' + base + quote
            params['leverage_type'] = 'isolated'
        elif account.is_ftx():
            pair = quote + '_' + base + '-' + 'PERP'
            params['leverage_type'] = 'cross'

        params['stop_loss'] = {
            'enabled': 'true',
            'order_type': ORDER_MARKET,
            'conditional': {
                'price': {
                    'value': self.stop_loss,
                    'type': 'bid'
                }
            }
        }
        total = invest * leverage
        res = create_smart_trade(account_id, pair, total, self.open_point, leverage, **params)
        return res
