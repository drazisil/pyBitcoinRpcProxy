from email.parser import Parser
import socket
import time
import sys

import proxyClient


__author__ = 'joseph'


def proxyserver(bitcoinrpc_webport, bitcoinrpc_port, bitcoinrpc_username, bitcoinrpc_password):
    # This is the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object

    host = 'localhost'  # Get local machine name
    port = bitcoinrpc_webport  # Reserve a port for your service.
    s.bind((host, port))  # Bind to the port
    print('Running server on', host, 'on port', port)

    try:
        while True:
            s.listen(5)  # Now wait for client connection.

            requestdata = []
            clientorigin = ''
            serversocket, addr = s.accept()  # Establish connection with client.

            data = serversocket.recv(1024)  # receive data from client
            rawdataserver = bytes.decode(data)  # decode it to string

            try:
                # remove the request line from the data
                headerlines = rawdataserver.split("\r\n")
                del headerlines[0]

                # parse the data into an email.message object
                requestdata = Parser().parsestr("\r\n".join(headerlines))

                # set the origin host for use with CORS later
                clientorigin = requestdata['Origin']

            except IndexError:
                # close the connection
                serversocket.close()
                exit()

            # get the request body from the browser
            mail = requestdata.get_payload()
            requestbody = mail

            # call the client
            responsebody = proxyClient.proxyclient(bitcoinrpc_port, bitcoinrpc_username, bitcoinrpc_password,
                                                   requestbody)

            # assemble the response
            responsestring = ''
            responsestring += "HTTP/1.1 200 OK\r\n"
            responsestring += "Access-Control-Allow-Origin: " + str(clientorigin) + "\r\n"
            responsestring += "Access-Control-Allow-Credentials: true\r\n"
            responsestring += "Content-Type: text/plain; encoding=utf8\r\n"
            responsestring += "Content-Length: " + str(len(responsebody))
            responsestring += "Server: pyBitcoinRpcProxy\r\n"
            responsestring += "Connection: close\r\n"
            responsestring += "\r\n"
            responsestring += str(responsebody)

            # send response
            serversocket.send(responsestring.encode())

            # sleep to allow client to receive all data
            time.sleep(0.5)

            # close the connection
            serversocket.close()

    except KeyboardInterrupt:
        # quit
        sys.exit()