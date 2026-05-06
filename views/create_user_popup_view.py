from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QMessageBox, QFormLayout
)
from PyQt6.QtCore import Qt
from utils.helpers import center_window


class CreateUserPopupView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Create User")
        self.setFixedSize(460, 520)
        self.setup_ui()
        center_window(self)

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f3f4f6;
                font-family: Arial;
                color: #111827;
            }

            QFrame#mainCard {
                background-color: white;
                border: 1px solid #d9d9d9;
                border-radius: 20px;
            }

            QLabel#titleLabel {
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            }

            QLabel#subtitleLabel {
                font-size: 12px;
                color: #6b7280;
                background: transparent;
            }

            QLineEdit {
                padding: 11px;
                border: 1px solid #d1d5db;
                border-radius: 9px;
                background: white;
                color: #222;
            }

            QPushButton#saveButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 9px;
                padding: 11px;
                font-weight: bold;
            }

            QPushButton#closeButton {
                background-color: #9aa5a8;
                color: white;
                border: none;
                border-radius: 9px;
                padding: 11px;
                font-weight: bold;
            }
        """)

        root = QVBoxLayout()
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("mainCard")
        card.setFixedSize(400, 460)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)

        title = QLabel("Create User")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Register a new library user account")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form = QFormLayout()
        form.setSpacing(10)

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First name")

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Address")

        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Contact number")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form.addRow("First Name:", self.first_name_input)
        form.addRow("Last Name:", self.last_name_input)
        form.addRow("Email:", self.email_input)
        form.addRow("Address:", self.address_input)
        form.addRow("Contact No:", self.contact_input)
        form.addRow("Password:", self.password_input)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)

        save_btn = QPushButton("Create User")
        save_btn.setObjectName("saveButton")
        save_btn.clicked.connect(self.controller.save_student_from_librarian)

        close_btn = QPushButton("Cancel")
        close_btn.setObjectName("closeButton")
        close_btn.clicked.connect(self.close)

        button_row.addWidget(save_btn)
        button_row.addWidget(close_btn)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(form)
        layout.addStretch()
        layout.addLayout(button_row)

        root.addWidget(card)
        self.setLayout(root)

    def clear_form(self):
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.contact_input.clear()
        self.password_input.clear()

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)