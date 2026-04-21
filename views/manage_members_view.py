from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QLineEdit, QFormLayout
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class ManageMembersView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.selected_user_id = None
        self.current_role = "librarian"

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

            QPushButton#tabButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }

            QPushButton#tabButton:hover {
                background-color: #222;
            }

            QPushButton#editButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }

            QPushButton#editButton:hover {
                background-color: #2980b9;
            }

            QPushButton#deleteButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }

            QPushButton#deleteButton:hover {
                background-color: #c0392b;
            }

            QPushButton#backButton {
                background-color: #9aa5a8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }

            QPushButton#backButton:hover {
                background-color: #7d878a;
            }

            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background: white;
                color: #222;
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
        main_card.setFixedSize(900, 620)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(14)

        title = QLabel("Manage Library Members")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("View students and manage librarian accounts")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        self.librarian_btn = QPushButton("Librarians")
        self.librarian_btn.setObjectName("tabButton")
        self.librarian_btn.clicked.connect(lambda: self.controller.load_members("librarian"))

        self.student_btn = QPushButton("Students")
        self.student_btn.setObjectName("tabButton")
        self.student_btn.clicked.connect(lambda: self.controller.load_members("student"))

        top_row.addWidget(self.librarian_btn)
        top_row.addWidget(self.student_btn)
        top_row.addStretch()

        self.role_label = QLabel("Showing: Librarians")
        self.role_label.setStyleSheet("font-size: 12px; color: #444; background: transparent;")

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Full Name", "Email", "Address", "Role"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellClicked.connect(self.select_row)

        self.edit_form = QFrame()
        self.edit_form.setStyleSheet("QFrame { background: #fafafa; border: 1px solid #e3e3e3; border-radius: 12px; }")
        form_layout = QFormLayout(self.edit_form)

        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()

        form_layout.addRow("First Name:", self.first_name_input)
        form_layout.addRow("Last Name:", self.last_name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Address:", self.address_input)

        action_row = QHBoxLayout()
        action_row.setSpacing(10)

        self.edit_btn = QPushButton("Update Librarian")
        self.edit_btn.setObjectName("editButton")
        self.edit_btn.clicked.connect(self.controller.edit_librarian)

        self.delete_btn = QPushButton("Delete Librarian")
        self.delete_btn.setObjectName("deleteButton")
        self.delete_btn.clicked.connect(self.controller.delete_librarian)

        action_row.addWidget(self.edit_btn)
        action_row.addWidget(self.delete_btn)
        action_row.addStretch()

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_admin_dashboard_from_members)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(top_row)
        layout.addWidget(self.role_label)
        layout.addWidget(self.table)
        layout.addWidget(self.edit_form)
        layout.addLayout(action_row)
        layout.addWidget(back_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

        self.toggle_librarian_tools(True)

    def toggle_librarian_tools(self, visible):
        self.edit_form.setVisible(visible)
        self.edit_btn.setVisible(visible)
        self.delete_btn.setVisible(visible)

    def populate_table(self, users, role_name):
        self.current_role = role_name
        self.role_label.setText(f"Showing: {role_name.capitalize()}s")
        self.table.clearContents()
        self.table.setRowCount(len(users))
        self.selected_user_id = None

        self.first_name_input.clear()
        self.last_name_input.clear()
        self.email_input.clear()
        self.address_input.clear()

        self.toggle_librarian_tools(role_name == "librarian")

        for row, user in enumerate(users):
            full_name = f"{user['first_name']} {user['last_name']}"
            self.table.setItem(row, 0, QTableWidgetItem(str(user["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(full_name))
            self.table.setItem(row, 2, QTableWidgetItem(user["email"]))
            self.table.setItem(row, 3, QTableWidgetItem(user["address"] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(user["role"]))

    def select_row(self, row, col):
        self.selected_user_id = int(self.table.item(row, 0).text())

        if self.current_role == "librarian":
            full_name = self.table.item(row, 1).text().split(" ", 1)
            first_name = full_name[0]
            last_name = full_name[1] if len(full_name) > 1 else ""

            self.first_name_input.setText(first_name)
            self.last_name_input.setText(last_name)
            self.email_input.setText(self.table.item(row, 2).text())
            self.address_input.setText(self.table.item(row, 3).text())

    def show_error(self, title, msg):
        QMessageBox.critical(self, title, msg)

    def show_message(self, title, msg):
        QMessageBox.information(self, title, msg)