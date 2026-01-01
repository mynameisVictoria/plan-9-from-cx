import socket
import threading
from queue import Queue
from client_funcs import *
import ssl
from pathlib import Path
#-----------------CLIENT-------------------------#

HOSTNAME = "p9cx.org"

context = ssl.create_default_context()

PORT = 1111
message_queue = Queue(maxsize=10)   # thread safe data exchange
message_lock = threading.Lock()

QUICK_GUIDE = "simply type, and press enter to transmit: \n"
USER_JSON_NAME = "user_data.json"

BASE_DIR = Path(__file__).resolve().parent
storing = JsonStoring(BASE_DIR / USER_JSON_NAME)

user_io = GeneralIO()
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
    message_queue.put(user_io.get_input())

def socket_receive(recv_socket):
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
                input_thread = threading.Thread(target=handle_input)
                input_thread.start()

                if not message_queue.empty():  #if it's not empty, try to send the data
                    try:
                        with message_lock:
                            send_data = user_io.format_message(storing.get_name(), message_queue.get())
                            tls_socket.sendall(send_data.encode("utf-8"))
                    except (socket.error, OSError):
                        break

        except socket.error:
            print("test")

main()
