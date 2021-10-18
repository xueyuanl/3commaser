from enum import Enum


class Coin(Enum):
    BTC = 'BTC'


class Pair(object):
    def __init__(self, base, quote):
        self.base = ''  # SOL
        self.quote = ''  # USDT


class Quote(Enum):
    USDT = 'USDT'
