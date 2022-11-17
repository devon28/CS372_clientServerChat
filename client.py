# Description: This file holds the client portion of a client server chat program client and
#               server send messages to each other over a single socket connection until one of
#               the parties closes the chat

import socket

def client():
    """ Makes socket connection to gaia.cs.umass.edu, sends GET request, prints response
    to GET request and closes socket connection"""

    HOST = "127.0.0.1"  # local host
    PORT = 16022  # can be any port > 1023

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # TCP connection
    connection.connect((HOST, PORT))
    print("Welcome to 20 questions, the server thought of a person place or thing and you need go guess!")
    print("on your turn enter /q to quit")
    print("Opponent chosing something to guess.......")
    #connect(connection)
    while True:
        response = connection.recv(1024)  # one recv is sufficient to read all data here
        print(response.decode())
        if response == b"/q":
            connection.close()
            break
        data = input(">>> ")
        data = bytes(data, 'utf-8')
        if data == b"/q":
            connection.send(data)
            connection.close()
            break
        connection.sendall(data)  # data to display in browser

if __name__ == "__main__":
    client()