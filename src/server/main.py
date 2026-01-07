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

import socket
from time import sleep
import threading
import ssl

#-------------SERVER----------#

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
message_broadcast_list = []
socket_list = []
socket_lock = threading.Lock()
message_lock = threading.Lock()
history_lock = threading.Lock()

server_socket.bind(("0.0.0.0", port))
server_socket.listen(5)

def receive_data(thread_client, thread_address):
    thread_client.settimeout(0.1)
    while True:
        sleep(0.1)  #not to hoard the cpu lol
        try:
            message_data = thread_client.recv(1024).decode("utf8")

            if not message_data:  # if no data is received
                print(f"Client {thread_address} disconnected")
                with socket_lock:
                    if thread_client in socket_list:
                        socket_list.remove(thread_client)
                break

            with message_lock:
                message_broadcast_list.append(message_data)

            with history_lock:
                message_history.append(message_data)

            print(f"Received from {thread_address}: {message_data}")

        except socket.timeout:
            pass

        except ConnectionResetError:
            with socket_lock:
                socket_list.remove(thread_client)
                thread_client.close()
                print(f"Client disconnected:[{thread_address}]")
                break

        except BrokenPipeError:
            with socket_lock:
                socket_list.remove(thread_client)
                thread_client.close()
                print(f"Client disconnected:[{thread_address}]")
                break
def broadcast_messages():
    while True:
        sleep(0.1)  # avoid hoarding the cpu

        with message_lock:
            if not message_broadcast_list:  #if its empty
                continue  #restarts the loop
            msg = message_broadcast_list.pop(0)

        with socket_lock:

            for client_socket in socket_list[:]:
                try:

                    trimmed_msg = msg.strip().split(":")
                    print(trimmed_msg)

                    if "/online" in trimmed_msg:
                        counter = 0
                        for sockets in socket_list:
                            counter += 1
                        client_socket.sendall(str(counter).encode())
                        print("sent online clients")

                    else:
                        client_socket.sendall(msg.encode())

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

main()
