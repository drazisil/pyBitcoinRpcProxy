import base64
from email.parser import Parser
import socket

__author__ = 'joseph'


def proxyclient(bitcoinrpc_port, bitcoinrpc_username, bitcoinrpc_password, requestbody):
    # TODO: create a cleaner client

    # Create a TCP/IP socket
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', bitcoinrpc_port)
    clientsocket.connect(server_address)

    try:

        # assemble request for bitcoin server
        requeststring = ''
        requeststring += "POST / HTTP/1.1\r\n"
        requeststring += "Host: localhost:8332\r\n"

        # send authorization line
        username = bitcoinrpc_username.encode()
        password = bitcoinrpc_password.encode()
        base64string = base64.encodebytes((username + ':'.encode() + password)).decode()
        authline = 'Authorization: Basic ' + base64string
        requeststring += authline
        requeststring += "Content-Length: " + str(len(requestbody)) + "\r\n"
        requeststring += '\r\n'
        requeststring += requestbody

        # send the request to the bitcoin server
        clientsocket.send(requeststring.encode())

        data = clientsocket.recv(1024)  # receive data from client
        rawdataclient = bytes.decode(data)  # decode it to string

        # remove the status line from the data
        tmp2 = rawdataclient.split("\r\n")
        del tmp2[0]

        # parse the data into an email.message object
        responsedata = Parser().parsestr("\r\n".join(tmp2))

        mail2 = responsedata.get_payload()
        responsebody = mail2

    finally:
        clientsocket.close()

    return responsebody