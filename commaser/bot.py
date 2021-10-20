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
    def __init__(self, account, coin, quote, level, Preset):
        self.name = '{}_{} {} {} AUTO'.format(coin, quote, level, Preset.__name__)
        self.account = account
        self.coin = coin
        self.quote = quote
        self.Preset = Preset
