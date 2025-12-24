import socket
import time

#-------------SERVER----------#

port = 1111

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

my_socket.bind(("localhost", port))

accept_state = False

client = None
address = None

my_socket.listen(5)

def send_receive_data():
    while True:
        client.sendall(b"test sending from server\n")

        data = client.recv(1024)
        if not data:
            print(f"Client {address} disconnected")
            break

        print(f"Received from {address}: {data.decode()}")

while True:
    time.sleep(0.5)
    try:
        client, address = my_socket.accept()
        print(f"socked accepted, {client}, {address}")

        with client:
            send_receive_data()

    except Exception as e:
        print(f"Error: {e}")


