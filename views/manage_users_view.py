from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class ManageUsersView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.selected_user_id = None
        self.setWindowTitle("Manage Users")
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

            QPushButton#deleteButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton#deleteButton:hover {
                background-color: #c0392b;
            }

            QPushButton#refreshButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton#refreshButton:hover {
                background-color: #2980b9;
            }

            QPushButton#backButton {
                background-color: #9aa5a8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton#backButton:hover {
                background-color: #7d878a;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 10px;
                gridline-color: #e6e6e6;
                color: #222;
                selection-background-color: #dbeafe;
                selection-color: #111;
            }

            QHeaderView::section {
                background-color: black;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_card = QFrame()
        main_card.setObjectName("mainCard")
        main_card.setFixedSize(900, 560)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(14)

        title = QLabel("Manage Users")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("View and manage student accounts")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setObjectName("refreshButton")
        refresh_btn.clicked.connect(self.controller.load_manage_users)

        delete_btn = QPushButton("Delete Selected User")
        delete_btn.setObjectName("deleteButton")
        delete_btn.clicked.connect(self.controller.delete_selected_user)

        button_row.addWidget(refresh_btn)
        button_row.addWidget(delete_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Full Name", "Email", "Address", "Contact"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellClicked.connect(self.select_row)

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_librarian_dashboard_from_users)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(button_row)
        layout.addWidget(self.table)
        layout.addWidget(back_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    def populate_table(self, students):
        self.table.setRowCount(len(students))
        self.selected_user_id = None

        for row, student in enumerate(students):
            full_name = f"{student['first_name']} {student['last_name']}"
            self.table.setItem(row, 0, QTableWidgetItem(str(student["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(full_name))
            self.table.setItem(row, 2, QTableWidgetItem(student["email"]))
            self.table.setItem(row, 3, QTableWidgetItem(student["address"] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(student["contact_no"] or ""))

    def select_row(self, row, column):
        self.selected_user_id = int(self.table.item(row, 0).text())

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)