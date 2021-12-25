from .threecommas import threec


class Account(object):
    def __init__(self, name, id_):
        self.name = name
        self.id_ = id_
        self.exchange_name = None

    def is_ftx(self):
        return 'FTX' in self.exchange_name or 'ftx' in self.exchange_name or 'Ftx' in self.exchange_name

    def is_binance(self):
        return 'Binance' in self.exchange_name


def get_account_id(name):
    accounts = threec.accounts_list().data
    for a in accounts:
        if a['name'] == name:
            return a['id']
    raise Exception('Cannot found account {}'.format(name))


def get_account_entity(name):
    accounts = threec.accounts_list().data
    for a in accounts:
        if a['name'] == name:
            account = Account(a['name'], a['id'])
            account.exchange_name = a['exchange_name']
            return account
    raise Exception('Cannot found account {}'.format(name))
