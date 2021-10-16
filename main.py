import os

from commasapi.api import ThreeCommas
from config import *
from log import logger_

key = os.getenv('API_KEY')
secret = os.getenv('SECRET')

threec = ThreeCommas(key, secret)


def main():
    # for each bot
    for bot_id in BOT_LIST:
        # get bot info
        res = threec.bot_info(bot_id=bot_id)
        bot_info = res.payload

        logger_.info('start config bot: {}, id: {}'.format(bot_info['name'], str(bot_id)))
        active_deals = bot_info['active_deals']
        active_pairs = [a['pair'] for a in active_deals]
        logger_.info('get active pair list: {}'.format(active_pairs))

        pairs = bot_info['pairs']
        logger_.info('get pair list: {}'.format(pairs))

        for p in pairs:
            if p in active_pairs:
                logger_.info('pair {} is still in deal, skip'.format(p))
                continue
            logger_.info('start pair {}'.format(p))
            res = threec.start_new_deal(bot_id=bot_id, pair=p)
            if res.ok:
                logger_.info('started a new deal for {}'.format(p))
            elif res.status_code == 422:  # Maximum active deals reached
                logger_.info('Pair {}: {}'.format(p, res.error))
            else:
                logger_.info('error code {}, error message: {}'.format(res.status_code, res.error))


if __name__ == '__main__':
    main()
