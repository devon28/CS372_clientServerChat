# Description: This file holds the server portion of a client server chat program client and
#               server send messages to each other over a single socket connection until one of
#               the parties closes the chat

class Server():
    def server(self):

        import socket
        HOST = "127.0.0.1"                                    # local host
        PORT = 16022                                          # can be any port > 1023
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:     # TCP connection
            socket.bind((HOST, PORT))
            socket.listen()
            connection, address = socket.accept()
            print(f"Connected by {address}")
            print("welcome to 20 questions, as the server you'll choose an object the client must guess!")
            goal = input("what will the client try to guess?\n")
            goal = bytes(goal, 'utf-8')
            print("Lets begin!")
            print("on your turn enter /q to quit")
            guesses = 20
            data = (b"The game has begun, you have %d guesses left" % guesses)
            connection.send(data)
            self.__connect(connection, goal, guesses)
        ""
    def __connect(self, connection, goal, guesses):
        while True:
            response = connection.recv(1024)  # one recv is sufficient to read all data here
            print(response.decode())
            if b"/q" in response:
                connection.close()
                break
            if response.lower() == goal.lower():
                self.__clientWinner(connection)
                break
            if guesses == 0:
                self.__serverWinner(connection)
                break
            data = input(">>>>>>> ")
            if data == "/q":
                self.__quit(connection)
                break
            data = bytes(data + ", you have %d guesses left" % guesses, 'utf-8')
            connection.sendall(data)
            guesses -= 1

    def __clientWinner(self, connection):
        print("The client won!")
        data = b"Youre the winner great job! /q"
        connection.send(data)
        connection.close()

    def __serverWinner(self, connection):
        print("The client ran out of guesses you've won!")
        data = b"You ran out of guesses, YOU LOST!"
        connection.send(data)
        connection.send(b"/q")
        connection.close()

    def __quit(self, connection):
        connection.send(b"/q")
        connection.close()

if __name__ == "__main__":
    server = Server()
    server.server()
