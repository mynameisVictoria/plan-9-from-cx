import socket

#-------------SERVER----------#

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 1111

my_socket.bind(("localhost", port))



while True:
    my_socket.listen(5)
    try:
        client, address = my_socket.accept()
        print("socket accepted")
        #client.sendall(b"test sending from server \n")
        print(client.recv(1024))
    except socket.error:
        continue
