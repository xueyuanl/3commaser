import os
from log import logger_
from commasapi.api import ThreeCommas

key = os.getenv('API_KEY')
secret = os.getenv('SECRET')

if not key:
    logger_.error('Need env value API_KEY')
    raise Exception('Need env value API_KEY')
if not secret:
    logger_.error('Need env value SECRET')
    raise Exception('Need env value SECRET')

threec = ThreeCommas(key, secret)
