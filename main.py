import os

from commasapi.api import ThreeCommas
from config import *
from log import logger_

key = os.getenv('API_KEY')
secret = os.getenv('SECRET')

threec = ThreeCommas(key, secret)


def main():
    # get bot info
    bot_info = threec.bot_info(bot_id=BOT_ID)
    active_deals = bot_info.payload['active_deals']
    active_pairs = [a['pair'] for a in active_deals]
    logger_.info('get active pair list: {}'.format(active_pairs))

    pairs = []
    for b in BASE:
        pairs.append(QUOTE + '_' + b)
    logger_.info('get pair list: {}'.format(pairs))

    for p in pairs:
        if p in active_pairs:
            logger_.info('pair {} is still in deal, skip'.format(p))
            continue
        logger_.info('start pair {}'.format(p))
        res = threec.start_new_deal(bot_id=BOT_ID, pair=p)
        if res.ok:
            logger_.info('started a new deal for {}'.format(p))
        elif res.status_code == 422:  # Maximum active deals reached
            logger_.info('Pair {}: {}'.format(p, res.error))
        else:
            logger_.info('error code {}, error message: {}'.format(res.status_code, res.error))


if __name__ == '__main__':
    main()
