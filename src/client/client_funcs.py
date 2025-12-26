import socket

class Client:
    def __init__(self, port, client_address, client_socket, server_socket):
        self.port = port
        self.server_socket = server_socket
        self.client_socket = client_socket
        self.client_address = client_address

    def receive_data(self):
        data = self.client_socket.recv(1024)
        if not data:
            return False
        elif data:
            return data.decode()
        else:
            return False

    def send_data(self, send_data):
        try:
            self.client_socket.sendall(send_data.encode())
            return True
        except socket.error:
            return False
        except Exception as err:
            return err
        





