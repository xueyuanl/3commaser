from log import logger_
from .threecommas import threec


class Bot(object):
    ENABLED = 'enabled'
    DISABLED = 'disabled'

    def __init__(self):
        self.id
        self.account_id
        self.is_enabled

        self.deletable
        self.trailing_enabled
        self.name

        # self.preset = Preset()

        self.tags = []


class BotSpec(object):
    def __init__(self, coin, quote, group_name, strategy, account=None, id_=None):
        self.name = '{}/{} {} {} AUTO'.format(coin, quote, group_name, strategy.code)
        self.coin = coin
        self.quote = quote
        self.strategy = strategy
        self.account = account
        self.id = id_


def update_bots(target_number, bot_list, bot_spec):
    # open existing bots anyway
    for b in bot_list:
        res = threec.bot_enable(bot_id=b['id'])
        logger_.info('open bot {}, id: {}'.format(b['name'], b['id']))
        b['state'] = Bot.ENABLED

    # open additional bots
    open_bot_number = target_number - len(bot_list)
    new_added_bots = []
    for i in range(0, open_bot_number):
        res = create_bot(bot_spec)  # create
        threec.bot_enable(bot_id=res.data['id'])  # enable
        bot = {'coin': bot_spec.coin, 'name': res.data['name'], 'id': res.data['id'], 'state': Bot.ENABLED}
        logger_.info('create bot {}, id: {}'.format(bot['name'], bot['id']))
        new_added_bots.append(bot)
    return new_added_bots


def create_bot(spec):
    account = spec.account
    coin = spec.coin
    quote = spec.quote
    strategy = spec.strategy
    pair = quote + '_' + coin
    data = {'name': spec.name,
            'account_id': account.id_,
            'pairs': [pair],  # USDT_BTC
            'base_order_volume': strategy.base_order_volume,  # 10
            'take_profit': strategy.take_profit,  # 1.25
            'safety_order_volume': strategy.safety_order_volume,  # 20
            'martingale_volume_coefficient': strategy.martingale_volume_coefficient,  # 1.05
            'martingale_step_coefficient': strategy.martingale_step_coefficient,  # 1
            'max_safety_orders': strategy.max_safety_orders,  # 25
            'active_safety_orders_count': strategy.active_safety_orders_count,  # 1
            'safety_order_step_percentage': strategy.safety_order_step_percentage,  # 2.4
            'take_profit_type': strategy.take_profit_type,  # total
            'strategy_list': strategy.strategy_list  # [{"strategy": "nonstop"}]
            }
    logger_.info('create bot data info: {}'.format(data))
    res = threec.bot_create(**data)
    if res.ok:
        logger_.info('successfully create bot {}, id: {}'.format(res.data['name'], res.data['id']))
    else:
        logger_.error('fail to create bot for account {}, account id: {}'.format(account.name, account.id_))
    return res


def edit_bot(spec):
    coin = spec.coin
    if not spec.id:
        logger_.error('need bot id to edit')
        raise Exception('no id found')
    bot_id = spec.id
    quote = spec.quote
    strategy = spec.strategy
    pair = quote + '_' + coin
    data = {'name': spec.name,
            'bot_id': bot_id,
            'pairs': [pair],  # USDT_BTC
            'base_order_volume': strategy.base_order_volume,  # 10
            'take_profit': strategy.take_profit,  # 1.25
            'safety_order_volume': strategy.safety_order_volume,  # 20
            'martingale_volume_coefficient': strategy.martingale_volume_coefficient,  # 1.05
            'martingale_step_coefficient': strategy.martingale_step_coefficient,  # 1
            'max_safety_orders': strategy.max_safety_orders,  # 25
            'active_safety_orders_count': strategy.active_safety_orders_count,  # 1
            'safety_order_step_percentage': strategy.safety_order_step_percentage,  # 2.4
            'take_profit_type': strategy.take_profit_type,  # total
            'strategy_list': strategy.strategy_list  # [{"strategy": "nonstop"}]
            }
    logger_.info('create bot data info: {}'.format(data))
    res = threec.bot_edit(**data)
    if res.ok:
        logger_.info('successfully update bot {}, id: {}'.format(res.data['name'], res.data['id']))
    else:
        logger_.error('fail to update bot {}, id: {}'.format(res.data['name'], res.data['id']))
    return res


def disable_bots(data):
    logger_.info('start to disable bots for deleted pairs')
    for exchange_name, e in data.items():
        for g in e['groups']:
            for b in g['bots']:
                coin_name = b['coin']
                if coin_name not in g['coins']:
                    # disable all bots anyway
                    res = threec.bot_disable(bot_id=b['id'])
                    if res.status_code == 404:  # bot might be delete manually
                        logger_.error('can not find bot {}, id: {}'.format(b['name'], b['id']))
                        continue
                    logger_.info('disabled bot {}, id: {}'.format(b['name'], b['id']))
                    b['state'] = Bot.DISABLED


def clean_bots():
    # delete deletable bots
    pass


def sync_bot_settings():
    # update preset, name
    pass
