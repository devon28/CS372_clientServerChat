# Author: Devon Miller
# Date: 11/24/2022
# Course: CS 372
# Assignment: Project 4: Client Server Chat
# Description: This file holds the client portion of a client server chat
#               program client and server send messages to each other over
#               a single socket connection until one of the parties closes
#               the chat
# Sources:
# ames F. Kurose and Keith W. Ross. 2012. Computer Networking: A Top-Down Approach (6th Edition) (6th. ed.). Pearson.
# Lewis, B (2022). [Lecture notes CS 372] Socket Programming. Oregon State University.
# https://canvas.oregonstate.edu/courses/1921178/pages/exploration-socket-programming?
# Multithreading in Python: Set 1. GeeksforGeeks. (2022, August 10). Retrieved November 27, 2022, from
# https://www.geeksforgeeks.org/multithreading-python-set-1/
# @mayurbadole2407. (2021, August 17). Python daemon threads. GeeksforGeeks. Retrieved November 27, 2022, from
# https://www.geeksforgeeks.org/python-daemon-threads/
# Threading - thread-based parallelism¶. threading - Thread-based parallelism - Python 3.11.0 documentation. (n.d.).
# Retrieved November 27, 2022, from https://docs.python.org/3/library/threading.html
# 28.1. sys - system-specific parameters and functions¶. 28.1. sys - System-specific parameters and functions
# - Python 2.7.18 documentation. (n.d.). Retrieved November 27, 2022, from https://docs.python.org/2/library/sys.html

import socket
import threading
import sys


class Client():
    """instance of client to interact with Server() class"""
    def __init__(self):
        """variables instructions and connection to be used by methods further down"""
        self.instructions = "In this game the serverside decides on a person place thing or other" + "\n" + \
                            "accepted target. The server enters this object when prompted to start the" + "\n" + \
                            "game and it is the client sides job to guess what the thing is. The client can \n" + "\n" + \
                            "ask up to 20 questions/guesses. When you think you know the answer enter it as \n" + "\n" + \
                            "the only word without any punctuation."
        self.connection = ""
        self.PORT = 16022           # same as Server()
        self.HOST = "127.0.0.1"     # local host

    def client(self):
        """client connects to local host and same port as Server() then
        sends messages back and forth taking turns in a game of 20 questions,
        printing instructions and rules here"""
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = connection
        self.connection.connect((self.HOST, self.PORT))
        print("Welcome to 20 Questions!")
        print(self.instructions)
        print("The server side will think of a person place or thing and you need go guess!")
        print("-----------------------------------------------------------------------")
        print("on your turn enter /q to quit")
        print("Opponent chosing something to guess.......")
        self.__connect()

    def __connect(self):
        """private function for a single connection called by client
        function uses threds to call receive and send methods"""
        sending = threading.Thread(target=Client.__sendMessages, args=(self,))
        receiving = threading.Thread(target=Client.__receiveMessages, args=(self, ))
        sending.setDaemon(True)
        receiving.start()
        sending.start()

    def __sendMessages(self):
        """private function for sending messages to Server()"""
        while True:
            data = input("")
            data = bytes(data, 'utf-8')
            if b"/q" in data:         # quit
                self.connection.send(b"/q")
                print("Game over, you quit")
                self.__exitProgram()
            else:
                self.connection.send(data)  # data to display in browser

    def __receiveMessages(self):
        """private function for receiving messages from server
        checks if game is over by looking for /q as part of response"""
        while True:
            try:
                response = self.connection.recv(1024)
            except Exception:  # connection closed
                break
            print("(opponent): " + response.decode())
            if "/q" in response.decode():         # quit
                print("Game over")
                self.connection.close()
                self.__exitProgram()

    def __exitProgram(self):
        """closes connection and exits program"""
        self.connection.close()
        sys.exit([0])


if __name__ == "__main__":
    client = Client()
    client.client()
