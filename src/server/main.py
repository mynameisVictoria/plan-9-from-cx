import socket
import time
import threading

#-------------SERVER----------#

port = 1111

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.bind(("0.0.0.0", port))

message_list = []
socket_list = []
socket_lock = threading.Lock()
message_lock = threading.Lock()

print("Welcome!")

my_socket.listen(5)

def send_receive_data(thread_client, thread_address):
    thread_client.settimeout(0.1)
    while True:
        try:
            data = thread_client.recv(1024)
            print("data received")
            if not data:         # if no data is received
                print(f"Client {thread_address} disconnected")
                with socket_lock:
                    if thread_client in socket_list:
                        socket_list.remove(thread_client)
                break
            with message_lock:
                message_list.append(data)

            print(f"Received from {thread_address}: {data.decode()}")

        except socket.timeout:
            pass
        except Exception as err:
            print(f"{err}")

def broadcast_messages():
    while True:
        time.sleep(0.1)

        with message_lock:
            if not message_list:
                continue
            msg = message_list.pop(0)

        with socket_lock:

                for list_client in socket_list[:]:
                    try:
                        list_client.sendall(msg)
                    except OSError as e:
                        socket_list.remove(list_client)
                        list_client.close()


broadcast_thread = threading.Thread(
    target=broadcast_messages,
    daemon=True
    )
broadcast_thread.start()
print("broadcast thread started")

while True:
    time.sleep(0.1)
    try:
        client, address = my_socket.accept()
        with socket_lock:
            socket_list.append(client)
        client_thread = threading.Thread(
            target=send_receive_data,
            args=(client, address),
            daemon=True)

        client_thread.start()
        print("threads started")

    except OSError:
        pass

    except Exception as err:
        print(err)
