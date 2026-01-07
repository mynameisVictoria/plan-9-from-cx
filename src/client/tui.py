import time

from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea
import queue
from client_funcs import *
import threading
import os

kb = KeyBindings()

send_message = queue.Queue()
send_lock = threading.Lock()

HOSTNAME = "p9cx.org"
PORT = 1111

def const_receive(recv_socket):
    pass

def network_main():
    while True:
        sleep(0.5)
        try:
            network = Network(HOSTNAME, PORT)
            network.tls_socket_creation()
            network.connect()

            while True:
                sleep(0.1)
                if not send_message.empty():  # if it's not empty, try to send the data
                    try:
                        with send_lock:
                            message = send_message.get()
                            network.socket_sendall(str(message))
                    except (socket.error, OSError):
                        break

        except socket.timeout:
            continue
        except Exception as err:
            print(err)

class Gui:
    def __init__(self):
        self.output_field = TextArea(style="class:output-field")
        self.input_field = TextArea(
            height=1,
            multiline=False,
            wrap_lines=False,
        )

        self.container = HSplit(
            [
                self.output_field,
                Window(height=1, char="-", style="class:line"),
                self.input_field,
            ]
        )

    def accept(self,buff):
        try:
            output = self.input_field.text
        except BaseException as e:
            output = f"\n\n{e}"

        new_text = self.output_field.text + output + "\n"

        with send_lock:
            send_message.put(new_text)

        self.output_field.buffer.document = Document(
            text=new_text
        )

    def main(self):
        self.input_field.accept_handler = self.accept

        @kb.add("c-c")
        @kb.add("c-q")
        def _(event):
            event.app.exit()
            os._exit(0)

            # Run application.
        application = Application(
            layout=Layout(self.container, focused_element=self.input_field),
            key_bindings=kb,
            mouse_support=True,
            full_screen=True,
        )

        application.run()

if __name__ == "__main__":
    obj = Gui()
    network_thread = threading.Thread(target=network_main)
    network_thread.start()
    obj.main()

