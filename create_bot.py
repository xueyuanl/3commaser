import os

from commasapi.api import ThreeCommas

key = os.getenv('API_KEY')
secret = os.getenv('SECRET')

threec = ThreeCommas(key, secret)


def main():
    bot_id = 6368568
    threec.bot_disable(bot_id=bot_id)


if __name__ == '__main__':
    main()
