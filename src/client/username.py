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


from textual import events
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Input, Label
from client_funcs import JsonStoring


class Username(Screen):

    json_obj = JsonStoring("username.json")

    CSS = """
        Screen {
            align: center middle;
        }
        Input:focus {
        border: round;
        border: black;
        width: 80%;
    }  
        """

    enter_counter = 0
    username = ""

    def compose(self) -> ComposeResult:
        yield Label("Hit Tab to return to main menu :3", id="main_menu")
        yield Label("Confirm", id="confirm")
        yield Label(f"{self.json_obj.get_name()}", id="username_field")
        yield Input(placeholder="Max 24 characters long", id="input")


    def on_input_submitted(self, event: Input.Submitted) -> None:
        label = self.query_one("#username_field", Label)
        label.update(event.value)
        self.username = event.value

    def on_key(self, event: events.Key) -> None:
        label = self.query_one("#confirm", Label)
        if event.key == "enter":
            self.enter_counter += 1
            if self.enter_counter == 1:
                label.update("Are you sure?")
            elif self.enter_counter == 2:
                if self.username == "":
                    label.update("Invalid username")
                    self.enter_counter = 0

                label.update("Okay")
                self.json_obj.write_name(self.username)
                self.enter_counter = 0

        elif event.key == "tab":
            self.app.pop_screen()
            self.app.push_screen("menu")
