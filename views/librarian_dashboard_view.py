from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton,
    QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class LibrarianDashboardView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Librarian Dashboard")
        self.setFixedSize(APP_WIDTH, APP_HEIGHT)
        self.setup_ui()
        center_window(self)

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f3f4f6;
                font-family: Arial;
            }

            QFrame#mainCard {
                background-color: white;
                border: 1px solid #d9d9d9;
                border-radius: 20px;
            }

            QLabel#titleLabel {
                font-size: 28px;
                font-weight: bold;
                color: #222;
                background: transparent;
            }

            QLabel#subtitleLabel {
                font-size: 13px;
                color: #666;
                background: transparent;
            }

            QFrame#actionCard {
                background-color: #f9f9f9;
                border: 1px solid #dddddd;
                border-radius: 12px;
            }

            QLabel#cardDesc {
                font-size: 11px;
                color: #777;
                background: transparent;
            }

            QPushButton#logoutButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
            }

            QPushButton#logoutButton:hover {
                background-color: #222;
            }
        """)

        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_card = QFrame()
        main_card.setObjectName("mainCard")
        main_card.setFixedSize(820, 430)

        main_layout = QVBoxLayout(main_card)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(18)

        title = QLabel("BookWise")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Welcome back, Librarian!")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        row1 = QHBoxLayout()
        row1.setSpacing(20)

        create_user_card = self.create_card(
            "Create User Account",
            "Register a new student account",
            self.controller.open_create_user_account
        )

        manage_books_card = self.create_card(
            "Manage Books",
            "Add, update, delete, and view books",
            self.controller.open_manage_books
        )

        row1.addWidget(create_user_card)
        row1.addWidget(manage_books_card)

        row2 = QHBoxLayout()
        row2.setSpacing(20)

        manage_users_card = self.create_card(
            "Manage Users",
            "View and manage student accounts",
            self.controller.open_manage_users
        )

        borrow_return_card = self.create_card(
            "Borrow / Return Books",
            "Process borrowed and returned books",
            self.controller.open_borrow_return
        )

        row2.addWidget(manage_users_card)
        row2.addWidget(borrow_return_card)

        search_books_card = self.create_card(
            "Search Books",
            "Search available and borrowed books",
            self.controller.open_search_books
        )

        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("logoutButton")
        logout_btn.clicked.connect(self.controller.logout)
        logout_btn.setFixedHeight(40)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addLayout(row1)
        main_layout.addLayout(row2)
        main_layout.addWidget(search_books_card)
        main_layout.addWidget(logout_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    def create_card(self, title_text, desc_text, callback):
        card = QFrame()
        card.setObjectName("actionCard")
        card.setFixedHeight(95)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        title_btn = QPushButton(title_text)
        title_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                text-align: left;
                font-size: 15px;
                font-weight: bold;
                color: #222;
                padding: 0;
            }
            QPushButton:hover {
                color: #0078d7;
            }
        """)
        title_btn.clicked.connect(callback)

        desc = QLabel(desc_text)
        desc.setObjectName("cardDesc")
        desc.setWordWrap(True)

        layout.addWidget(title_btn)
        layout.addWidget(desc)

        return card