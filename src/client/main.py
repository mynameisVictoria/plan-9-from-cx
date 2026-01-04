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

import threading
from queue import Queue
from client_funcs import *
import ssl
from time import sleep
import os 
import sys
import socket

#-----------------CLIENT-------------------------#

HOSTNAME = "p9cx.org"

context = ssl.create_default_context()

PORT = 1111
message_queue = Queue(maxsize=10)   # thread safe data exchange
message_lock = threading.Lock()

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

json_path = os.path.join(BASE_DIR, "user_data.json")
storing = JsonStoring(json_path)
user_io = GeneralIO()

print("For more information check out the GitHub \n https://github.com/mynameisVictoria/comms-platform \nDo /help for help!")

if not storing.check_name():
    name = input("Please enter your name: \n")
    storing.write_name(name)
elif storing.check_name():
    yes_or_no = input(f"Do you want to change your name? Current name: {storing.get_name()} \n y or n \n ")
    if yes_or_no.lower() == "y":
        new_name = input("Please enter your new name: \n")
        storing.write_name(new_name)

def handle_input():
    while True:
        input_data = input()
        command = Commands(input_data, storing)
        command.check_command()
        with message_lock:
            message_queue.put(input_data)

def socket_receive(recv_socket):
    message_history = b""
    while True:
        try:
            part = recv_socket.recv(1024)
        except socket.timeout:
            break
        if not part:
            break
        message_history += part

    print(message_history.decode("utf-8"))

    while True:
        sleep(0.1)
        try:
            print(recv_socket.recv(1024).decode("utf-8"))
        except socket.timeout:
            continue
        except Exception as err:
            print(err)

def main():
    while True:
        sleep(0.5)
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket.settimeout(0.5)

            tls_socket = context.wrap_socket(
                my_socket,
                server_hostname=HOSTNAME
            )

            tls_socket.connect((HOSTNAME, PORT))

            recv_thread = threading.Thread(target=socket_receive, daemon=True, args=(tls_socket,))
            recv_thread.start()

            while True:
                sleep(0.1)
                if not message_queue.empty():  #if it's not empty, try to send the data
                    try:
                        with message_lock:
                            message = message_queue.get()
                            send_data = user_io.format_message(storing.get_name(), message)
                            tls_socket.sendall(send_data.encode("utf-8"))
                    except (socket.error, OSError):
                        break

        except socket.error as err:
            print(f"socket error: {err}")

input_thread = threading.Thread(target=handle_input, daemon=True)
input_thread.start()

main()
input_thread.join()
