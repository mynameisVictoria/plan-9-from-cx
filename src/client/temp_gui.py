#  Copyright (C) <2026>  <mynameisVictoria> and <Victoria2048>
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

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QScrollArea, QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtGui import QIcon
from pathlib import Path
from time import sleep


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comms-Platform Client")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon(str(BASE_DIR / "icon.png")))
        self.send_button = QPushButton("Send")
        self.input_field = QLineEdit()


        self.initUI()
    

    def initUI(self): # Makes the UI and stuffs
        central = QWidget()
        main_layout = QVBoxLayout(central)

        self.message_display_area = QScrollArea() # Initializes the scrolling area
        self.message_display_area.setWidgetResizable(True)

        container_for_messages = QWidget()
        self.layout_for_messages = QVBoxLayout(container_for_messages) # Creates the layout for the widget in the scrolling area

        self.labels = []
        self.label_count = 0

        self.message_display_area.setWidget(container_for_messages) # Throws the actual message widgets into the scrollinator area
        main_layout.addWidget(self.message_display_area)

        input_section = QHBoxLayout() # Creates and adds the input section to the main layout
        input_section.addWidget(self.input_field)
        input_section.addWidget(self.send_button)   
        main_layout.addLayout(input_section)

        self.setCentralWidget(central) # Throws the main_layout onto the entire window

        self.message_display_area.verticalScrollBar().rangeChanged.connect(self.scroll_to_bottom) # Automatically scrolls to the bottom upon adding a message that changes FOV
        self.send_button.clicked.connect(self.send_message)

    def send_message(self):
        message = self.input_field.text() # THIS IS WHERE THE MESSAGE COMES OUT AS A STRING
        self.receive_message(message)
        self.input_field.clear()
        
    def receive_message(self, received_message:str):
        label = QLabel(received_message) # Sets up each messages formatting!
        label.setWordWrap(True)
        label.setMinimumHeight(50)
        label.setMaximumHeight(100)
        # Adds the label to the message area
        self.layout_for_messages.addWidget(label)
        self.labels.append(label)
        self.label_count += 1

    def scroll_to_bottom(self, _min=None, _max=None):
        self.message_display_area.verticalScrollBar().setValue(self.message_display_area.verticalScrollBar().maximum())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    main()
