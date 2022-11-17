# Author: Devon Miller
# Date: 11/25/2022
# Course: CS 372
# Assignment: Project 4: Client Server Chat
# Description: This file holds the server portion of a client server chat program client and
#               server send messages to each other over a single socket connection until one of
#               the parties closes the chat

def server():
    """ Simple server that accepts connections, prints response to terminal, sends html
    data viewable through browser and prints this data to the terminal"""

    import socket
    HOST = "127.0.0.1"                                    # local host
    PORT = 16022                                          # can be any port > 1023

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:     # TCP connection
        socket.bind((HOST, PORT))                        # bind host and port to allow socket connections
        socket.listen()
        connection, address = socket.accept()            # connection is socket connection, adress is connected machine
        #with connection:
        print(f"Connected by {address}")
        print("welcome to 20 questions, as the server you'll choose an object the client must guess!")
        goal = input("what will the client try to guess?\n")
        goal = bytes(goal, 'utf-8')
        print("Lets begin!")
        print("on your turn enter /q to quit")
        guesses = 19
        data = (b"The game has begun, you have %d guesses left" % guesses)
        connection.send(data)
        while True:
            #print(f"Connected by {address}")
            response = connection.recv(1024)             # one recv is sufficient to read all data here
            print(response.decode())
            if response == "/q":
                connection.close()
            print(True, response, goal)
            if response == goal:
                print("The client won!")
                data = b"Youre the winner great job!"
                connection.send(data)
                connection.send(b"/q")
                connection.close()
            if guesses == 0:
                print("The client ran out of guesses you've won!")
                data = b"You ran out of guesses, YOU LOST!"
                connection.send(data)
                connection.send(b"/q")
                connection.close()
            data = input("(yes or no >>>>>>> ")
            print(data)
            if data == b"/q":
                connection.send(data)
                connection.close()
            data = bytes(data + ", you have %d guesses left" % guesses, 'utf-8')
            connection.sendall(data)
            guesses -= 1

            #print("Sending>>>>>>>>")


if __name__ == "__main__":
    server()
