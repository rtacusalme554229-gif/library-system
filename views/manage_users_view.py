from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QLineEdit, QComboBox
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
                color: #111827;
            }

            QFrame#mainCard {
                background-color: white;
                border: 1px solid #d9d9d9;
                border-radius: 20px;
            }

            QFrame#editPanel {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
            }

            QLabel#titleLabel {
                font-size: 25px;
                font-weight: bold;
                color: #111827;
                background: transparent;
            }

            QLabel#subtitleLabel {
                font-size: 12px;
                color: #6b7280;
                background: transparent;
            }

            QLabel#sectionTitle {
                font-size: 15px;
                font-weight: bold;
                color: #111827;
                background: transparent;
            }

            QLabel#hintLabel {
                font-size: 11px;
                color: #6b7280;
                background: transparent;
            }

            QPushButton#primaryButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }

            QPushButton#primaryButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton#updateButton {
                background-color: #16a34a;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: bold;
            }

            QPushButton#updateButton:hover {
                background-color: #15803d;
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

            QLineEdit, QComboBox {
                padding: 9px;
                border: 1px solid #d1d5db;
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
        main_card.setFixedSize(960, 660)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(24, 18, 24, 18)
        layout.setSpacing(12)

        title = QLabel("Manage Users")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Create users, update user information, and manage account status.")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # TOP BAR
        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        create_user_btn = QPushButton("+ Create User")
        create_user_btn.setObjectName("primaryButton")
        create_user_btn.clicked.connect(self.controller.open_create_user_popup)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setObjectName("primaryButton")
        refresh_btn.clicked.connect(self.controller.load_manage_users)

        top_row.addWidget(create_user_btn)
        top_row.addWidget(refresh_btn)
        top_row.addStretch()

        # TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Full Name", "Email", "Address", "Contact No.", "Role", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellClicked.connect(self.select_row)

        # EDIT PANEL
        edit_panel = QFrame()
        edit_panel.setObjectName("editPanel")

        edit_layout = QVBoxLayout(edit_panel)
        edit_layout.setContentsMargins(14, 12, 14, 12)
        edit_layout.setSpacing(10)

        panel_title = QLabel("Selected User")
        panel_title.setObjectName("sectionTitle")

        panel_hint = QLabel("Select a user, edit the details, then click Update User.")
        panel_hint.setObjectName("hintLabel")

        first_row = QHBoxLayout()
        first_row.setSpacing(10)

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        first_row.addWidget(self.first_name_input)
        first_row.addWidget(self.last_name_input)
        first_row.addWidget(self.email_input)

        second_row = QHBoxLayout()
        second_row.setSpacing(10)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Address")

        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Contact No.")

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Active", "Inactive"])

        second_row.addWidget(self.address_input)
        second_row.addWidget(self.contact_input)
        second_row.addWidget(self.status_combo)

        action_row = QHBoxLayout()
        action_row.setSpacing(10)

        update_btn = QPushButton("Update User")
        update_btn.setObjectName("updateButton")
        update_btn.clicked.connect(self.controller.update_selected_user)

        action_row.addStretch()
        action_row.addWidget(update_btn)

        edit_layout.addWidget(panel_title)
        edit_layout.addWidget(panel_hint)
        edit_layout.addLayout(first_row)
        edit_layout.addLayout(second_row)
        edit_layout.addLayout(action_row)

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_librarian_dashboard_from_users)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(top_row)
        layout.addWidget(self.table)
        layout.addWidget(edit_panel)
        layout.addWidget(back_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    def populate_table(self, users):
        self.table.clearContents()
        self.table.setRowCount(len(users))
        self.selected_user_id = None
        self.clear_edit_form()

        for row, user in enumerate(users):
            full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}"
            role = "User"
            status = user.get("status", "Active")
            contact_no = user.get("contact_no", "")

            self.table.setItem(row, 0, QTableWidgetItem(str(user.get("id", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(full_name))
            self.table.setItem(row, 2, QTableWidgetItem(str(user.get("email", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(user.get("address", ""))))
            self.table.setItem(row, 4, QTableWidgetItem(str(contact_no)))
            self.table.setItem(row, 5, QTableWidgetItem(role))
            self.table.setItem(row, 6, QTableWidgetItem(status))

    def select_row(self, row, col):
        id_item = self.table.item(row, 0)
        name_item = self.table.item(row, 1)
        email_item = self.table.item(row, 2)
        address_item = self.table.item(row, 3)
        contact_item = self.table.item(row, 4)
        status_item = self.table.item(row, 6)

        if not id_item:
            return

        self.selected_user_id = int(id_item.text())

        full_name = name_item.text().split(" ", 1) if name_item else [""]

        self.first_name_input.setText(full_name[0])
        self.last_name_input.setText(full_name[1] if len(full_name) > 1 else "")
        self.email_input.setText(email_item.text() if email_item else "")
        self.address_input.setText(address_item.text() if address_item else "")
        self.contact_input.setText(contact_item.text() if contact_item else "")
        self.status_combo.setCurrentText(status_item.text() if status_item else "Active")

    def clear_edit_form(self):
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.contact_input.clear()
        self.status_combo.setCurrentText("Active")

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)