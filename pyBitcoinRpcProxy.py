from modules.config import Config

import proxyServer


__author__ = "Joseph W Becher"
__copyright__ = "Copyright 2014, Joseph W Becher"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0"
__email__ = "jwbecher@gmail.com"
__status__ = "Development"

config = Config()

bitcoinrpc_port = '8332'
bitcoinrpc_webport = config.web_port
bitcoinrpc_username = config.username
bitcoinrpc_password = config.password

proxyServer.proxyserver(bitcoinrpc_webport, bitcoinrpc_port, bitcoinrpc_username, bitcoinrpc_password)