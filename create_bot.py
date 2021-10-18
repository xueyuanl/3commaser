import os

from commasapi.api import ThreeCommas
from commaser.Preset import TAS1
from commaser.account import Account
from commaser.coin import Coin, Quote
from log import logger_

key = os.getenv('API_KEY')
secret = os.getenv('SECRET')

threec = ThreeCommas(key, secret)


def create_bot(account, coin, quote, Preset):
    pair = quote.name + '_' + coin.name
    data = {'name': '{}_{} {} AUTO'.format(coin.name, quote.name, Preset.__name__),
            'account_id': account.id_,
            'pairs': [pair],  # USDT_BTC
            'base_order_volume': Preset.base_order_volume,  # 10
            'take_profit': Preset.take_profit,  # 1.25
            'safety_order_volume': Preset.safety_order_volume,  # 20
            'martingale_volume_coefficient': Preset.martingale_volume_coefficient,  # 1.05
            'martingale_step_coefficient': Preset.martingale_step_coefficient,  # 1
            'max_safety_orders': Preset.max_safety_orders,  # 25
            'active_safety_orders_count': Preset.active_safety_orders_count,  # 1
            'safety_order_step_percentage': Preset.safety_order_step_percentage,  # 2.4
            'take_profit_type': Preset.take_profit_type,  # total
            'strategy_list': Preset.strategy_list  # [{"strategy": "nonstop"}]
            }
    logger_.info('create bot data info: {}'.format(data))
    res = threec.bot_create(**data)
    if res.ok:
        logger_.info('successfully create bot {}, id: {}'.format(res.data['name'], res.data['id']))
    else:
        logger_.error('fail to create bot for account {}, account id: {}'.format(account.name, account.id_))
    return res


def main():
    # res = threec.accounts_list()

    paper_account = Account('paper', 31028998)
    res = create_bot(paper_account, Coin.BTC, Quote.USDT, TAS1)
    # threec.bot_enable(bot_id=res.data['id'])
    print(res)


if __name__ == '__main__':
    main()
