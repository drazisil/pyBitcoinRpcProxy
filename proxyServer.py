from email.parser import Parser
import socket
import time

import proxyClient


__author__ = 'joseph'


def proxyserver(bitcoinrpc_webport, bitcoinrpc_port, bitcoinrpc_username, bitcoinrpc_password):
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
        rawdataserver = bytes.decode(data)  # decode it to string
        request_method = []

        try:
            request_method = rawdataserver.split(' ')[0]
            # TODO: extract the request body

            # remove the request line from the data
            headerlines = rawdataserver.split("\r\n")
            del headerlines[0]

            # parse the data into an email.message object
            requestdata = Parser().parsestr("\r\n".join(headerlines))

            # print('Header count:', len(headers))
            # print('All Headers:', requestdata.keys())

            # set the origin host for use with CORS later
            clientorigin = requestdata['Origin']

        except IndexError:
            # TODO: check if this is a Keep-Alive behavior
            # close the connection
            serversocket.close()
            exit()

        print('=== Server recieving from Browser ===')
        print('Got connection from', clientorigin)

        # determine request method  (HEAD and GET are supported)
        print("Method: ", request_method)

        mail = requestdata.get_payload()
        requestbody = mail

        print("Request body: ", requestbody)

        # call the client
        responsebody = proxyClient.proxyclient(bitcoinrpc_port, bitcoinrpc_username, bitcoinrpc_password, requestbody)

        # resume server-side logic

        # TODO: create a cleaner server

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

        # Session done
        print("Connection closed")
        print("---------------------------------------------------")