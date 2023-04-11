import json
import random
import time
from datetime import datetime, timezone, timedelta
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config.builder import Builder
from config.config import config
from logs import logger
from presentation.observer import Observable
from data.shareddata import SELECTED_COIN

DATA_SLICE_DAYS = 1
DATETIME_FORMAT = "%Y-%m-%dT%H:%M"


def get_dummy_data():
    logger.info('Generating dummy data')



def fetch_prices():
    logger.info('Fetching prices')
    url = f'https://api.coingecko.com/api/v3/coins/{config.currency_id[SELECTED_COIN]}/ohlc?vs_currency={config.vs_currency[SELECTED_COIN]}&days={config.graph_days}'
    print(url)
    req = Request(url)
    data = urlopen(req).read()
    external_data = json.loads(data)
    prices = [entry[1:] for entry in external_data[:]]
    print(prices)
    return prices


def main():
    logger.info('Initialize')
    global SELECTED_COIN
    data_sink = Observable()
    builder = Builder(config)
    builder.bind(data_sink)

    try:
        while True:
            try:
                currency_length = len(config.currency_id)
                prices = [entry[1:] for entry in get_dummy_data()] if config.dummy_data else fetch_prices()
                if (currency_length > SELECTED_COIN):
                    SELECTED_COIN += 1
                else:
                    SELECTED_COIN = 0
                data_sink.update_observers(prices)
                time.sleep(config.refresh_interval)
            except (HTTPError, URLError) as e:
                logger.error(str(e))
                time.sleep(5)
    except IOError as e:
        logger.error(str(e))
    except KeyboardInterrupt:
        logger.info('Exit')
        data_sink.close()
        exit()


if __name__ == "__main__":
    main()
