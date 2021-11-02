import os

from commasapi.api import ThreeCommas
from constants import *
from log import logger_

key = os.getenv('API_KEY')
secret = os.getenv('SECRET')

threec = ThreeCommas(key, secret)


def is_bot_available(bot_info):
    return bot_info['is_enabled'] and bot_info['active_deals_count'] < bot_info['max_active_deals']


def open_deals_number(pair, active_pairs, deals_number):
    pair_number = 0
    for a in active_pairs:
        if a == pair:
            pair_number += 1
    return deals_number - pair_number


def main():
    # for each bot
    for bot_id in BOT_LIST:
        # get bot info
        bot_info = threec.bot_info(bot_id=bot_id).data
        logger_.info('get bot: {}, id: {}'.format(bot_info['name'], str(bot_id)))

        if not is_bot_available(bot_info):
            logger_.info('bot {} is not available, id: {}'.format(bot_info['name'], str(bot_id)))
            continue

        active_deals = bot_info['active_deals']
        active_pairs = [a['pair'] for a in active_deals]
        logger_.info('get active pair list: {}'.format(active_pairs))

        pairs = bot_info['pairs']
        logger_.info('get pair list: {}'.format(pairs))
        for p in pairs:
            number = open_deals_number(p, active_pairs, bot_info['allowed_deals_on_same_pair'])
            if number <= 0:
                logger_.info('pair {} is still in deals, skip'.format(p))
                continue
            logger_.info('number of deal can be opened is {} for pair {}'.format(number, p))
            while number > 0:
                logger_.info('start add deal for pair {}'.format(p))
                res = threec.start_new_deal(bot_id=bot_id, pair=p)
                if res.ok:
                    logger_.info('started a new deal for {}'.format(p))
                elif res.status_code == 422:  # Maximum active deals reached
                    logger_.info('Pair {}: {}'.format(p, res.error))
                else:
                    logger_.info('error code {}, error message: {}'.format(res.status_code, res.error))
                number -= 1


if __name__ == '__main__':
    main()
