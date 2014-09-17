import argumentParser

import proxyServer


__author__ = "Joseph W Becher"
__copyright__ = "Copyright 2014, Joseph W Becher"
__credits__ = [""]
__license__ = "GPL"
__version__ = "0.5"
__email__ = "jwbecher@gmail.com"
__status__ = "Development"

parser = argumentParser.ArgumentParser()

parser.add_argument("--username", help="Bitcoin RPC username", required=True, nargs=1, action="store")
parser.add_argument("--password", help="Bitcoin RPC password", required=True, nargs=1, action="store")
parser.add_argument("--port", help="Bitcoin RPC port (8332)", default=8332, action="store_true")
parser.add_argument("--webport", help="Proxy web port (8330)", default=8330, action="store_true")

args = parser.parse_args()

bitcoinrpc_port = args.port
bitcoinrpc_webport = args.webport
bitcoinrpc_username = args.username[0]
bitcoinrpc_password = args.password[0]

proxyServer.proxyserver(bitcoinrpc_webport, bitcoinrpc_port, bitcoinrpc_username, bitcoinrpc_password)