# Author: Devon Miller
# Date: 11/25/2022
# Course: CS 372
# Assignment: Project 4: Client Server Chat
# Description: This file holds the server portion of a client server chat
#               program client and server send messages to each other over
#               a single socket connection until one of parties closes the chat

class Server():
    """server class holds instance of server to connect with Client() class"""
    def server(self):
        """binds to port and local host then communicates back and forth with
        client in a game of 20 questions where the client must guess an object
        of the servers choosing"""
        import socket
        HOST = "127.0.0.1"       # local host
        PORT = 16022             # same port as Client()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
            socket.bind((HOST, PORT))
            socket.listen()
            connection, address = socket.accept()
            print(f"Connected by {address}")
            print("welcome to 20 questions, as the server you'll choose an \
            object the client must guess!")
            goal = input("what will the client try to guess?\n")  # string to guess
            goal = bytes(goal, 'utf-8')
            print("Lets begin!")
            print("on your turn enter /q to quit")
            guesses = 19           # number of guesses to guess goal
            data = (b"The game has begun, you have %d guesses left" % guesses)
            connection.send(data)
            self.__connect(connection, goal, guesses)
        ""
    def __connect(self, connection, goal, guesses):
        """A connection handled by server class, connection is the connection
        goal is the string to guess, guesses are the number of remaining
        guesses"""
        while True:
            response = connection.recv(1024)
            print(response.decode())
            if b"/q" in response:     # quit
                connection.close()
                break
            if response.lower() == goal.lower():   # client wins
                self.__clientWinner(connection)
                break
            if guesses == 0:      # server wins
                self.__serverWinner(connection)
                break
            data = input(">>>>>>> ")
            if data == "/q":    # quit
                self.__quit(connection)
                break
            data = bytes(data + ", you have %d guesses \
            left" % guesses, 'utf-8')
            connection.sendall(data)
            guesses -= 1

    def __clientWinner(self, connection):
        """client wins, prints messages to client and server then closes
        connection on both sides"""
        print("The client won!")
        data = b"Youre the winner great job! /q"
        connection.send(data)
        connection.close()

    def __serverWinner(self, connection):
        """server wins, client unable to guesss object in 20 guesses"""
        print("The client ran out of guesses you've won!")
        data = b"You ran out of guesses, YOU LOST!"
        connection.send(data)
        connection.send(b"/q")
        connection.close()

    def __quit(self, connection):
        """closes connection on server and client side"""
        connection.send(b"/q")
        connection.close()


if __name__ == "__main__":
    server = Server()
    server.server()
