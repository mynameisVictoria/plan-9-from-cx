import socket
import errno
import time
import threading
from queue import Queue
from client_funcs import *

#-----------------CLIENT-------------------------#
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.settimeout(0.5)

port = 1111

send_info_queue = Queue(maxsize=10)   # thread safe data exchange

storing = JsonStoring()

if not storing.check_name():
    name = input("Whats your name?")
    storing.write_name(name)
elif storing.check_name():
    name_decision = input(f"do you wish to change your name, current name: {storing.read_name()} \n y or n \n")
    if name_decision.lower() == "y":
        new_name = input("input new name \n")
        storing.write_name(new_name)
    elif name_decision.lower() == "n":
        print("cool")
    else:
        print("\n")

def handle_input():
    while True:
        send_info_input = input("")
        send_info_queue.put(send_info_input)
        if send_info_input == "exit":
            break

def constant_recv():
    while True:
        time.sleep(0.1)
        try:
            print(my_socket.recv(1024).decode())
        except socket.timeout:
            continue
        except Exception:
            pass

def main():
    connected = False

    while True:
        time.sleep(0.5)
        if not connected:
            try:
                my_socket.connect(("127.0.0.1", port))
                print("socket connected")
                connected = True
            except OSError as e:
                if e.errno in (errno.EISCONN, 56):  #checks if its already connected
                    print("ERROR")
                    connected = True
                else:   #idfk man
                    connected = False

        elif connected:
            if send_info_queue.empty():  #if its empty, reset the loop
                continue
            elif not send_info_queue.empty():  #if it's not empty, try to send the data
                try:
                    send_data = storing.read_name() + ": " + send_info_queue.get()
                    if send_data == "exit":
                        break
                    else:
                        my_socket.sendall(send_data.encode("utf-8"))
                        #print("sent")
                except (socket.error, OSError) as err:   #don't really know what can go wrong
                    print(err)

input_thread = threading.Thread(target=handle_input)
recv_thread = threading.Thread(target=constant_recv, daemon=True)

input_thread.start()   #starts the user input thread
recv_thread.start()

main()
input_thread.join()
recv_thread.join()
