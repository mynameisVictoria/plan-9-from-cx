#  Copyright (C) <2026>  <mynameisVictoria>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

#-------------SERVER----------#
#--- In full cander, I must reveal the truth, this code is absolute shit,     ↓
#--- this script is a direct descendant of the first tcp server I ever        ↓
#--- made if that matters. I will be incredibly shocked if this piece of      ↓
#--- shit can handle more than 5 clients reliably (it cannot handle 1 client- ↓
#--- reliably even)
#--- I will fix it... eventually, good luck!

from server_methods import format_message
import socket
from time import sleep
import threading
import ssl

port = 1111

server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
server_context.load_cert_chain(
    certfile="/etc/letsencrypt/live/p9cx.org/fullchain.pem",
    keyfile="/etc/letsencrypt/live/p9cx.org/privkey.pem"
)

client_context = ssl.create_default_context()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

message_history = []
history_lock = threading.Lock()

message_broadcast_list = []
message_broadcast_lock = threading.Lock()

socket_list = []
socket_lock = threading.Lock()

socket_username_dict = {}
socket_username_lock = threading.Lock()

server_socket.bind(("0.0.0.0", port))
server_socket.listen()


def receive_data(thread_client, thread_address):
    thread_client.settimeout(0.5)
    username = thread_client.recv(1024).decode("utf8")

    with socket_username_lock:
        socket_username_dict.update({thread_client: username})

    while True:
        sleep(0.1)  #not to hoard the cpu lol
        try:
            message_data = thread_client.recv(1024).decode("utf8")

            if not message_data:  # if no data is received
                with socket_lock:
                    if thread_client in socket_list:
                        socket_list.remove(thread_client)

                print(f"Client {thread_address} disconnected")

                break

            with message_broadcast_lock:
                message_broadcast_list.append((thread_client,message_data))

            print(f"Received from {thread_address}: {message_data}")

        except socket.timeout:
            pass

        except (BrokenPipeError, ConnectionResetError):
            with socket_lock:
                socket_list.remove(thread_client)
                thread_client.close()

                with socket_lock:
                    socket_list.remove(thread_client)

                print(f"Client disconnected:[{thread_address}]")
                break

def broadcast_messages():
    while True:
        sleep(0.1)  # avoid hoarding the cpu

        with message_broadcast_lock:
            if not message_broadcast_list:
                continue

            message_tuple = message_broadcast_list.pop(0)
            client_sock, msg = message_tuple

            with socket_lock:
                for key in socket_username_dict:
                    if key == client_sock:
                        username = socket_username_dict[key]


        with socket_lock:

            for client_socket in socket_list[:]:
                try:

                    formatted_message = format_message(username, msg.strip())
                    client_socket.sendall(formatted_message.encode("utf-8"))

                    with history_lock:
                        message_history.append(formatted_message)

                except OSError:
                    socket_list.remove(client_socket)
                    client_socket.close()

def main():
    broadcast_thread = threading.Thread(
        target=broadcast_messages,
        daemon=True
    )
    broadcast_thread.start()
    print("broadcast thread started")

    while True:
        sleep(0.1)  #dont wanna take up the cpu
        try:
            client, address = server_socket.accept()
            tls_client = server_context.wrap_socket(client, server_side=True)

            history_data = ""

            with history_lock:
                for index in message_history:
                    history_data += index + "\n"
                tls_client.sendall(history_data.encode())

            with socket_lock:
                socket_list.append(tls_client)

            client_thread = threading.Thread(
                target=receive_data,
                args=(tls_client, address),
                daemon=True)

            client_thread.start()
            print("threads started")

        except OSError:
            continue
        except Exception as err:
            print(err)

if "__main__" == __name__:
    main()