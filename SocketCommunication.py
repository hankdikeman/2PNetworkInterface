import socket as skt

# create new socket object
move_ex = skt.socket()

# get hostname of computer and print
print(skt.gethostname())

# get IP number of computer
print(skt.gethostbyname(skt.gethostname()))

# generate server socket with TCP connection
addr = ("", 8080)  # all interfaces, port 8080
if socket.has_dualstack_ipv6():
    s = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
else:
    s = socket.create_server(addr)
