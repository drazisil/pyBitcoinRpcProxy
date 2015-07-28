import ConfigParser
import argparse
from modules.util.fakesechead import FakeSecHead

__author__ = 'drazisil'

class Config:

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('path', metavar='path', help='specify a configuration file')
        parser.add_argument('--webport', dest='web_port', help='Proxy web port (8330)', default=8330)
        args = parser.parse_args()

        config = ConfigParser.SafeConfigParser()
        config.readfp(FakeSecHead(open(args.path)))

        self.host = 'http://127.0.0.1:8332'
        self.username = config.get('asection', 'rpcuser')
        self.password = config.get('asection', 'rpcpassword')
        self.web_port = args.web_port


