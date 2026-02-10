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

import dataclasses
import threading
import time

from textual.app import Screen
from textual.app import ComposeResult, App
from textual.widgets import Input, Log
from client_methods import *


class InputScreen(Screen):

    @dataclasses.dataclass
    class NVals:
        HOSTNAME: str
        PORT: int

    DFLNVals = NVals("p9cx.org", 1111)
    typed_message = []
    recevied_message = []
    recevied_message_lock = threading.Lock()
    typed_message_lock = threading.Lock()

    json_obj = JsonStoring("username.json")

    CSS = """Input {
                margin: 1 0;
                padding: 0 1;
                border: none;
                background: $surface;
                width: 40;
        }

            Input:focus {
                border: round;
                border: black;
                width: 80%;
            }"""

    def compose(self) -> ComposeResult:
        yield Log(id="history")
        yield Input(placeholder="lorem ipsum i forgot the rest", id="user_name")

    def on_input_submitted(self, event: Input.Submitted) -> None:

        with self.typed_message_lock:
            self.typed_message.append(event.value)

        event.input.value = ""

    def network_main(self):
        while True:
            time.sleep(0.1)
            try:

                network = Network(self.DFLNVals.HOSTNAME, self.DFLNVals.PORT)
                network.tls_socket_creation()
                network.connect()
                network.socket_sendall(f"{self.json_obj.get_name()}")

                receive_thread = threading.Thread(
                    target=self.recv_loop,
                    args=(network.socket,),
                ).start()

                while True:
                    time.sleep(0.1)
                    with self.typed_message_lock:
                        try:
                            if len(self.typed_message) != 0:
                                to_be_sent = self.typed_message.pop()
                                network.socket_sendall(to_be_sent)

                        except socket.timeout:
                            continue

                        except (socket.error, OSError):
                            receive_thread.join()
                            break

            except socket.timeout:
                continue

            except Exception:
                break

    def recv_loop(self, sock):

        message_history = b""
        while True:
            try:
                part = sock.recv(4096)
            except socket.timeout:
                break
            if not part:
                break
            message_history += part

            self.app.call_from_thread(
                self.query_one("#history").write, message_history.decode("utf8")
            )

        while True:
            try:
                data = sock.recv(4096)
                if not data:
                    break

                text = data.decode(errors="ignore")
                self.app.call_from_thread(
                    self.query_one("#history").write, text
                )

            except socket.timeout:
                continue
            except OSError:
                break

    def on_mount(self):
        self.query_one("#history")
        threading.Thread(target=self.network_main, daemon=True).start()

