from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class RegisterView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("BookWise Registration")
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
                font-size: 28px;
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

            QPushButton#registerButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
            }

            QPushButton#registerButton:hover {
                background-color: #222;
            }

            QPushButton#backButton {
                background-color: #f1f3f5;
                color: #222;
                border: 1px solid #d9d9d9;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
            }

            QPushButton#backButton:hover {
                background-color: #e9ecef;
            }
        """)

        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_card = QFrame()
        main_card.setObjectName("mainCard")
        main_card.setFixedSize(460, 620)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(12)

        brand = QLabel("BookWise")
        brand.setObjectName("brandLabel")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("User Registration")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Create your account to access the library system")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Home Address")

        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Contact Number")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        register_btn = QPushButton("Create Account")
        register_btn.setObjectName("registerButton")
        register_btn.clicked.connect(self.controller.register_student)

        back_btn = QPushButton("Back to Login")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_login)

        layout.addWidget(brand)
        layout.addSpacing(2)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.address_input)
        layout.addWidget(self.contact_input)
        layout.addWidget(self.password_input)
        layout.addSpacing(8)
        layout.addWidget(register_btn)
        layout.addWidget(back_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)