# import socket library
import socket
import pickle

HEADERSIZE = 10

# create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

# receive socket data (setting buffer size)
# msg = s.recv(1024)
# print(msg.decode("utf-8"))

while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(10)

        if new_msg:
            print(f"new message length: {msg[:HEADERSIZE]}")
            msg_len = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg

        if len(full_msg) - HEADERSIZE == msg_len:
            print("full message received")
            print(full_msg[HEADERSIZE:])

            d = pickle.loads(full_msg[HEADERSIZE:])
            print(d)

            new_msg = True
            full_msg = b''


    print(full_msg)
