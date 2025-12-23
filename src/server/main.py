import socket

#-------------SERVER----------#

port = 1111

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

my_socket.bind(("localhost", port))

accept_state = False

client = None
address = None

while True:


    my_socket.listen(5)
    try:
        client, address = my_socket.accept()
        print(f"socked accepted, {client}, {address}")
        accept_state = True
    except Exception as err:
        print(f"Error: {err}")

    if accept_state:
        client.sendall(b"test sending from server \n")
        data = client.recv(1024)
        if not data:
            client.close()
    elif not accept_state:
        accept_state = False

