from .threecommas import threec


class Account(object):
    def __init__(self, name, id_):
        self.name = name
        self.id_ = id_


def get_account_id(name):
    accounts = threec.accounts_list().data
    for a in accounts:
        if a['name'] == name:
            return a['id']
    raise Exception('Cannot found account {}'.format(name))
