# Author: Devon Miller
# Date: 11/25/2022
# Course: CS 372
# Assignment: Project 4: Client Server Chat
# Description: This file holds the client portion of a client server chat
#               program client and server send messages to each other over
#               a single socket connection until one of the parties closes
#               the chat

import socket


class Client():
    """instance of client to interact with Server() class"""

    def __init__(self):
        self.instructions = "In this game the serverside decides on a person place thing or other" + "\n" + \
                            "accepted target. The server enters this object when prompted to start the" + "\n" + \
                            "game and it is the client sides job to guess what the thing is. The client can \n" + "\n" + \
                            "ask up to 20 questions/guesses. When you think you know the answer enter it as \n" + "\n" + \
                            "the only word without any punctuation."

    def client(self):
        """client connects to local host and same port as Server() then
        sends messages back and forth taking turns in a game of 20 questions"""
        HOST = "127.0.0.1"               # local host
        PORT = 16022                     # same as Server()
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((HOST, PORT))
        print("Welcome to 20 Questions!")
        print(self.instructions)
        print("The server side will think of a person place or thing and you need go guess!")
        print("-----------------------------------------------------------------------")
        print("on your turn enter /q to quit")
        print("Opponent chosing something to guess.......")
        self.__connect(connection)

    def __connect(self, connection):
        """private function for a single connection called by client
        function"""
        while True:
            response = connection.recv(1024)
            print(response.decode())
            if b"/q" in response:    # quit
                connection.close()
                break
            data = input(">>> ")
            data = bytes(data, 'utf-8')
            if data == b"/q":   # quit
                connection.send(data)
                connection.close()
                break
            connection.sendall(data)  # data to display in browser


if __name__ == "__main__":
    client = Client()
    client.client()
