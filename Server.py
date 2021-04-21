import socket
import threading

host = '127.0.0.1'
port = 21000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
nicknames = []
privates = []


def broadcast(message):
    for client in clients:
        client.send(message)


def welcome(client):
    client.send(f"Hi {nicknames[clients.index((client))]} Welcome to the Chatroom\n".encode('utf-8'))


def Clientlist(client):
    client.send(f"Here is the list of attendees:\n\r{nicknames}\n".encode('utf-8'))


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(nicknames)
            print(clients)

            broadcast(message)

            command = message.decode('utf-8').split(':')
            private = command[1].split(' ')
            hello = command[1].split(' ')

            if command[1] == 'Bye\n':
                broadcast(f"{nicknames[clients.index((client))]} left the chatroom \n".encode('utf-8'))
                index = clients.index(client)
                clients.remove(client)
                client.close()

                nickname = nicknames[index]
                nicknames.remove(nickname)
                break

            elif command[1] == 'Please send the list of attendees.\n':
                Clientlist(client)

          


            elif hello[0] == 'Hello':
                welcome(client)

        except:
            broadcast(f"{nicknames[clients.index((client))]} left the chatroom\n ".encode('utf-8'))
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break



def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with{str(address)}")

        client.send("N".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f"nickname of the client{nickname}")
        broadcast(f"{nickname} join the chat room.\n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("server running....")
receive()
