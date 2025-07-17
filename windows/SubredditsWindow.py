import requests
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidget, QAbstractItemView, \
    QListWidgetItem, QMessageBox, QLineEdit


class SubredditsWindow(QWidget):
    def __init__(self, reddit):
        super().__init__()

        self.login_window = None
        self.reddit = reddit

        self.setWindowTitle('Subreddit Manager')
        self.setWindowIcon(QIcon('resources/Reddit_logo.png'))
        self.resize(400, 600)

        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()

        profile_pic_url = reddit.user.me().icon_img
        response = requests.get(profile_pic_url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        pixmap = pixmap.scaled(32, 32)

        profile_pic_label = QLabel()
        profile_pic_label.setPixmap(pixmap)
        header_layout.addWidget(profile_pic_label)

        username_label = QLabel(reddit.user.me().name)
        header_layout.addWidget(username_label)

        header_layout.addStretch()

        logout_button = QPushButton('Logout')
        logout_button.clicked.connect(self.logout_action)
        header_layout.addWidget(logout_button)

        main_layout.addLayout(header_layout)

        filter_layout = QHBoxLayout()

        filter_label = QLabel("Filter Subreddits:")
        filter_layout.addWidget(filter_label)
        self.filter_text = QLineEdit()
        self.filter_text.setPlaceholderText("Type to filter...")
        self.filter_text.textChanged.connect(self.filter_subreddits)
        filter_layout.addWidget(self.filter_text)

        main_layout.addLayout(filter_layout)

        self.subreddits = sorted(reddit.user.subreddits(limit=None),
                                 key=lambda subreddit: subreddit.display_name.lower())

        self.subreddit_list_widget = QListWidget()
        for subreddit in self.subreddits:
            name = "r/" + subreddit.display_name
            icon_url = subreddit.icon_img or subreddit.community_icon
            if icon_url:
                response = requests.get(icon_url)
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                pixmap = pixmap.scaled(24, 24)
                icon = QIcon(pixmap)
            else:
                pixmap = QPixmap()
                pixmap.load("resources/default_icon.png")
                pixmap = pixmap.scaled(24, 24)
                icon = QIcon(pixmap)

            item = QListWidgetItem(icon, name)
            self.subreddit_list_widget.addItem(item)

        self.subreddit_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        main_layout.addWidget(self.subreddit_list_widget)

        button_layout = QHBoxLayout()
        unsubscribe_button = QPushButton('Unsubscribe')
        unsubscribe_button.clicked.connect(self.unsubscribe)
        button_layout.addWidget(unsubscribe_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def logout_action(self):
        from windows.LoginWindow import LoginWindow
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

    def filter_subreddits(self):
        filter_text = self.filter_text.text().lower()
        for i in range(self.subreddit_list_widget.count()):
            item = self.subreddit_list_widget.item(i)
            item.setHidden(filter_text not in item.text().lower())

    def unsubscribe(self):
        selected_items = self.subreddit_list_widget.selectedItems()
        if not selected_items:
            no_subreddit_selected_popup = QMessageBox(self)
            no_subreddit_selected_popup.setIcon(QMessageBox.Icon.Information)
            no_subreddit_selected_popup.setWindowTitle("No Selection")
            no_subreddit_selected_popup.setText("No Subreddit selected")
            no_subreddit_selected_popup.setStandardButtons(QMessageBox.StandardButton.Ok)
            no_subreddit_selected_popup.exec()
            return

        unsubscribing_popup = QMessageBox(self)
        unsubscribing_popup.setIcon(QMessageBox.Icon.Information)
        unsubscribing_popup.setWindowTitle("Processing")
        unsubscribing_popup.setText("Unsubscribing from selected subreddits...")
        unsubscribing_popup.setStandardButtons(QMessageBox.StandardButton.Cancel)  # TODO: Cancel the action
        unsubscribing_popup.exec()

        for item in selected_items:
            subreddit_name = item.text().replace("r/", "")
            subreddit = self.reddit.subreddit(subreddit_name)
            subreddit.unsubscribe()
            row = self.subreddit_list_widget.row(item)
            self.subreddit_list_widget.takeItem(row)

        unsubscribing_popup.destroy()
