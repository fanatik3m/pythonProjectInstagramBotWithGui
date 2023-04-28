import datetime
import sys
from pathlib import Path
from typing import List

import multiprocessing
import threading

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QPushButton, QWidget, QVBoxLayout, QLabel, QCheckBox,
    QFileDialog
)

from main import InstagramBot, log_in_set_likes


def main_logic(post_urls, username, password, is_multiprocessing):
    if len(post_urls) == 1:
        bot = InstagramBot(username, password)
        bot.log_in()
        bot.set_like(post_urls[0])
        bot.close()

    if is_multiprocessing:
        start_time = datetime.datetime.now()
        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            pool.map(log_in_set_likes, post_urls)
        print(f'Total time is {datetime.datetime.now() - start_time}')
    else:
        start_time = datetime.datetime.now()
        bot = InstagramBot(username, password)
        bot.log_in()
        for url in post_urls:
            bot.set_like(url)
        bot.close()
        print(f'Total time is {datetime.datetime.now() - start_time}')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.username: str = ''
        self.password: str = ''

        self.post_urls: List = []

        self.is_agree: bool = False
        self.is_multiprocessing: bool = False

        self.setWindowTitle('Instagram Bot GUI tool')

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('your username...')
        self.username_input.textChanged.connect(self.get_username)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('your password...')
        self.password_input.textChanged.connect(self.get_password)

        self.agree_label = QLabel('I agree with using my date in logging https://www.instagram.com/\n')

        self.agree_checkbox = QCheckBox()
        self.agree_checkbox.stateChanged.connect(self.check_agree)

        self.post_urls_label = QLabel('\nEnter post urls')

        self.post_urls_input = QLineEdit()
        self.post_urls_input.setPlaceholderText('Enter url of post which you want to set like...')

        self.clear_button = QPushButton('+')
        self.clear_button.clicked.connect(self.save_clear)

        self.start_button = QPushButton('Start working')
        self.start_button.clicked.connect(self.start_working)

        self.filename_edit = QLabel('\nYour path to read urls (optionally)')

        self.browse_button = QPushButton('Browse urls')
        self.browse_button.clicked.connect(self.browse_from_file)

        self.is_multiprocessing_label = QLabel('Should use multiprocessing?')

        self.check_multiprocessing = QCheckBox()
        self.check_multiprocessing.stateChanged.connect(self.change_multiprocessing)

        self.file_dialog = QFileDialog(self)

        self.layout = QVBoxLayout()
        self.widgets = (
            self.username_input,
            self.password_input,
            self.agree_checkbox,
            self.agree_label,
            self.is_multiprocessing_label,
            self.check_multiprocessing,
            self.post_urls_label,
            self.post_urls_input,
            self.clear_button,
            self.filename_edit,
            self.browse_button,
            self.start_button
        )

        for widget in self.widgets:
            self.layout.addWidget(widget)

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

    def get_username(self, text: str) -> None:
        self.username = text

    def get_password(self, text: str) -> None:
        self.password = text

    def check_agree(self, status) -> None:
        print(status)
        self.is_agree = bool(status)

    def save_clear(self) -> None:
        text = self.post_urls_input.text()
        if text == '':
            return

        self.post_urls.append(text)
        self.post_urls_input.clear()

    def change_multiprocessing(self, status) -> None:
        self.is_multiprocessing = bool(status)

    def start_working(self) -> None:
        _args = (self.post_urls, self.username, self.password, self.is_multiprocessing)
        threading.Thread(target=main_logic, args=_args, name='webdriver-thread', daemon=True).start()

    def browse_from_file(self) -> None:
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            ".",
            "Text files (*.txt)"
        )
        if filename:
            path = Path(filename)
            self.filename_edit.setText(str(path))

            with open(path, 'r') as file:
                lines = [i.strip() for i in file.readlines()]
                for line in lines:
                    self.post_urls.append(line)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

if __name__ == '__main__':
    app.exec()