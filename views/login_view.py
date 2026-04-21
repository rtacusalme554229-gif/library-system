from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class LoginView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("BookWise Login")
        self.setFixedSize(APP_WIDTH, APP_HEIGHT)
        self.setup_ui()
        center_window(self)

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f3f4f6;
                font-family: Arial;
                color: #222;
            }

            QFrame#mainCard {
                background-color: white;
                border: 1px solid #d9d9d9;
                border-radius: 22px;
            }

            QLabel#brandLabel {
                font-size: 30px;
                font-weight: bold;
                color: #111;
                background: transparent;
            }

            QLabel#titleLabel {
                font-size: 18px;
                font-weight: bold;
                color: #222;
                background: transparent;
            }

            QLabel#subtitleLabel {
                font-size: 12px;
                color: #666;
                background: transparent;
            }

            QLineEdit {
                padding: 12px;
                border: 1px solid #cfcfcf;
                border-radius: 10px;
                background: white;
                color: #222;
                font-size: 12px;
            }

            QPushButton#loginButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
            }

            QPushButton#loginButton:hover {
                background-color: #222;
            }

            QPushButton#registerButton {
                background-color: #f1f3f5;
                color: #222;
                border: 1px solid #d9d9d9;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
            }

            QPushButton#registerButton:hover {
                background-color: #e9ecef;
            }
        """)

        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_card = QFrame()
        main_card.setObjectName("mainCard")
        main_card.setFixedSize(430, 420)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(14)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        brand = QLabel("BookWise")
        brand.setObjectName("brandLabel")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Welcome Back")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Sign in to continue to your library system")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_btn = QPushButton("Login")
        login_btn.setObjectName("loginButton")
        login_btn.clicked.connect(self.controller.login)

        register_btn = QPushButton("Register as User")
        register_btn.setObjectName("registerButton")
        register_btn.clicked.connect(self.controller.open_register)

        layout.addWidget(brand)
        layout.addSpacing(4)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(12)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addSpacing(6)
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)