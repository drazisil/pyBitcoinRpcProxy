pyBitcoinRpcProxy
=================

A small python script to serve as a CORS proxy between Bitcon's RPC server and the web.

I created this because I didn't want to have to worry about node.js or another web server when testing/developing on my local machine.

Username and password are not actually optional, they just display that way for some reason.

    usage: pyBitcoinRpcProxy.py [-h] [--webport WEB_PORT] path

    positional arguments:
      path                specify a configuration file

    optional arguments:
      -h, --help          show this help message and exit
      --webport WEB_PORT  Proxy web port (8330)


