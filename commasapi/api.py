import hashlib
import hmac
import json

from requests import Session

from log import logger_
from .config import *


class Response(object):
    """wrap response"""

    def __init__(self, resp):
        self.data = json.loads(resp.text)
        self.ok = resp.ok
        if not self.ok:
            self.error = self.data['error']
        self.status_code = resp.status_code
        self.elapsed = resp.elapsed


class ThreeCommas(object):
    """3commas Wrapper Class"""

    def __init__(self, key, secret, **kwargs):
        self._logger = kwargs.get('logger', logger_)
        self._session = Session()
        self.base_url = BASE_URL
        self.key = key
        self.secret = secret

    def _get(self, path_, **kwargs):

        new_path = self._make_path(path_, **kwargs)
        signature = self._generate_signature(new_path)
        headers = {
            'APIKEY': self.key,
            'Signature': signature
        }
        self._session.headers.update(headers)
        url = '{}{}'.format(self.base_url, new_path)
        self._logger.info('calling GET api: {}'.format(url))
        try:
            response = self._session.get(url)
            rep = Response(response)
            if not rep.ok:
                logger_.error(rep.data)
                raise
            return rep
        except Exception as e:
            raise e

    def _post(self, path_, **kwargs):
        signature = self._generate_signature(path_, data=json.dumps(kwargs))
        headers = {
            'APIKEY': self.key,
            'Signature': signature
        }
        self._session.headers.update(headers)
        url = '{}{}'.format(self.base_url, path_)
        self._logger.info('calling POST api: {}'.format(url))
        try:
            response = self._session.post(url, json=kwargs)
            rep = Response(response)
            if not rep.ok:
                logger_.error(rep.data)
                raise Exception(rep.data)
            return rep
        except Exception as e:
            raise e

    def _patch(self, path_, **kwargs):
        signature = self._generate_signature(path_, data=json.dumps(kwargs))
        headers = {
            'APIKEY': self.key,
            'Signature': signature
        }
        self._session.headers.update(headers)
        url = '{}{}'.format(self.base_url, path_)
        self._logger.info('calling POST api: {}'.format(url))
        try:
            response = self._session.patch(url, json=kwargs)
            rep = Response(response)
            if not rep.ok:
                logger_.error(rep.data)
                raise
            return rep
        except Exception as e:
            raise e

    def _make_path(self, path_, **kwargs):
        params = ''
        if kwargs:
            for k in kwargs:
                params += k + '=' + str(kwargs[k]) + '&'
            params = params[:-1]
            path_ = path_ + f"?{params}"
        return path_

    def _generate_signature(self, path, data=''):
        """
        Generates the signature needed for 3commas API communication
        path: /public/api/ver1/accounts
        data: payload
        """
        encoded_key = str.encode(self.secret)
        message = str.encode(path + data)
        signature = hmac.new(encoded_key, message, hashlib.sha256).hexdigest()
        return signature

    def accounts_list(self, **kwargs):
        return self._get(PUBLIC_API + V1 + ACCOUNTS, **kwargs)

    def bots_list(self, **kwargs):
        return self._get(PUBLIC_API + V1 + BOTS, **kwargs)

    def start_new_deal(self, **kwargs):
        endpoint = BOT_START_NEW_DEAL.replace('{bot_id}', str(kwargs['bot_id']))
        return self._post(PUBLIC_API + V1 + endpoint, **kwargs)

    def deals_stats(self, **kwargs):
        endpoint = BOT_DEALS_STATS.replace('{bot_id}', str(kwargs['bot_id']))
        return self._get(PUBLIC_API + V1 + endpoint, **kwargs)

    def bot_create(self, **kwargs):
        return self._post(PUBLIC_API + V1 + BOT_CREATE, **kwargs)

    def bot_edit(self, **kwargs):
        endpoint = BOT_EDIT.replace('{bot_id}', str(kwargs['bot_id']))
        return self._patch(PUBLIC_API + V1 + endpoint, **kwargs)

    def bot_info(self, **kwargs):
        endpoint = BOT_INFO.replace('{bot_id}', str(kwargs['bot_id']))
        return self._get(PUBLIC_API + V1 + endpoint, **kwargs)

    def bot_enable(self, **kwargs):
        endpoint = BOT_ENABLE.replace('{bot_id}', str(kwargs['bot_id']))
        return self._post(PUBLIC_API + V1 + endpoint, **kwargs)

    def bot_disable(self, **kwargs):
        endpoint = BOT_DISABLE.replace('{bot_id}', str(kwargs['bot_id']))
        return self._post(PUBLIC_API + V1 + endpoint, **kwargs)

    def bot_delete(self, **kwargs):
        endpoint = BOT_DELETE.replace('{bot_id}', str(kwargs['bot_id']))
        return self._post(PUBLIC_API + V1 + endpoint, **kwargs)

    def smart_trade_get(self, **kwargs):
        return self._get(PUBLIC_API + V2 + SMART_TRADE, **kwargs)

    def smart_trade_create(self, **kwargs):
        return self._post(PUBLIC_API + V2 + SMART_TRADE, **kwargs)
