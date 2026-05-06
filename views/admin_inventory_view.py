from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class AdminInventoryView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Admin Inventory")
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

            QFrame#topPanel {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
            }

            QLabel#titleLabel {
                font-size: 26px;
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

            QLineEdit, QComboBox {
                padding: 10px;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                background: white;
                color: #222;
                font-size: 12px;
            }

            QPushButton#refreshButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }

            QPushButton#refreshButton:hover {
                background-color: #1d4ed8;
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

        title = QLabel("Book Inventory")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Admin view of total copies, available copies, borrowed copies, lost copies, and book status.")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ================= TOP PANEL =================

        top_panel = QFrame()
        top_panel.setObjectName("topPanel")

        top_layout = QVBoxLayout(top_panel)
        top_layout.setContentsMargins(16, 14, 16, 14)
        top_layout.setSpacing(10)

        section_title = QLabel("Inventory Search & Filter")
        section_title.setObjectName("sectionTitle")

        hint = QLabel("Admins can monitor book inventory copies here. Book details are managed by the librarian.")
        hint.setObjectName("hintLabel")

        search_row = QHBoxLayout()
        search_row.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title, author, category, or status")
        self.search_input.textChanged.connect(self.controller.search_admin_inventory)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Available", "Borrowed", "Lost"])
        self.filter_combo.currentTextChanged.connect(self.controller.filter_admin_inventory)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setObjectName("refreshButton")
        refresh_btn.clicked.connect(self.controller.load_admin_inventory)

        search_row.addWidget(self.search_input, 4)
        search_row.addWidget(self.filter_combo, 1)
        search_row.addWidget(refresh_btn)

        top_layout.addWidget(section_title)
        top_layout.addWidget(hint)
        top_layout.addLayout(search_row)

        # ================= TABLE =================

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Title", "Author", "Category",
            "Total", "Available", "Borrowed", "Lost", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # ================= BACK =================

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_admin_dashboard_from_inventory)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(top_panel)
        layout.addWidget(self.table)
        layout.addWidget(back_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    # ================= DATA =================

    def populate_table(self, books):
        self.table.clearContents()
        self.table.setRowCount(len(books))

        for row, book in enumerate(books):
            self.table.setItem(row, 0, QTableWidgetItem(str(book.get("id", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(book.get("title", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(book.get("author", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(book.get("category", "") or "")))
            self.table.setItem(row, 4, QTableWidgetItem(str(book.get("total_copies", 1))))
            self.table.setItem(row, 5, QTableWidgetItem(str(book.get("available_copies", 0))))
            self.table.setItem(row, 6, QTableWidgetItem(str(book.get("borrowed_copies", 0))))
            self.table.setItem(row, 7, QTableWidgetItem(str(book.get("lost_copies", 0))))
            self.table.setItem(row, 8, QTableWidgetItem(str(book.get("status", ""))))

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)