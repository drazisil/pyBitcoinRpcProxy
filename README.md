pyBitcoinRpcProxy
=================

A small python script to serv as a CORS proxy between Bitcon's RPC server and the web.

I created this because I didn't want to have to worry about node.js or another web server when testing/developing on my local machine.

Not working yet, but I wanted to toss it up anyway.

usage: pyBitcoinRpcProxy.py [-h] --username USERNAME --password PASSWORD
                            [--port] [--webport]

optional arguments:
  -h, --help           show this help message and exit
  --username USERNAME  Bitcoin RPC username
  --password PASSWORD  Bitcoin RPC password
  --port               Bitcoin RPC port (8332)
  --webport            Proxy web port (8330)
