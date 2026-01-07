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
from time import sleep
from datetime import datetime, timezone
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

class GeneralIO:
    def __init__(self):
        pass
    @staticmethod
    def get_input():
        while True:
            sleep(0.1)
            send_info_input = input("")
            if not send_info_input.strip() == "":
                return send_info_input

    @staticmethod
    def format_message(username, message):
        timestamp = datetime.now(timezone.utc).strftime('%H:%M:%S')
        return f"[{timestamp} ] | {username}: {message}"

class Commands:
    def __init__(self, given_command, json_obj):
        self.given_command = given_command
        self.json_obj = json_obj

    def check_command(self):
        if self.given_command == "/help":
            self.help()
        elif self.given_command == "/name":
            self.change_name()
        elif self.given_command == "/exit":
            os._exit(0)
        else:
            return False

    def change_name(self):
        new_name = input("Enter new name: ")
        self.json_obj.write_name(new_name)

    @staticmethod
    def help():
        print(f"  Do /name to change you name, it will prompt you afterwards\n "
              f"Do /exit to exit \n "
              f"Do /online to check how many people are online \n ")

class Network:
    def __init__(self, HOSTNAME, PORT):
        self.socket = None
        self.context = ssl.create_default_context()
        self.HOSTNAME = HOSTNAME
        self.PORT = PORT

    def tls_socket_creation(self):
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.settimeout(0.5)

        tls_socket = self.context.wrap_socket(
            my_socket,
            server_hostname=self.HOSTNAME
        )
        self.socket = tls_socket

    def connect(self):
        if self.socket is None:
            self.tls_socket_creation()
        else:
            self.socket.connect((self.HOSTNAME, self.PORT))

    def socket_sendall(self, data): #pass this a non binary type please
        if self.socket is None:
            self.tls_socket_creation()
        else:
            self.socket.sendall(data.encode("utf-8"))

