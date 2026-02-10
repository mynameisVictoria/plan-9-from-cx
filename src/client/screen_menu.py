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

from screen_chatroom import *
from screen_username import *
from screen_about import *

class Main(App):

    CSS = """
        Screen {
            align: center middle;
        }"""

    def on_mount(self) -> None:
        self.app.install_screen(Username, "username")
        self.app.install_screen(InputScreen, "chat")
        self.app.install_screen(AboutScreen, "about")
        self.install_screen(Menu(), "menu")
        self.push_screen("menu")

class Menu(Screen):

    currently_selected = 0

    BINDINGS = [
        ("[Tab]", "change", "Changes menu option",),
        ("ctrl+q", "quit", "Quit"),
        ("enter", "enter", "Selects menu option")
    ]

    options_dict = {
        "1": "Enter Chatroom",
        "2": "Change username",
        "3": "About",
    }

    def compose(self) -> ComposeResult:
        yield Label(self.options_dict["1"], id="l1")
        yield Label(self.options_dict["2"], id="l2")
        yield Label(self.options_dict["3"], id="l3")
        yield Footer()

    def on_key(self, event: events.Key) -> None:
        if event.key == "tab":
            self.currently_selected += 1
            if self.currently_selected > 3:
                self.currently_selected = 0

            else:
                for i in range(1,4):

                    label = self.query_one(f"#l{i}", Label)

                    if i == self.currently_selected:
                        label.update(f"> {self.options_dict[str(i)]}")
                    else:
                        label.update(self.options_dict[str(i)])

        elif event.key == "enter":
            if self.currently_selected == 1:
                self.app.pop_screen()
                self.app.push_screen("chat")
            elif self.currently_selected == 2:
                self.app.pop_screen()
                self.app.push_screen("username")
            elif self.currently_selected == 3:
                self.app.pop_screen()
                self.app.push_screen("about")

if __name__ == "__main__":
    app = Main()
    app.run()
