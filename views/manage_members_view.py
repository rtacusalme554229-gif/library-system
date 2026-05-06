from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QLineEdit, QComboBox
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

        self.setWindowTitle("Manage Accounts")
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

            QLabel#roleLabel {
                font-size: 12px;
                color: #374151;
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

            QPushButton#tabButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }

            QPushButton#tabButton:hover {
                background-color: #333333;
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

            QPushButton#deleteButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: bold;
            }

            QPushButton#deleteButton:hover {
                background-color: #b91c1c;
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

        title = QLabel("Manage Accounts")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Create librarians, view users, update account details, and manage access.")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ================= TOP BAR =================

        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        create_librarian_btn = QPushButton("+ Create Librarian")
        create_librarian_btn.setObjectName("primaryButton")
        create_librarian_btn.clicked.connect(self.controller.open_create_librarian_popup)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setObjectName("primaryButton")
        refresh_btn.clicked.connect(lambda: self.controller.load_members(self.current_role))

        self.librarian_btn = QPushButton("Librarians")
        self.librarian_btn.setObjectName("tabButton")
        self.librarian_btn.clicked.connect(lambda: self.controller.load_members("librarian"))

        self.user_btn = QPushButton("Users")
        self.user_btn.setObjectName("tabButton")
        self.user_btn.clicked.connect(lambda: self.controller.load_members("student"))

        top_row.addWidget(create_librarian_btn)
        top_row.addWidget(refresh_btn)
        top_row.addStretch()
        top_row.addWidget(self.librarian_btn)
        top_row.addWidget(self.user_btn)

        self.role_label = QLabel("Showing: Librarians")
        self.role_label.setObjectName("roleLabel")

        # ================= TABLE =================

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Full Name", "Email", "Address", "Role", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellClicked.connect(self.select_row)

        # ================= SELECTED ACCOUNT PANEL =================

        self.edit_panel = QFrame()
        self.edit_panel.setObjectName("editPanel")

        edit_layout = QVBoxLayout(self.edit_panel)
        edit_layout.setContentsMargins(14, 12, 14, 12)
        edit_layout.setSpacing(10)

        panel_title = QLabel("Selected Account")
        panel_title.setObjectName("sectionTitle")

        panel_hint = QLabel(
            "Select a row, edit the details or status, then click Update Account."
        )
        panel_hint.setObjectName("hintLabel")

        fields_row = QHBoxLayout()
        fields_row.setSpacing(10)

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Address")

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Active", "Inactive"])

        fields_row.addWidget(self.first_name_input)
        fields_row.addWidget(self.last_name_input)
        fields_row.addWidget(self.email_input)
        fields_row.addWidget(self.address_input)
        fields_row.addWidget(self.status_combo)

        action_row = QHBoxLayout()
        action_row.setSpacing(10)

        self.update_btn = QPushButton("Update Account")
        self.update_btn.setObjectName("updateButton")
        self.update_btn.clicked.connect(self.controller.update_selected_account)

        self.delete_btn = QPushButton("Delete Account")
        self.delete_btn.setObjectName("deleteButton")
        self.delete_btn.clicked.connect(self.controller.delete_selected_account)

        action_row.addStretch()
        action_row.addWidget(self.update_btn)
        action_row.addWidget(self.delete_btn)

        edit_layout.addWidget(panel_title)
        edit_layout.addWidget(panel_hint)
        edit_layout.addLayout(fields_row)
        edit_layout.addLayout(action_row)

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_admin_dashboard_from_members)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(top_row)
        layout.addWidget(self.role_label)
        layout.addWidget(self.table)
        layout.addWidget(self.edit_panel)
        layout.addWidget(back_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

        self.set_user_edit_mode("librarian")

    # ================= HELPERS =================

    def clear_edit_form(self):
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.status_combo.setCurrentText("Active")

    def set_user_edit_mode(self, role_name):
        """
        Librarian tab:
        - Can update info and status.
        - Can delete librarian.

        Users tab:
        - Can update status.
        - Info fields are disabled to avoid accidental user info editing.
        """
        if role_name == "student":
            self.first_name_input.setEnabled(False)
            self.last_name_input.setEnabled(False)
            self.email_input.setEnabled(False)
            self.address_input.setEnabled(False)
            self.delete_btn.setVisible(False)
        else:
            self.first_name_input.setEnabled(True)
            self.last_name_input.setEnabled(True)
            self.email_input.setEnabled(True)
            self.address_input.setEnabled(True)
            self.delete_btn.setVisible(True)

    def populate_table(self, users, role_name):
        self.current_role = role_name

        if role_name == "student":
            self.role_label.setText("Showing: Users")
        else:
            self.role_label.setText("Showing: Librarians")

        self.set_user_edit_mode(role_name)

        self.table.clearContents()
        self.table.setRowCount(len(users))

        self.selected_user_id = None
        self.clear_edit_form()

        for row, user in enumerate(users):
            full_name = f"{user['first_name']} {user['last_name']}"
            display_role = "User" if user["role"] == "student" else user["role"].capitalize()
            status = user.get("status", "Active")

            self.table.setItem(row, 0, QTableWidgetItem(str(user["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(full_name))
            self.table.setItem(row, 2, QTableWidgetItem(user["email"]))
            self.table.setItem(row, 3, QTableWidgetItem(user["address"] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(display_role))
            self.table.setItem(row, 5, QTableWidgetItem(status))

    def select_row(self, row, col):
        self.selected_user_id = int(self.table.item(row, 0).text())
        self.status_combo.setCurrentText(self.table.item(row, 5).text())

        full_name = self.table.item(row, 1).text().split(" ", 1)

        self.first_name_input.setText(full_name[0])
        self.last_name_input.setText(full_name[1] if len(full_name) > 1 else "")
        self.email_input.setText(self.table.item(row, 2).text())
        self.address_input.setText(self.table.item(row, 3).text())

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)