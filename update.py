import json
import os

from commasapi.api import ThreeCommas
from commaser.Preset import presets
from commaser.account import Account
from commaser.bot import BotSpec, Bot
from log import logger_

key = os.getenv('API_KEY')
secret = os.getenv('SECRET')

threec = ThreeCommas(key, secret)


def create_bot(spec):
    account = spec.account
    coin = spec.coin
    quote = spec.quote
    Preset = spec.Preset
    pair = quote + '_' + coin
    data = {'name': spec.name,
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


def update_bots(coin, bot_spec):
    target_number = coin['number']
    enabled_bot_list = []
    disabled_bot_list = []
    if 'bots' not in coin:
        coin['bots'] = []
    for b in coin['bots']:
        if b['stats'] == Bot.DISABLED:
            disabled_bot_list.append(b)
        elif b['stats'] == Bot.ENABLED:
            enabled_bot_list.append(b)

    enabled_bot_number = len(enabled_bot_list)
    disabled_bot_number = len(disabled_bot_list)

    if target_number < enabled_bot_number:  # we need to disable some bots
        number = enabled_bot_number - target_number
        logger_.info('disable bots for {}'.format(coin['name']))
        for i in range(0, number):
            threec.bot_disable(bot_id=enabled_bot_list[i]['id'])
            logger_.info('disable bot {}, id: {}'.format(enabled_bot_list[i]['name'], enabled_bot_list[i]['id']))
            enabled_bot_list[i]['stats'] = Bot.DISABLED
    elif enabled_bot_number < target_number <= enabled_bot_number + disabled_bot_number:
        # change some disabled bots to enable
        number = target_number - enabled_bot_number
        logger_.info('enable part of bots for {}'.format(coin['name']))
        for i in range(0, number):
            threec.bot_enable(bot_id=disabled_bot_list[i]['id'])
            logger_.info('enable bot {}, id: {}'.format(disabled_bot_list[i]['name'], disabled_bot_list[i]['id']))
            disabled_bot_list[i]['stats'] = Bot.ENABLED
    elif target_number > enabled_bot_number + disabled_bot_number:
        # enable some disabled bots and add some new bots
        logger_.info('first enable all the disabled bots for {}'.format(coin['name']))
        for i in range(0, disabled_bot_number):
            threec.bot_enable(bot_id=disabled_bot_list[i]['id'])
            logger_.info('enable bot {}, id: {}'.format(disabled_bot_list[i]['name'], disabled_bot_list[i]['id']))
            disabled_bot_list[i]['stats'] = Bot.ENABLED

        open_bot_number = target_number - enabled_bot_number - disabled_bot_number
        for i in range(0, open_bot_number):
            res = create_bot(bot_spec)  # create
            threec.bot_enable(bot_id=res.data['id'])  # enable
            bot = {'name': res.data['name'], 'id': res.data['id'], "stats": Bot.ENABLED}
            logger_.info('open bot {}, id: {}'.format(bot['name'], bot['id']))
            coin['bots'].append(bot)


def main():
    # res = threec.accounts_list()

    with open('config.json') as f:
        data = json.load(f)

    for k, v in data.items():
        for e in v['exchanges']:
            id_ = e['id']
            exchange_name = e['name']
            quote = e['quote']
            for coin in e['coins']:
                coin_name = coin['name']
                exchange = Account(exchange_name, id_)
                bot_spec = BotSpec(exchange, coin_name, quote, v['coin_level'], presets[v['name']])
                update_bots(coin, bot_spec)

    with open('config.json', 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    main()
