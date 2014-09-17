import base64
import time
import socket  # Import socket module
from email.parser import Parser

import argumentParser


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

# This is the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object

host = 'localhost'  # Get local machine name
port = bitcoinrpc_webport  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port
print('Running server on ', host, ' on port ', port)

while True:
    s.listen(5)  # Now wait for client connection.
    serversocket, addr = s.accept()  # Establish connection with client.

    data = serversocket.recv(1024)  # receive data from client
    string = bytes.decode(data)  # decode it to string

    try:
        request_method = string.split(' ')[0]
        # TODO: extract the request body
        headerlines = string.split("\r\n")
        del headerlines[0]
        headers = Parser().parsestr("\r\n".join(headerlines))
        # print('Header count:', len(headers))
        print('All Headers:', headers.keys())
        clientorigin = headers['Origin']

    except IndexError:
        # TODO: check if this is a Keep-Alive behavior
        # close the connection
        serversocket.close()
        exit()

    print('Got connection from', clientorigin)

    # determine request method  (HEAD and GET are supported)
    print("Method: ", request_method)
    print("Request body: ", string)

    # Create a TCP/IP socket
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', bitcoinrpc_port)
    print('connecting to ', server_address[0], 'port', server_address[1])
    clientsocket.connect(server_address)

    try:

        # Send data
        requestheader_requestline = "GET / HTTP/1.1\r\n".encode()
        print(requestheader_requestline)
        clientsocket.send(requestheader_requestline)

        # send host
        requestheader_host = "Host: localhost:8332\r\n".encode()
        print(requestheader_host)
        clientsocket.send(requestheader_host)

        # send authorization line
        username = bitcoinrpc_username.encode()
        password = bitcoinrpc_password.encode()
        base64string = base64.encodebytes((username + ':'.encode() + password)).decode()
        authline = 'Authorization: Basic ' + base64string + "\r\n"
        requestheader_authorization = str.encode(authline)
        print(requestheader_authorization)
        clientsocket.send(requestheader_authorization)

        # send newline preceding response message body
        clientsocket.send('\r\n'.encode())  # to separate headers from body

        data = clientsocket.recv(1024)  # receive data from client
        string = bytes.decode(data)  # decode it to string

        # determine request method  (HEAD and GET are supported)
        request_method = string.split(' ')[0]
        print("Method: ", request_method)
        print("Request body: ", string)

    finally:
        print('closing socket')
        clientsocket.close()

    # TODO: add a proper server
    # resume server-side logic
    responsebody = '{"result":null,"error":{"code":-32700,"message":"Parse error"},"id":null}'.encode()

    # Reply as HTTP/1.1 server, saying "HTTP OK" (code 200).
    responseheader_statusline = "HTTP/1.1 200 OK\r\n".encode()
    serversocket.send(responseheader_statusline)

    # send Access header allowing for CORS
    responseheader_accesscontrolalloworigin = str.encode("Access-Control-Allow-Origin: " + str(clientorigin) + "\r\n")
    serversocket.send(responseheader_accesscontrolalloworigin)

    # send Access-Control-Allow-Credentials header to allow login
    responseheader_accessallowcredentials = "Access-Control-Allow-Credentials: true\r\n".encode()
    serversocket.send(responseheader_accessallowcredentials)

    # send Content-Type
    responseheader_contenttype = "Content-Type: text/plain; encoding=utf8\r\n".encode()
    serversocket.send(responseheader_contenttype)

    # send Content-Length
    responseheader_contentlength = str.encode("Content-Length: " + str(len(responsebody)) + "\r\n")
    serversocket.send(responseheader_contentlength)

    # send server name
    responseheader_server = "Server: pyBitcoinRpcProxy\r\n".encode()
    serversocket.send(responseheader_server)

    # send connection close
    responseheader_connectionclose = "Connection: close\r\n".encode()
    serversocket.send(responseheader_connectionclose)

    # send newline preceding response message body
    serversocket.send('\r\n'.encode())  # to separate headers from body

    # send response message body
    serversocket.send(responsebody)

    # sleep to allow client to receive all data
    time.sleep(0.5)

    # close the connection
    serversocket.close()

    # Session done
    print("Connection closed")