import socket
from time import sleep
import threading
from queue import Queue
from client_funcs import *
import ssl
from datetime import datetime, timezone
import sys
from pathlib import Path
#-----------------CLIENT-------------------------#

hostname = "p9cx.org"

context = ssl.create_default_context()

port = 1111
send_info_queue = Queue(maxsize=10)   # thread safe data exchange
message_lock = threading.Lock()

QUICK_GUIDE = "simply type, and press enter to transmit: \n"
USER_JSON_NAME = "user_data.json"

BASE_DIR = Path(__file__).resolve().parent
storing = JsonStoring(BASE_DIR / USER_JSON_NAME)

print("For more information check out the GitHub \n https://github.com/mynameisVictoria/comms-platform \n")

if not storing.check_name():
    name = input("Whats your name? \n")
    storing.write_name(name)
elif storing.check_name():
    name_decision = input(f"do you wish to change your name, current name: {storing.get_name()} \n y or n \n")
    if name_decision.lower() == "y":
        new_name = input("input new name \n")
        storing.write_name(new_name)
print(QUICK_GUIDE)

def handle_input():
    while True:
        sleep(0.1)
        send_info_input = input("")
        if not send_info_input.strip() == "":
            with message_lock:
                send_info_queue.put(send_info_input)
        else:
            pass
        if send_info_input == "exit":
            sys.exit()
def constant_recv(recv_socket):
    while True:
        sleep(0.1)
        try:
            print(recv_socket.recv(1024).decode())
        except socket.timeout:
            continue
        except Exception:
            pass

def format_message(username, message):
    timestamp = datetime.now(timezone.utc).strftime('%H:%M:%S')
    return f"[{timestamp} ] | {username}: {message}"

def main():

    while True:
        sleep(0.5)

        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Source - https://stackoverflow.com/a
            # Posted by Joshua Wolff
            # Retrieved 2025-12-30, License - CC BY-SA 4.0
            # noinspection PyUnresolvedReferences
            my_socket.settimeout(0.5)

            tls_socket = context.wrap_socket(
                my_socket,
                server_hostname=hostname
            )

            tls_socket.connect((hostname, port))
            recv_thread = threading.Thread(target=constant_recv, daemon=True, args=(tls_socket,))
            recv_thread.start()

            while True:
                sleep(0.1)
                if send_info_queue.empty():  #if its empty, reset the loop
                    continue
                elif not send_info_queue.empty():  #if it's not empty, try to send the data
                    try:
                        with message_lock:
                            send_data = format_message(storing.get_name(), send_info_queue.get())
                            tls_socket.sendall(send_data.encode("utf-8"))
                    except (socket.error, OSError):   #don't really know what can go wrong
                        break

        except socket.error:
            print("test")

input_thread = threading.Thread(target=handle_input)
input_thread.start()   #starts the user input thread

main()
input_thread.join()
