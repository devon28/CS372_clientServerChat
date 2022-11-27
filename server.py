# Author: Devon Miller
# Date: 11/24/2022
# Course: CS 372
# Assignment: Project 4: Client Server Chat
# Description: This file holds the server portion of a client server chat
#               program client and server send messages to each other over
#               a single socket connection until one of parties closes the chat
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

import threading
import sys


class Server():
    """server using sockets that accepts one connection from client()
    used for game of 20 questions between server and client"""
    def __init__(self):
        """variables to be used in functions or set by the Server() user
        upon the game starting"""
        self.instructions = "In this game the serverside decides on a person place thing or other" + "\n" + \
                            "accepted target. The server enters this object when prompted to start the" + "\n" + \
                            "game and it is the client sides job to guess what the thing is. The client can \n" + "\n" + \
                            "ask up to 20 questions/guesses. When you think you know the answer enter it as \n" + "\n" + \
                            "the only word without any punctuation."
        self.guesses = 19
        self.HOST = "127.0.0.1"            # local host
        self. PORT = 16022                 # same port as Client()
        self.goal = ""
        self.connection = ""

    def server(self):
        """binds to port and local host then communicates back and forth with
        client in a game of 20 questions where the client must guess an object
        of the servers choosing"""
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
            socket.bind((self.HOST, self.PORT))
            socket.listen()
            self.socket = socket
            connection, address = socket.accept()
            self.connection = connection
            print(f"Connected by {address}")
            print("welcome to 20 questions!")
            print(self.instructions)
            print("As the server you'll choose an object the client must guess!")
            goal = input("what will the client try to guess? \n")  # string to guess
            self.goal = bytes(goal, 'utf-8')
            print("Lets begin!")
            print("------------------------------------------------------------------------------")
            print("on your turn enter /q to quit")
            data = bytes("The game has begun, you have %d guesses left!" % (self.guesses + 1), "utf-8")
            self.connection.send(data)
            self.__connect(connection)

    def __connect(self, connection):
        """a connection to Client() using theading to receive and 
        send messages back and forth"""
        sending = threading.Thread(target=Server.__sendMessages, args=(self,))
        receiving = threading.Thread(target=Server.__receiveMessages, args=(self,))
        sending.setDaemon(True)
        sending.start()
        receiving.start()

    def __sendMessages(self):
        """sends messages to Client(), if 20 messages are sent without
        self.goal being guessed the server wins"""
        while True:
            if self.guesses == -1:  # server wins
                self.__serverWinner()
                break
            data = input("")
            if "/q" in data:  # quit
                print("Game over, your quit")
                self.connection.send(b"/q")
                self.__exitProgram()
            data = bytes(data + ", you have %d guesses left" % self.guesses, 'utf-8')
            self.connection.sendall(data)
            self.guesses -= 1

    def __receiveMessages(self):
        """receives messages from Client(), if self.goal is guessed in
        a message the client wins, if /q is sent connection is closed and
        program shuts down"""
        while True:
            try:               
                response = self.connection.recv(1024)
            except Exception:          # game quit, connection closed
                break
            print("(Opponent): " + response.decode())
            if b"/q" in response:                      # quit
                print("Game over, your opponent quit")
                self.__exitProgram()
            if response.lower() == self.goal.lower():  # client wins
                self.__clientWinner()
                break

    def __clientWinner(self):
        """client wins, prints messages to client and server then closes
        connection on both sides"""
        print("The client won!")
        data = b"Youre the winner great job! /q"
        self.connection.send(data)
        self.__exitProgram()

    def __serverWinner(self):
        """server wins, client unable to guesss object in 20 guesses"""
        print("The client ran out of guesses you've won!")
        data = b"You ran out of guesses, YOU LOST! /q"
        self.connection.send(data)
        self.__exitProgram()

    def __exitProgram(self):
        """closes connection and exits program"""
        print("Game over")
        self.connection.close()
        sys.exit([0])


if __name__ == "__main__":
    server = Server()
    server.server()
