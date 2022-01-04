import argparse
import json

from commaser.Preset import Strategy
from commaser.account import Account, get_account_id
from commaser.bot import BotSpec, update_bots, disable_bots, edit_bot
from log import logger_
from constants import DEFAULT_STRATEGY
from commaser.threecommas import threec

def check_key(key, map_, value):
    if key not in map_:
        map_[key] = value


def get_args():
    parser = argparse.ArgumentParser(description='3commas bot configuration')
    parser.add_argument('-s', '--strategy', dest='strategy', action='store_true',
                        help='update strategy')
    args = parser.parse_args()
    return args


def main():
    # t = threec.bot_info(bot_id=6805525)
    args = get_args()
    with open('bot_strategies.json') as f:
        strategies = json.load(f)

    with open('config.json') as f:
        data = json.load(f)

    if args.strategy:
        # update strategy
        for exchange_name, e in data.items():
            for g in e['groups']:
                strategy = g.get('strategy', DEFAULT_STRATEGY)
                logger_.info('update strategy {} for group {}'.format(strategy, g['name']))
                for bot in g['bots']:
                    s = Strategy(strategy, **strategies[strategy])
                    bot_spec = BotSpec(bot['coin'], g['quote'], g['name'], s, id_=bot['id'])
                    edit_bot(bot_spec)
                    bot['name'] = bot_spec.name
        with open('config.json', 'w') as f:  # write back config anyway
            json.dump(data, f, indent=2)
        return

    try:
        for exchange_name, e in data.items():
            id_ = e.get('id', get_account_id(exchange_name))
            for g in e['groups']:
                quote = g.get('quote', 'USD')
                check_key('bots', g, [])
                group_bot_list = g['bots']
                target_number = g.get('pair_number', 1)
                g['coins'] = sorted(list(set(g['coins'])))  # dedup and sort
                for coin in g['coins']:
                    exchange = Account(exchange_name, id_)
                    preset = g.get('strategy', DEFAULT_STRATEGY)
                    s = Strategy(preset, **strategies[preset])
                    bot_spec = BotSpec(coin, quote, g['name'], s, account=exchange)
                    current_bot_list = [b for b in group_bot_list if b['coin'] == coin]
                    new_bots = update_bots(target_number, current_bot_list, bot_spec)
                    group_bot_list.extend(new_bots)

        # disable bots for deleted pairs
        disable_bots(data)
    except Exception as e:
        print(e.with_traceback())

    finally:
        with open('config.json', 'w') as f:  # write back config anyway
            json.dump(data, f, indent=2)


if __name__ == '__main__':
    main()
