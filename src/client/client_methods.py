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

import json
import os
import ssl
import socket

class JsonStoring:
    def __init__(self, file_name):
        self.file_name = file_name
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_name):
            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump({"name": None}, f)

    def get_name(self):
        with open(self.file_name, "r", encoding="utf-8") as file:
            contents = file.read()
            dict_data = json.loads(contents)
            name = dict_data["name"]
            return name
    def write_name(self,name):
        with open(self.file_name,"r+", encoding="utf-8") as file:
            contents = file.read()
            file.seek(0)
            file.truncate()
            dict_data = json.loads(contents)
            dict_data["name"] = name
            file.write(json.dumps(dict_data))

    def check_name(self):
        with open(self.file_name, "r", encoding="utf-8") as file:
            contents = file.read()
            dict_data = json.loads(contents)
            if dict_data["name"] is None:
                return False
            else:
                return True


class Network:
    def __init__(self, HOSTNAME, PORT):
        self.socket = None
        self.context = ssl.create_default_context()
        self.HOSTNAME = HOSTNAME
        self.PORT = PORT

    def tls_socket_creation(self):
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        tls_socket = self.context.wrap_socket(
           my_socket,
           server_hostname=self.HOSTNAME
        )
        self.socket = tls_socket

    def connect(self):
        if self.socket is None:
            self.tls_socket_creation()
        self.socket.connect((self.HOSTNAME, self.PORT))

    def socket_sendall(self, data): #pass this a non binary type please
        if self.socket is None:
            self.tls_socket_creation()

        self.socket.sendall(data.encode("utf-8"))

