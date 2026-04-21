from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class EditProfileView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Edit Profile")
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
                font-size: 24px;
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
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background: white;
                color: #222;
            }

            QPushButton#saveButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
            }

            QPushButton#saveButton:hover {
                background-color: #222;
            }

            QPushButton#backButton {
                background-color: #9aa5a8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
            }

            QPushButton#backButton:hover {
                background-color: #7d878a;
            }
        """)

        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_card = QFrame()
        main_card.setObjectName("mainCard")
        main_card.setFixedSize(520, 580)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(14)

        title = QLabel("Edit Profile")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Update your student profile information")
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

        save_btn = QPushButton("Save Changes")
        save_btn.setObjectName("saveButton")
        save_btn.clicked.connect(self.controller.save_student_profile)

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_student_dashboard_from_edit_profile)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.address_input)
        layout.addWidget(self.contact_input)
        layout.addWidget(self.password_input)
        layout.addSpacing(10)
        layout.addWidget(save_btn)
        layout.addWidget(back_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    def load_data(self, user, student):
        self.first_name_input.setText(user["first_name"])
        self.last_name_input.setText(user["last_name"])
        self.email_input.setText(user["email"])
        self.address_input.setText(user["address"] or "")
        self.contact_input.setText(student["contact_no"] if student else "")
        self.password_input.setText(user["password"])

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)