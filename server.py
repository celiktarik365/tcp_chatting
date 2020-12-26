import socket
import threading

# connection data
#host = "127.0.0.1"
#port = 55555

# starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 55555))
server.listen()

# list for clients and their nicknames
clients = []
nicknames = []

# sending messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# handling messages from clients
def handle(client):
    while True:
        try:
            # brodcasting messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # removing and closing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode(ascii))
            nickname.remove(nickname)
            break

# receiving / listening function
def receive():
    while True:
        # accept connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        
        # request and store nickname
        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        # print and broadcast
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode("ascii"))
        client.send("Connected to server!".encode("ascii"))

        # start handling thread for client
        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

receive()