from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window
import os


class LoginView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.password_visible = False

        self.setWindowTitle("BookWise Login")
        self.setFixedSize(APP_WIDTH, APP_HEIGHT)

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
                border: 1px solid #e5e7eb;
                border-radius: 30px;
            }

            QFrame#brandPanel {
                background-color: #0b1730;
                border-radius: 26px;
            }

            QFrame#logoOuter {
                background-color: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 28px;
            }

            QFrame#logoCard {
                background-color: white;
                border-radius: 22px;
                border: 1px solid #e5e7eb;
            }

            QLabel#logoImage {
                background: transparent;
            }

            QLabel#logoFallback {
                color: #0b1730;
                background-color: white;
                border-radius: 22px;
                font-size: 38px;
                font-weight: bold;
            }

            QLabel#brandBadge {
    color: #dbeafe;
    background-color: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 16px;
    padding: 8px 18px;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1px;
}

            QLabel#brandTitle {
                color: white;
                font-size: 42px;
                font-weight: bold;
                background: transparent;
            }

            QLabel#brandSubtitle {
                color: #d1d5db;
                font-size: 13px;
                line-height: 1.5;
                background: transparent;
            }

            QLabel#featureText {
                color: #f8fafc;
                font-size: 13px;
                line-height: 1.5;
                background: transparent;
            }

            QLabel#formTitle {
                color: #111827;
                font-size: 32px;
                font-weight: bold;
                background: transparent;
            }

            QLabel#formSubtitle {
                color: #6b7280;
                font-size: 13px;
                background: transparent;
            }

            QLabel#fieldLabel {
                color: #374151;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
            }

            QLineEdit {
                background-color: #f9fafb;
                border: 1px solid #d1d5db;
                border-radius: 12px;
                padding: 13px;
                font-size: 13px;
                color: #111827;
            }

            QLineEdit:focus {
                border: 1px solid #2563eb;
                background-color: white;
            }

            QPushButton#toggleButton {
                background-color: #f9fafb;
                border: 1px solid #d1d5db;
                border-radius: 12px;
                padding: 10px 14px;
                font-size: 12px;
                font-weight: bold;
                color: #374151;
            }

            QPushButton#toggleButton:hover {
                background-color: #eef2ff;
                border: 1px solid #2563eb;
                color: #1d4ed8;
            }

            QPushButton#loginButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 14px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#loginButton:hover {
                background-color: #1d4ed8;
            }

            QLabel#noteLabel {
                color: #6b7280;
                font-size: 11px;
                background: transparent;
            }
        """)

        root = QVBoxLayout()
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_card = QFrame()
        main_card.setObjectName("mainCard")
        main_card.setFixedSize(980, 600)

        main_layout = QHBoxLayout(main_card)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(22)

        # ================= LEFT BRAND PANEL =================
        brand_panel = QFrame()
        brand_panel.setObjectName("brandPanel")
        brand_panel.setFixedWidth(420)

        brand_layout = QVBoxLayout(brand_panel)
        brand_layout.setContentsMargins(28, 28, 28, 28)
        brand_layout.setSpacing(14)
        brand_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # OUTER SOFT FRAME
        logo_outer = QFrame()
        logo_outer.setObjectName("logoOuter")
        logo_outer.setFixedSize(260, 190)

        logo_outer_layout = QVBoxLayout(logo_outer)
        logo_outer_layout.setContentsMargins(18, 18, 18, 18)
        logo_outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # INNER WHITE CARD
        logo_card = QFrame()
        logo_card.setObjectName("logoCard")
        logo_card.setFixedSize(220, 140)

        logo_card_layout = QVBoxLayout(logo_card)
        logo_card_layout.setContentsMargins(10, 10, 10, 10)
        logo_card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_path = os.path.join("assets", "logo.png")

        if os.path.exists(logo_path):
            logo = QLabel()
            logo.setObjectName("logoImage")
            logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

            pixmap = QPixmap(logo_path)
            pixmap = pixmap.scaled(
                190,
                110,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            logo.setPixmap(pixmap)
            logo.setFixedSize(195, 115)
        else:
            logo = QLabel("BW")
            logo.setObjectName("logoFallback")
            logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo.setFixedSize(120, 90)

        logo_card_layout.addWidget(logo)
        logo_outer_layout.addWidget(logo_card)

        badge = QLabel("LIBRARY MANAGEMENT SYSTEM")
        badge.setObjectName("brandBadge")
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setFixedWidth(285)

        brand_title = QLabel("BookWise")
        brand_title.setObjectName("brandTitle")
        brand_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        brand_subtitle = QLabel(
            "Manage books, users, borrowing records, returns, penalties, copies, and reports in one organized system."
        )
        brand_subtitle.setObjectName("brandSubtitle")
        brand_subtitle.setWordWrap(True)
        brand_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        feature_1 = QLabel("✓ Role-based access for Admin, Librarian, and User")
        feature_1.setObjectName("featureText")

        feature_2 = QLabel("✓ Borrow and return tracking with due dates")
        feature_2.setObjectName("featureText")

        feature_3 = QLabel("✓ Copy monitoring with lost and damaged condition")
        feature_3.setObjectName("featureText")

        feature_4 = QLabel("✓ PDF reports for library records")
        feature_4.setObjectName("featureText")

        brand_layout.addWidget(logo_outer, alignment=Qt.AlignmentFlag.AlignHCenter)
        brand_layout.addSpacing(6)
        brand_layout.addWidget(badge, alignment=Qt.AlignmentFlag.AlignHCenter)
        brand_layout.addSpacing(10)
        brand_layout.addWidget(brand_title)
        brand_layout.addWidget(brand_subtitle)
        brand_layout.addSpacing(18)
        brand_layout.addWidget(feature_1)
        brand_layout.addWidget(feature_2)
        brand_layout.addWidget(feature_3)
        brand_layout.addWidget(feature_4)
        brand_layout.addStretch()

        # ================= RIGHT FORM PANEL =================
        form_panel = QFrame()

        form_layout = QVBoxLayout(form_panel)
        form_layout.setContentsMargins(24, 40, 24, 40)
        form_layout.setSpacing(12)

        form_title = QLabel("Welcome Back")
        form_title.setObjectName("formTitle")

        form_subtitle = QLabel("Login to continue to your BookWise dashboard.")
        form_subtitle.setObjectName("formSubtitle")

        email_label = QLabel("Email Address")
        email_label.setObjectName("fieldLabel")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email address")

        password_label = QLabel("Password")
        password_label.setObjectName("fieldLabel")

        password_row = QHBoxLayout()
        password_row.setSpacing(8)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.toggle_btn = QPushButton("Show")
        self.toggle_btn.setObjectName("toggleButton")
        self.toggle_btn.setFixedWidth(78)
        self.toggle_btn.clicked.connect(self.toggle_password)

        password_row.addWidget(self.password_input)
        password_row.addWidget(self.toggle_btn)

        login_btn = QPushButton("Login")
        login_btn.setObjectName("loginButton")
        login_btn.clicked.connect(self.controller.login)

        note = QLabel("Access is managed by authorized administrators and librarians only.")
        note.setObjectName("noteLabel")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setWordWrap(True)

        form_layout.addStretch()
        form_layout.addWidget(form_title)
        form_layout.addWidget(form_subtitle)
        form_layout.addSpacing(22)
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(password_label)
        form_layout.addLayout(password_row)
        form_layout.addSpacing(12)
        form_layout.addWidget(login_btn)
        form_layout.addSpacing(10)
        form_layout.addWidget(note)
        form_layout.addStretch()

        main_layout.addWidget(brand_panel)
        main_layout.addWidget(form_panel)

        root.addWidget(main_card)
        self.setLayout(root)

    def toggle_password(self):
        self.password_visible = not self.password_visible

        if self.password_visible:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText("Show")

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)