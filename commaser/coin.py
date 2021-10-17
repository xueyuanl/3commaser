class Coin(object):
    def __init__(self, name):
        self.name = name
        self.kind = ''  # main, alts, salts


class Pair(object):
    def __init__(self):
        self.base = ''  # SOL
        self.quote = ''  # USDT

