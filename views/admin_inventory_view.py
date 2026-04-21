from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox
)
from PyQt6.QtCore import Qt
from config import APP_WIDTH, APP_HEIGHT
from utils.helpers import center_window


class AdminInventoryView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Inventory Books")
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

            QLabel#fieldLabel {
                font-size: 11px;
                font-weight: bold;
                color: #555;
                background: transparent;
            }

            QLineEdit, QComboBox {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background: white;
                color: #222;
            }

            QPushButton#searchButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }

            QPushButton#searchButton:hover {
                background-color: #2980b9;
            }

            QPushButton#showAllButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }

            QPushButton#showAllButton:hover {
                background-color: #27ae60;
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
        main_card.setFixedSize(930, 620)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QLabel("Inventory Books")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Monitor all books used by library users")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title, author, category, or status")

        search_btn = QPushButton("Search")
        search_btn.setObjectName("searchButton")
        search_btn.clicked.connect(self.controller.search_admin_inventory)

        show_all_btn = QPushButton("Show All")
        show_all_btn.setObjectName("showAllButton")
        show_all_btn.clicked.connect(self.controller.load_admin_inventory)

        top_row.addWidget(self.search_input)
        top_row.addWidget(search_btn)
        top_row.addWidget(show_all_btn)

        filter_row = QHBoxLayout()
        filter_row.setSpacing(10)

        filter_label = QLabel("Show Books:")
        filter_label.setObjectName("fieldLabel")

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Available", "Borrowed"])
        self.filter_combo.currentIndexChanged.connect(lambda: self.controller.filter_admin_inventory())

        filter_row.addWidget(filter_label)
        filter_row.addWidget(self.filter_combo)
        filter_row.addStretch()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "Category", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.controller.back_to_admin_dashboard_from_inventory)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(top_row)
        layout.addLayout(filter_row)
        layout.addWidget(self.table)
        layout.addWidget(back_btn)

        root_layout.addWidget(main_card)
        self.setLayout(root_layout)

    def populate_table(self, books):
        self.table.clearContents()
        self.table.setRowCount(len(books))

        for row, book in enumerate(books):
            self.table.setItem(row, 0, QTableWidgetItem(str(book["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(book["title"]))
            self.table.setItem(row, 2, QTableWidgetItem(book["author"]))
            self.table.setItem(row, 3, QTableWidgetItem(book["category"] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(book["status"]))