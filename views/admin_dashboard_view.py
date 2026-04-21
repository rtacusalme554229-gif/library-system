from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class AdminDashboardView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Admin Dashboard")
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

            QLabel#titleLabel {
                font-size: 28px;
                font-weight: bold;
                color: #111;
                background: transparent;
            }

            QLabel#subtitleLabel {
                font-size: 13px;
                color: #666;
                background: transparent;
            }

            QFrame#statBlue {
                background-color: #3b82f6;
                border-radius: 16px;
            }

            QFrame#statGreen {
                background-color: #22c55e;
                border-radius: 16px;
            }

            QFrame#statOrange {
                background-color: #f59e0b;
                border-radius: 16px;
            }

            QFrame#statDark {
                background-color: #111827;
                border-radius: 16px;
            }

            QLabel#statTitle {
                color: white;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
            }

            QLabel#statValue {
                color: white;
                font-size: 26px;
                font-weight: bold;
                background: transparent;
            }

            QPushButton#actionButton {
                background-color: #fafafa;
                border: 1px solid #d9d9d9;
                border-radius: 14px;
                text-align: left;
                padding: 16px;
                color: #111;
            }

            QPushButton#actionButton:hover {
                background-color: #f4f4f4;
                border: 1px solid #cfcfcf;
            }

            QLabel#cardTitle {
                font-size: 15px;
                font-weight: bold;
                color: #111;
                background: transparent;
            }

            QLabel#cardDesc {
                font-size: 12px;
                color: #777;
                background: transparent;
            }

            QPushButton#logoutButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 14px;
                font-size: 13px;
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
        main_card.setFixedSize(900, 620)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(14)

        title = QLabel("BookWise")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Welcome back, Administrator!")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== Stat cards =====
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)

        self.books_card = self.create_stat_card("statBlue", "Total Books", "0")
        self.available_card = self.create_stat_card("statGreen", "Available Books", "0")
        self.borrowed_card = self.create_stat_card("statOrange", "Borrowed Books", "0")
        self.members_card = self.create_stat_card("statDark", "Total Members", "0")

        stats_row.addWidget(self.books_card)
        stats_row.addWidget(self.available_card)
        stats_row.addWidget(self.borrowed_card)
        stats_row.addWidget(self.members_card)

        # ===== Action cards =====
        row1 = QHBoxLayout()
        row1.setSpacing(14)

        create_librarian_btn = self.create_action_button(
            "Create Librarian",
            "Add a new librarian account",
            self.controller.open_create_librarian
        )

        manage_users_btn = self.create_action_button(
            "Manage Users",
            "View and manage librarians and users",
            self.controller.open_manage_members
        )

        row1.addWidget(create_librarian_btn)
        row1.addWidget(manage_users_btn)

        row2 = QHBoxLayout()
        row2.setSpacing(14)

        reports_btn = self.create_action_button(
            "View Reports",
            "Analyze library data and export reports",
            self.controller.open_reports
        )

        inventory_btn = self.create_action_button(
            "Inventory Books",
            "View and monitor all books in the library",
            self.controller.open_admin_inventory
        )

        row2.addWidget(reports_btn)
        row2.addWidget(inventory_btn)

        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("logoutButton")
        logout_btn.clicked.connect(self.controller.logout)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(stats_row)
        layout.addSpacing(6)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addStretch()
        layout.addWidget(logout_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    def create_stat_card(self, object_name, title_text, value_text):
        card = QFrame()
        card.setObjectName(object_name)
        card.setFixedHeight(90)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        title = QLabel(title_text)
        title.setObjectName("statTitle")

        value = QLabel(value_text)
        value.setObjectName("statValue")

        layout.addWidget(title)
        layout.addWidget(value)

        card.value_label = value
        return card

    def create_action_button(self, title_text, desc_text, callback):
        button = QPushButton()
        button.setObjectName("actionButton")
        button.setFixedHeight(100)
        button.clicked.connect(callback)

        content_layout = QVBoxLayout(button)
        content_layout.setContentsMargins(16, 14, 16, 14)
        content_layout.setSpacing(8)

        title = QLabel(title_text)
        title.setObjectName("cardTitle")

        desc = QLabel(desc_text)
        desc.setObjectName("cardDesc")
        desc.setWordWrap(True)

        content_layout.addWidget(title)
        content_layout.addWidget(desc)
        content_layout.addStretch()

        return button

    def set_stats(self, total_books, available_books, borrowed_books, total_members):
        self.books_card.value_label.setText(str(total_books))
        self.available_card.value_label.setText(str(available_books))
        self.borrowed_card.value_label.setText(str(borrowed_books))
        self.members_card.value_label.setText(str(total_members))