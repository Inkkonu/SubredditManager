import sys

import praw
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from prawcore import ResponseException


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.subreddits_window = None

        self.setWindowTitle('Subreddit Manager')
        self.setWindowIcon(QIcon('resources/Reddit_logo.png'))
        self.resize(400, 200)

        main_layout = QVBoxLayout()

        label = QLabel("Subreddit Manager")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        label.setFont(font)
        main_layout.addWidget(label)

        form_layout = QVBoxLayout()

        self.client_id_text_field = self.add_text_field_with_label("Client ID :", "Client ID", form_layout)
        self.client_secret_text_field = self.add_text_field_with_label("Client Secret :", "Client Secret", form_layout,
                                                                       echo_mode=QLineEdit.EchoMode.Password)
        self.user_agent_text_field = self.add_text_field_with_label("User Agent :", "User Agent", form_layout)
        self.username_text_field = self.add_text_field_with_label("Username :", "Username", form_layout)
        self.password_text_field = self.add_text_field_with_label("Password :", "Password", form_layout,
                                                                  echo_mode=QLineEdit.EchoMode.Password)

        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        submit_button = QPushButton("Login", self)
        submit_button.clicked.connect(self.login_action)
        button_layout.addWidget(submit_button)

        cancel_button = QPushButton("Quit", self)
        cancel_button.clicked.connect(self.quit_action)
        button_layout.addWidget(cancel_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def login_action(self):
        if not all([self.client_id_text_field.text(), self.client_secret_text_field.text(),
                    self.user_agent_text_field.text(), self.username_text_field.text(),
                    self.password_text_field.text()]):
            missing_credentials_popup = QMessageBox(self)
            missing_credentials_popup.setWindowTitle("Error")
            missing_credentials_popup.setText("Please fill out all the fields")
            missing_credentials_popup.setIcon(QMessageBox.Icon.Critical)
            missing_credentials_popup.setStandardButtons(QMessageBox.StandardButton.Ok)
            missing_credentials_popup.exec()
            return

        connecting_popup = QMessageBox(self)
        connecting_popup.setWindowTitle("Connecting")
        connecting_popup.setText("Connecting to Reddit...")
        connecting_popup.setIcon(QMessageBox.Icon.Information)
        connecting_popup.setStandardButtons(QMessageBox.StandardButton.Cancel)  # TODO: Cancel the action
        connecting_popup.exec()

        reddit = praw.Reddit(client_id=self.client_id_text_field.text(),
                             client_secret=self.client_secret_text_field.text(),
                             user_agent=self.user_agent_text_field.text(), username=self.username_text_field.text(),
                             password=self.password_text_field.text())

        try:
            reddit.user.me()
        except ResponseException as e:
            connecting_popup.destroy()
            failed_login_popup = QMessageBox(self)
            failed_login_popup.setWindowTitle("Error")
            failed_login_popup.setText("Couldn't connect to Reddit, check the fields are correct\nError : " + str(e))
            failed_login_popup.setIcon(QMessageBox.Icon.Critical)
            failed_login_popup.setStandardButtons(QMessageBox.StandardButton.Ok)
            failed_login_popup.exec()
            return

        connecting_popup.destroy()

        from windows.SubredditsWindow import SubredditsWindow
        self.close()
        self.subreddits_window = SubredditsWindow(reddit)
        self.subreddits_window.show()

    @staticmethod
    def quit_action():
        sys.exit()

    def add_text_field_with_label(self, label: str, placeholder: str, layout: QVBoxLayout,
                                  echo_mode: QLineEdit.EchoMode = QLineEdit.EchoMode.Normal) -> QLineEdit:
        horizontal_layout = QHBoxLayout()

        label = QLabel(label)
        horizontal_layout.addWidget(label)

        text_field = QLineEdit(self)
        text_field.setPlaceholderText(placeholder)
        text_field.setEchoMode(echo_mode)
        horizontal_layout.addWidget(text_field)

        layout.addLayout(horizontal_layout)

        return text_field
