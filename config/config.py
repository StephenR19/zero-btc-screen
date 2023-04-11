import configparser
import os

__all__ = ('config', 'Config')


class Config:
    def __init__(self, file_name=os.path.join(os.path.dirname(__file__), os.pardir, 'configuration.cfg')):
        self._conf = self._load_screens(file_name)

    @property
    def console_logs(self):
        return self._conf.getboolean('base', 'console_logs', fallback=False)

    @property
    def logs_file(self):
        return self._conf.get('base', 'logs_file', fallback=None)

    @property
    def dummy_data(self):
        return self._conf.getboolean('base', 'dummy_data', fallback=False)

    @property
    def screens(self):
        screens = self._conf.get('base', 'screens', fallback='').strip('[]\n').split('\n')
        screens_conf = {}
        for screen in screens:
            screens_conf[screen] = dict(self._conf.items(screen))
        return screens_conf

    @property
    def refresh_interval(self):
        return self._conf.getint('base', 'refresh_interval_seconds', fallback=15)

    @property
    def currency(self):
        currencies = self._conf.get('base', 'currency', fallback='BTC,ETH,ADA,DOT,ATOM,SOL,XCH,LINK,MATIC,AVAX,QNT,ADS,DAG,DIMO,HNT,AAVE,LTX')
        return currencies.split(',')


    @property
    def currency_id(self):
        currency_ids = self._conf.get('base', 'currency_id', fallback='bitcoin,ethereum,cardano,polkadot,cosmos,solana,chia,chainlink,matic-network,avalanche-2,quant-network,alkimi,constellation-labs,dimo,helium,lattice-token')
        return currency_ids.split(',')

    @property
    def vs_currency(self):
        return self._conf.get('base', 'vs_currency', fallback='usd')

    @property
    def graph_days(self):
        return self._conf.get('base', 'graph_days', fallback='1')          

    @staticmethod
    def _load_screens(file_name):
        conf = configparser.ConfigParser()
        conf.read_file(open(file_name))
        return conf


# we want to import the config across the files
config = Config()
