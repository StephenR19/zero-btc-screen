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
    def coins(self):
        coins_list = self._conf.get('base', 'coins', fallback='bitcoin:BTC,ethereum:ETH,cardano:ADA,polkadot:DOT,cosmos:ATOM,solana:SOL,chia:XCH,chainlink:LINK,matic-network:MATIC,avalanche-2:AVAX,quant-network:QNT,alkimi:ADS,constellation-labs:DAG,dimo:DIMO,helium:HNT,aave:AAVE,lattice-token:LTX,curve-dao-token:CRV,enjincoin:ENJ,uniswap:UNI,the-graph:GRT,zelcash:FLUX,fantom:FTM,thorchain:RUNE,the-sandbox:SAND,arweave:AR,axelar:AXL,livepeer:LPT,mapmetrics:MMAPS,algorand:ALGO,planetwatch:PLANETS,rss3:RSS3,siaprime-coin:SCP,banano:BAN,derace:DERC')
        return coins_list.split(',')

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
