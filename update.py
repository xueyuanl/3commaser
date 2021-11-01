import json

from commaser.Preset import presets, TAS2
from commaser.account import Account, get_account_id
from commaser.bot import BotSpec, update_bots, disable_bots


def check_key(key, map_, value):
    if key not in map_:
        map_[key] = value


def main():
    with open('config.json') as f:
        data = json.load(f)
    try:
        for exchange_name, e in data.items():
            id_ = e.get('id', get_account_id(exchange_name))
            for g in e['groups']:
                quote = g.get('quote', 'USD')
                check_key('bots', g, [])
                group_bot_list = g['bots']
                target_number = g.get('pair_number', 1)
                for coin in g['coins']:
                    exchange = Account(exchange_name, id_)
                    preset = g.get('preset', TAS2.__name__)
                    bot_spec = BotSpec(exchange, coin, quote, g['name'], presets[preset])
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
