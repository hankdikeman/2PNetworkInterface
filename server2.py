import socket
import select

# constants incl header length, IP num, and port num
HEADER_LENGTH = 10
IP = socket.gethostname()
PORT = 1234

# generate TCP server socket and allow to reuse address
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind server to server socket
server_socket.bind((IP, PORT))
server_socket.listen()

# list of sockets for server and users
sockets_list = [server_socket]

# list of clients with identifying info beyond IP
clients = {}

# define message receive funnction from
def receive_msg(client_socket):
    try:
        msg_header = client_socket.recv(HEADER_LENGTH)

        if not len(msg_header):
            return False

        msg_len = int(msg_header.decode('utf-8').strip())
        return {"header": msg_header, "data": client_socket.recv(msg_len)}

    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        # receive new user and add to list of users in chat
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            # read in connection messages from server socket and store in user
            user = receive_msg(client_socket)
            # if user is false, some connection error
            if user is False:
                continue

            # append new connection to client list
            sockets_list.append(client_socket)

            # new user added to client dictionary
            clients[client_socket] = user
            # new user connection message
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
        # receive a normal message from an already connected user
        else:
            msg = receive_msg(notified_socket)
            # remove client if no connection is found
            if msg is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            # set user to the socket where message was sent from
            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {msg['data'].decode('utf-8')}")
            # send message to all other active users
            for client_socket in clients:
                if client_socket != notified_socket:
                    print(user['header'] + user['data'] + msg['header'] + msg['data'])
                    client_socket.send(user['header'] + user['data'] + msg['header'] + msg['data'])
    # if there is some error in connections remove socket connections
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
