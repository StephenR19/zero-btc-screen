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

DATA_SLICE_DAYS = 1
DATETIME_FORMAT = "%Y-%m-%dT%H:%M"
selected_coin = 0


def get_dummy_data():
    logger.info('Generating dummy data')



def fetch_prices():
    logger.info('Fetching prices')
    url = f'https://api.coingecko.com/api/v3/coins/{config.currency_id[selected_coin]}/ohlc?vs_currency={config.vs_currency}&days={config.graph_days}'
    req = Request(url)
    data = urlopen(req).read()
    external_data = json.loads(data)
    prices = [entry[1:] for entry in external_data[:]]
    return prices


def main():
    global selected_coin
    logger.info('Initialize')
    data_sink = Observable()
    builder = Builder(config)
    builder.bind(data_sink)

    try:
        while True:
            try:
                prices = [entry[1:] for entry in get_dummy_data()] if config.dummy_data else fetch_prices()
                data_sink.update_observers(prices)
                if (len(config.currency_id)-1 > selected_coin):
                    selected_coin += 1
                else:
                    selected_coin = 0
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
